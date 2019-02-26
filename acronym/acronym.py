#!/bin/python3

"""
Main script for CLI frontend
"""

import sys
import getopt
from os.path import dirname, realpath

import cli
import sample
import templates

# usage info
def usage():
    print(
        "acroym - A Cool Red-Operative Network Yeeting Multitool\n"
        "Usage:\n"
        " acronym [options] :: launch acronym\n"
        " acronym [options] <sample> :: launch acronym and load saved <sample>\n"
        "\n"
        "Options:\n"
        " -h --help :: this\n"
        " -d --dir <dir> :: load initial packages from <dir> instead of acronym/packages/"
    )

# handle options/arguments and initialize CLI
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:", ["help", "dir="])

    except getopt.GetoptError as e:
        print(e, end="\n\n")
        usage()
        sys.exit(-1)

    # default values
    #TODO try/except block this for folder not found or unreadable
    init_local_packages = dirname(realpath(__file__))+"/../packages"

    # handle (option, value) pairs
    for opt, val in opts:
        if opt in ["-h", "--help"]:
            usage()
            sys.exit(-1)

        if opt in ["-d", "--dir"]:
            init_local_packages = val

    # instantiate CLI
     
    instance = None

    if args:
        if len(args) != 1:
            print("wrong number of args: requires 0 or 1, got " + len(args), end="\n\n")
            usage()
            sys.exit(-1)
        
        try:
            instance = cli.Instance(init_local_packages, sample=sample.unpickle_from(args[0]))
            print("[*] Loaded '{}'".format(args[0]))

        except Exception as e:
            print("[!] An error occurred while attempting to load {}:\n{}", args[0], e)
            sys.exit(-1)
    else:
        instance = cli.Instance(init_local_packages)
        print("[*] No sample specified - initialized blank sample")

    # read lines from stdin and feed to CLI instance
    while True:
        command = input(" > ").strip().split(" ")

        if len(command[0]):
            instance.try_run(command)

if __name__ == "__main__":
    main()