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
    "name": "package",
    "includes": [
        "package.h"
    ],
    "init":"package_init",
    "events": {
        "handled":{
            "timer": "hander_function"
        },
        "generated":[
            "timer",
        ]
    }
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
    cmain = ""

    cincludes = ""
    cinit = ""
    cclose = ""

    cbroadcast_constants = ""
    cbroadcast_type_totals = ""
    cbroadcast_callback_assignment = ""

    #the regex replacement of the main template
    reincludes = re.compile(r"{<includes>}")
    reinit = re.compile(r"{<init>}")
    reclose = re.compile(r"{<close>}")

    rebroadcast_constants = re.compile(r"{<broadcast_constants>}")
    rebroadcast_type_totals = re.compile(r"{<broadcast_type_totals>}")
    rebroadcast_callback_assignment = re.compile(r"{<broadcast_callback_assignment>}")

    with open("packages/main.c.template") as main_file:
        cmain = main_file.read()

    handled_events = {}
    generated_events = {}
    for p in sample:
        #collect and join includes
        cincludes += "\n".join(["#include \"{}/{}\"\n".format(p, h) for h in sample[p]["includes"]])
        if "init" in sample[p]:
            cinit += "    {}();\n".format(sample[p]["init"])
        if "close" in sample[p]:
            cclose += "    {}();\n".format(sample[p]["close"])

        if "events" in sample[p]:
            sevent = sample[p]["events"]
            #collect information needed for events
            if "handled" in sevent:
                for event in sevent["handled"]:
                    if event not in handled_events:
                        handled_events[event] = []
                    handled_events[event].append(sevent["handled"][event])
            if "generated" in sevent:
                for event in sevent["generated"]:
                    if event not in generated_events:
                        generated_events[event] = 0

    #TODO check if it works with an event producer and consumber mismatch occurs
    total_events = len(handled_events);

    cbroadcast_constants += "int broadcast_total_types = {};".format(total_events)

    event_type = 0;
    for gevent in generated_events:
        generated_events[gevent] = len(handled_events[gevent])
        cbroadcast_constants += "int broadcast_type_{} = {};".format(gevent, event_type)
        event_type += 0

    cbroadcast_type_totals = """
    broadcast_type_totals = {{
        {}
    }};
    """.format(",\n        ".join(str(len(handled_events[h])) for h in handled_events))

    event_type = 0;
    for gevent in generated_events:
        cbroadcast_callback_assignment += "    broadcast_callback[{}] = malloc(sizeof(void (*)(const broadcast_msg_t*))*broadcast_type_totals[{}]);\n".format(event_type, event_type)

        type_specific = 0
        for callback in handled_events[gevent]:
            cbroadcast_callback_assignment += "    broadcast_callback[{}][{}] = {};\n".format(event_type, type_specific, callback);
            type_specific += 1;

        event_type += 1;

    #simple replacement of includes, init, and cleanup
    cmain = reincludes.sub(cincludes, cmain)
    cmain = reinit.sub(cinit, cmain)
    cmain = reclose.sub(cclose, cmain)

    #replacement of broadcast system
    cmain = rebroadcast_constants.sub(cbroadcast_constants, cmain)
    cmain = rebroadcast_type_totals.sub(cbroadcast_type_totals, cmain)
    cmain = rebroadcast_callback_assignment.sub(cbroadcast_callback_assignment, cmain)

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
