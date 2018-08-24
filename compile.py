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

if __name__ == "__main__":
    sample = {}
    packages = get_packages()
    for p in packages:
        print("package: {}".format(p))
        pack = parse_package(p)
        print("    files: {}".format(pack))
        sample[p] = pack

    reincludes = re.compile(r"{<includes>}")
    cincludes = ""

    reinit = re.compile(r"{<init>}")
    cinit = ""

    rebreak = re.compile(r"{<break>}")
    rebreakaround = re.compile(r"^[ ]*{<\?break>}(.|\n)*{<!break>}$", re.MULTILINE)
    resbreak = re.compile(r"{<\?break>}")
    reebreak = re.compile(r"{<!break>}")
    cbreak = ""

    reclose = re.compile(r"{<close>}")
    cclose = ""

    mainstr = ""
    with open("packages/main.c.template") as main_file:
        mainstr = main_file.read()


    #loop through all the selected samples and then add them all into their replacement strings
    #once thats happened generate out the new main file via the template replacement

    #for p in sample:
    #    if "init.h" in p:

    #simple replacement of includes, init, and cleanup
    mainstr = reincludes.sub(cincludes, mainstr)
    mainstr = reinit.sub(cinit, mainstr)
    mainstr = reclose.sub(cclose, mainstr)

    #if there are no breaks, remove the loop
    if len(cbreak) == 0:
        mainstr = rebreakaround.sub("", mainstr)
    else:
        mainstr = resbreak.sub("", mainstr)
        mainstr = reebreak.sub("", mainstr)
        mainstr = rebreak.sub(cbreak, mainstr)

    #write the generated main file into main.c
    print(mainstr)
    with open("packages/main.c", "w+") as main_file:
        main_file.write(mainstr)
