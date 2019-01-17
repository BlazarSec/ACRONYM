#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from logging import iprint, eprint, dprint, wprint
import skeleton
import sample
import os

if __name__ == "__main__":
    loaded_sample = None

    try:
        while True:
            logging.reset_print()
            print("""1 - build basic skeleton
2 - create sample
3 - save sample
4 - load sample
0 - exit
    """)
            uinput = input(">")
            try:
                option = int(uinput)
            except ValueError:
                eprint("please enter integers")
                continue

            if option == 1:
                name = input("enter project name> ")
                path = input("enter project path> ")
                skeleton.scaffold_skeleton(path, name)
                iprint("skeleton built")
            elif option == 2:
                name = input("enter project name> ")
                path = input("enter project path> ")
                loaded_sample = sample.Sample(name, path)
                iprint("sample created")
            elif option == 3:
                if loaded_sample:
                    loaded_sample.pickle()
                    iprint("sample saved")
                else:
                    eprint("no sample to save")
            elif option == 4:
                path = input("enter project path> ")
                loaded_sample = sample.unpickle_from(os.path.join(path, ".sample.pickle"))
                iprint("sample loaded")
    except EOFError:
        exit(0)
