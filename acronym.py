#!/usr/bin/env python3

import sys
from acronym.sample import *
from acronym.cmake import *
from acronym.args import *

#demo run
#~/code/ACRONYM/acronym.py init testing ./
#cat >> testing/src/main.c
#~/code/ACRONYM/acronym.py ./testing/ main add file src/main.c

#TODO switch prints to use the exisitng logging interface
#TODO fix the pathing to allow running externally and from in the dir

if __name__ == "__main__":
    args = Args(sys.argv)
    sam = None
    print(f"==>{args.mode}<==")
    if args.mode == "test":
        suite = unittest.TestSuite()
        results = unittest.TestResult()
        suite.addTest(unittest.makeSuite(ArgsTest))
        suite.addTest(unittest.makeSuite(CmakeTest))
        runner = unittest.TextTestRunner()
        print(runner.run(suite))
    elif args.mode == "help":
        args_help()
        sys.exit(0)
    elif args.mode == "init":
        print(f"generating in {args.name}")
        sam = Sample.unpickle_from(args.path, args.name)
        if sam:
            print("found exising sample, regenerating")
        else:
            sam = Sample(path=args.path, name=args.name)
        sam.gen_scaffold()
    else:
        print(f"loading '{args.path}'")
        sam = Sample.unpickle_from(args.path)
        if not sam:
            print("unable to load sample")
            sys.exit(1)
        #target mode
        if args.target:
            target = None
            print(f"==>target: {args.target}<==")
            if args.target not in sam.cmake.targets:
                print(f"creating new target {args.target}")
                target = sam.cmake.add_target(args.target)
            else:
                target = sam.cmake.targets[args.target]

            if args.mode == "stat":
                print(f"path:{sam.path}\n{str(target)}")
            elif args.mode == "add":
                if args.add in ['debug', 'release']:
                    print(f"adding {args.add} {args.type} {args.option}")
                    if args.add == 'debug':
                        if args.type == 'flag':
                            target.debug_flags.extend(args.option)
                        else:
                            target.debug_defines.extend(args.option)
                    else:
                        if args.type == 'flag':
                            target.release_flags.extend(args.option)
                        else:
                            target.release_defines.extend(args.option)

                else:
                    print(f"adding {args.add} {args.option}")
                    if args.add == 'debug':
                        if args.type == 'flag':
                            target.debug_flags.extend(args.option)
                        else:
                            target.debug_defines.extend(args.option)
                    elif args.add == 'release':
                        if args.type == 'flag':
                            target.release_flags.extend(args.option)
                        else:
                            target.release_defines.extend(args.option)
                    elif args.add == 'file':
                        target.files.extend(args.option)
                    elif args.add == 'include':
                        target.includes.extend(args.option)
                    elif args.add == 'library':
                        target.libraries.extend(args.option)
            elif args.mode == "set":
                print(f"setting {args.set} {args.state}")
                if args.set == 'c3po':
                    target.c3po = args.state

        #global mode
        else:
            print("==>global<==")
            if args.mode == "stat":
                print(f"path:{sam.path}\n{str(sam.cmake)}")
            elif args.mode == "add":
                print(f"adding {args.add} {args.type} {args.option}")
                if args.add == 'debug':
                    if args.type == 'flag':
                        sam.cmake.debug_flags.extend(args.option)
                    else:
                        sam.cmake.debug_defines.extend(args.option)
                else:
                    if args.type == 'flag':
                        sam.cmake.release_flags.extend(args.option)
                    else:
                        sam.cmake.release_defines.extend(args.option)
            elif args.mode == "set":
                print(f"setting {args.set} to {args.state}")
                if args.set == 'c3po':
                    sam.cmake.c3po = args.state

    if sam:
        if args.mode not in ['help', 'stat']:
            sam.gen_cmake()
        #save changes
        sam.pickle()
