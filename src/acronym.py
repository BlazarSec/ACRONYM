#!/bin/python3

"""
Main script for CLI frontend
"""

import sys
import getopt
from os.path import dirname, realpath

import templates
import cli

# usage info
def usage():
    print("acroym - A Cool Red-Operative Network Yeeting Multitool")
    print("Usage:")
    print(" acronym [options] :: launch acronym")
    print(" acronym [options] <sample> :: launch acronym and load saved <sample>")
    print("")
    print("Options:")
    print(" -h --help :: this")
    print(" -d --dir <dir> :: load initial packages from <dir> instead of acronym/packages/")

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

    # handle args
    if args:
        if len(args) != 1:
            print("wrong number of args: requires 0 or 1, got " + len(args), end="\n\n")
            usage()
            sys.exit(-1)
        
        #TODO allow dumping of samples as python pickles, and reconstruction of samples from pickles
        print("[$] Warning: saved sample loading not yet implemented")

    # instantiate CLI and handle commands
    instance = cli.Instance(init_local_packages)

    while True:
        command = input(" > ").split(" ")

        if len(command[0]):
            instance.try_run(command)

if __name__ == "__main__":
    main()