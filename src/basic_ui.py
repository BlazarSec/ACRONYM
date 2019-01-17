#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from logging import iprint, eprint, dprint, wprint
import skeleton
import sample
import os

base_menu = """1 - create sample
2 - load sample
0 - exit
"""
loaded_menu= """1 - create sample
2 - load sample
3 - build basic skeleton
4 - save sample
0 - exit
"""

if __name__ == "__main__":
    loaded_sample = None
    promptstr = ": "
    try:
        while True:
            logging.reset_print()
            if loaded_sample:
                promptstr = "{}: ".format(loaded_sample.prompt())
                print(loaded_menu)
            else:
                print(base_menu)

            uinput = input(promptstr)
            try:
                option = int(uinput)
            except ValueError:
                eprint("please enter integers")
                continue

            if option == 0:
                #TODO check for unsaved changes
                exit(0)
            elif option == 1:
                name = input("enter project name: ")
                path = input("enter project path: ")
                loaded_sample = sample.Sample(name, path)
                iprint("sample created")
            elif option == 2:
                path = input("enter project path: ")
                try:
                    loaded_sample = sample.unpickle_from(os.path.join(path, ".sample.pickle"))
                    iprint("sample loaded")
                except FileNotFoundError:
                    eprint("sample not found")
            elif loaded_sample and option == 3:
                skeleton.scaffold_skeleton(loaded_sample.path, loaded_sample.name)
                iprint("skeleton built")
            elif loaded_sample and option == 4:
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
