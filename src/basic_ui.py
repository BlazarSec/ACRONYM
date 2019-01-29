#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from logging import iprint, eprint, dprint, wprint, nprint
import skeleton
import sample
import os
import re

base_menu = """1 - create sample
2 - load sample
0 - exit
"""
loaded_menu= """1 - create sample
2 - load sample
3 - build basic skeleton
4 - add git repo
5 - save sample
0 - exit
"""

sampletype_menu = """1 - default project
2 - basic RAT
0 - back
"""

fullyre = re.compile('^(git|ssh|(ftp|http)(s)?).*')

def intresp(prompt):
    while True:
        logging.reset_print()
        uinput = input(prompt)
        try:
            option = int(uinput)
            return option
        except ValueError:
            eprint("please enter integers")

if __name__ == "__main__":
    loaded_sample = None
    promptstr = ": "
    try:
        while True:
            logging.reset_print()
            if loaded_sample:
                promptstr = "{}: ".format(loaded_sample.prompt())
                nprint(loaded_menu)
            else:
                nprint(base_menu)

            option = intresp(promptstr)

            if option == 0:
                #TODO check for unsaved changes
                exit(0)
            elif option == 1:
                nprint(sampletype_menu)
                sample_option = intresp(promptstr)
                if sample_option == 0:
                    continue

                name = input("enter project name: ")
                path = input("enter project path: ")
                if sample_option == 1:
                    loaded_sample = sample.Sample(name, path)
                    iprint("sample created")
                elif sample_option == 2:
                    host = input("server ip or host: ")
                    loaded_sample = sample.RAT(name, path, host)

            elif option == 2:
                path = input("enter project path: ")
                try:
                    loaded_sample = sample.unpickle_from(os.path.join(path, ".sample.pickle"))
                    iprint("sample loaded")
                except FileNotFoundError:
                    eprint("sample not found")
            elif loaded_sample and option == 3:
                skeleton.scaffold_skeleton(loaded_sample.path, loaded_sample.name, loaded_sample.cmake())
                iprint("skeleton built")
            elif loaded_sample and option == 4:
                url = input("enter github user/repo or fully qualified url: ")
                if not fullyre.match(url):
                    url = "https://github.com/" + url
                loaded_sample.add_git_repo(url)
            elif loaded_sample and option == 5:
                #requires the sample to not be null
                loaded_sample.pickle()
                iprint("sample saved")
            else:
                wprint("unknown option")
    except EOFError:
        #TODO check for unsaved changes
        exit(0)
    except KeyboardInterrupt:
        #TODO check for unsaved changes
        exit(0)
