#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from logging import iprint, eprint, dprint, wprint, nprint
import sample
import os
import re

base_menu = """1 - create sample
2 - load sample
0 - exit
"""
loaded_menu = """1 - create sample
2 - load sample
3 - save sample
4 - regenerate sample
5 - regenerate cmake
6 - configure cmake
0 - exit
"""

sampletype_menu = """1 - default project
0 - back
"""

main_config_menu = """1 - add target
2 - add debug defines
3 - add release defines
4 - add debug flags
5 - add release flags
6 - list targets
7 - select target
0 - exit
"""
target_config_menu = """1 - add debug defines
2 - add release defines
3 - add debug flags
4 - add release flags
5 - add file
6 - add include
7 - add library
0 - exit
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
                else:
                    eprint("unknown sample type")

            elif option == 2:
                path = input("enter project path: ")
                try:
                    loaded_sample = sample.unpickle_from(os.path.join(path, ".sample.pickle"))
                    iprint("sample loaded")
                    nprint(loaded_sample.cmake.debug())
                except FileNotFoundError:
                    eprint("sample not found")
            elif loaded_sample and option == 3:
                #requires the sample to not be null
                loaded_sample.pickle()
                iprint("sample saved")
            elif loaded_sample and option == 4:
                loaded_sample.gen_scaffold()
                iprint("skeleton built")
                loaded_sample.gen_cmake()
                iprint("cmake generated")
            elif loaded_sample and option == 5:
                loaded_sample.gen_cmake()
                iprint("cmake generated")
            elif loaded_sample and option == 6:
                while True:
                    nprint(main_config_menu)
                    opt = intresp(promptstr)
                    if opt == 0:
                        break
                    elif opt == 1:
                        name = input("enter target name: ")
                        loaded_sample.cmake.add_target(name)
                    elif opt == 2:
                        key = input("enter key: ")
                        value = input("enter value: ")
                        loaded_sample.cmake.add_debug_define(key, value)
                    elif opt == 3:
                        key = input("enter key: ")
                        value = input("enter value: ")
                        loaded_sample.cmake.add_release_define(key, value)
                    elif opt == 4:
                        flags = input("enter flags (-O0 -flto ...): ")
                        loaded_sample.cmake.add_debug_flags(flags.split())
                    elif opt == 5:
                        flags = input("enter flags (-O0 -flto ...): ")
                        loaded_sample.cmake.add_release_flags(flags.split())
                    elif opt == 6:
                        for index, target in enumerate(loaded_sample.cmake.targets):
                            nprint(">{} - {}".format(index+1,target.name))
                    elif opt == 7:
                        index = intresp("enter index: ")
                        if index > 0 and index <= len(loaded_sample.cmake.targets):
                            index -= 1
                            while True:
                                nprint(target_config_menu)
                                opt = intresp("[{}]{}".format(loaded_sample.cmake.targets[index].name, promptstr))
                                if opt == 0:
                                    break
                                elif opt == 1:
                                    key = input("enter key: ")
                                    value = input("enter value: ")
                                    loaded_sample.cmake.targets[index].add_debug_define(key, value)
                                elif opt == 2:
                                    key = input("enter key: ")
                                    value = input("enter value: ")
                                    loaded_sample.cmake.targets[index].add_release_define(key, value)
                                elif opt == 3:
                                    flags = input("enter flags (-O0 -flto ...): ")
                                    loaded_sample.cmake.targets[index].add_debug_flags(flags.split())
                                elif opt == 4:
                                    flags = input("enter flags (-O0 -flto ...): ")
                                    loaded_sample.cmake.targets[index].add_release_flags(flags.split())
                                elif opt == 5:
                                    path = input("enter path: ")
                                    loaded_sample.cmake.targets[index].add_file(path)
                                elif opt == 6:
                                    path = input("enter path: ")
                                    loaded_sample.cmake.targets[index].add_include(path)
                                elif opt == 7:
                                    lib = input("enter library: ")
                                    loaded_sample.cmake.targets[index].add_library(lib)
                        else:
                            eprint("index out of range")


            else:
                wprint("unknown option")
    except EOFError:
        #TODO check for unsaved changes
        exit(0)
    except KeyboardInterrupt:
        #TODO check for unsaved changes
        exit(0)
