#!/bin/python3

import getopt
import sys

from os.path import dirname, realpath

import cli
import core.acmd

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
        " -e --exec <command> :: instead of opening shell session, exec command and exit."
    )

def main():
    instance = cli.Instance()

    # load commands from supplementary py packages
    try:
        core.acmd.load_into(instance)

    except ValueError as e:
        print(f"Error loading core: {e}")
        return 1

    # main loop, will feed lines of input into instance
    def loop():
        for (cmd, args) in cli.cstrparse(input("# ")): #TODO PS1?
            if len(cmd):
                try:
                    instance.run(cmd, args)

                except RuntimeError as e:
                    print(f"[!] <{cmd}>: {e}")

                except KeyError:
                    print(f"[!] {cmd} is not a defined command.")

    # start loop and hand control off to instance until finished.
    instance.loop_func = loop
    instance.start()

    return 0

if __name__ == "__main__":
    exit(main())