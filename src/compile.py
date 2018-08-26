#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import listdir
from os.path import isfile, isdir, join
import re

def get_packages():
    ppath = "packages"

    full_listing = listdir(ppath)

    alldirs = [f for f in full_listing if isdir(join(ppath, f))]

    return alldirs

def parse_package(folder):
    ppath = join("packages",folder)

    full_listing = listdir(ppath)

    allfiles = [f for f in full_listing if isfile(join(ppath, f))]

    return allfiles

def build_sample(packages):
    sample = {}
    for p in packages:
        pack = parse_package(p)
        sample[p] = pack
    return sample

def build_main(sample):
    #TODO generalize the regex to be based on dictionary lookups for any file
    cincludes = ""
    cinit = ""
    cbreak = ""
    cclose = ""
    cmain = ""

    #the regex replacement of the main template
    reincludes = re.compile(r"{<includes>}")

    reinit = re.compile(r"{<init>}")

    rebreak = re.compile(r"{<break>}")
    rebreakaround = re.compile(r"^[ ]*{<\?break>}(.|\n)*{<!break>}$", re.MULTILINE)
    resbreak = re.compile(r"{<\?break>}")
    reebreak = re.compile(r"{<!break>}")

    reclose = re.compile(r"{<close>}")

    with open("packages/main.c.template") as main_file:
        cmain = main_file.read()

    for p in sample:
        csamp = sample[p]
        #collect and join includes
        cincludes += "\n".join(["#include \"{}/{}\"\n".format(p, h) for h in sample[p] if h[-2:] == ".h"])
        if "init.h" in sample[p]:
            cinit += "{}_init();\n".format(p)
        if "break.h" in sample[p]:
            cbreak += """
        if (!{}_break()) {{
            break;
        }}
""".format(p)
        if "close.h" in sample[p]:
            cclose += "{}_close();\n".format(p)

    #simple replacement of includes, init, and cleanup
    cmain = reincludes.sub(cincludes, cmain)
    cmain = reinit.sub(cinit, cmain)
    cmain = reclose.sub(cclose, cmain)

    #if there are no breaks, remove the loop
    if len(cbreak) == 0:
        cmain = rebreakaround.sub("", cmain)
    else:
        cmain = resbreak.sub("", cmain)
        cmain = reebreak.sub("", cmain)
        cmain = rebreak.sub(cbreak, cmain)

    return cmain

def print_sample(sample):
    print("sample content")
    for p in sample:
        print("package: {}".format(p))
        print("    files: {}".format(", ".join(sample[p])))

if __name__ == "__main__":
    #if you want to run this directly make sure to run it from the root of the repo
    #./src/conpilw.py
    packages = get_packages()
    sample = build_sample(packages)
    print_sample(sample)

    cmain = build_main(sample)

    #write the generated main file into main.c
    print("generated main:\n")
    print(cmain)
    with open("packages/main.c", "w+") as main_file:
        main_file.write(cmain)
