#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import listdir
from os.path import isfile, isdir, join
import re
import json

def get_packages():
    ppath = "packages"

    full_listing = listdir(ppath)

    alldirs = [f for f in full_listing if isdir(join(ppath, f))]

    return alldirs

def parse_package(folder):
    ppath = join(join("packages",folder), "package.json")

    #this is the template for package.json
    """
{
    "name": "helloworld",
    "includes": [
        "helloworld.h"
    ],
    "init":"",
    "close":"",
    "event_handlers": []
}
"""

    package = None
    with open(ppath, "r") as pfile:
        package = json.load(pfile)

    return package

def build_sample(packages):
    sample = {}
    for p in packages:
        pack = parse_package(p)
        sample[p] = pack
    return sample

def build_main(sample):
    cincludes = ""
    cinit = ""
    cbreak = ""
    cclose = ""
    cmain = ""

    #the regex replacement of the main template
    reincludes = re.compile(r"{<includes>}")

    reinit = re.compile(r"{<init>}")

    reclose = re.compile(r"{<close>}")

    with open("packages/main.c.template") as main_file:
        cmain = main_file.read()

    for p in sample:
        csamp = sample[p]
        #collect and join includes
        cincludes += "\n".join(["#include \"{}/{}\"\n".format(p, h) for h in sample[p]["includes"]])
        if "init" in sample[p]:
            cinit += "{}();".format(sample[p]["init"])
        if "close" in sample[p]:
            cclose += "{}();".format(sample[p]["close"])

    #simple replacement of includes, init, and cleanup
    cmain = reincludes.sub(cincludes, cmain)
    cmain = reinit.sub(cinit, cmain)
    cmain = reclose.sub(cclose, cmain)

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
