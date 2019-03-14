#!/usr/bin/env python3

import sys
from acronym.sample import *
from acronym.cmake import *
from acronym.args import *

#TODO switch prints to use the exisitng logging interface
if __name__ == "__main__":
    args = Args(sys.argv)
    sam = None
    print(f"==>{args.mode}<==")
    if args.mode == "test":
        suite = unittest.TestSuite()
        results = unittest.TestResult()
        suite.addTest(unittest.makeSuite(ArgsTest))
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
                print(str(target))
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
            elif args.mode == "set":
                print(f"setting {args.set} {args.state}")

        #global mode
        else:
            print("==>global<==")
            if args.mode == "stat":
                print(str(sam.cmake))
            elif args.mode == "add":
                print(f"adding {args.add} {args.type} {args.option}")
            elif args.mode == "set":
                print(f"setting {args.set} to {args.state}")

    if sam:
        if args.mode not in ['help', 'stat']:
            sam.gen_cmake()
        #save changes
        sam.pickle()

'''
    parser = argparse.ArgumentParser(description="ACRONYM")
    parser.add_argument("name", help="the name of the project to generate")
    parser.add_argument("path", help="path to the project")
    parser.add_argument("mode", help="what operation to perform", choices=["gen","status"])
    parser.add_argument("--scan", help="when rebuilding, scan the specified folder for sources, defaults to 'src/'", nargs='?', const='src/')
    parser.add_argument("--c3po", help="enable c3po additional build steps", action='store_true')
    parser.add_argument("--strip", help="enable strip additional build step", action='store_true')
    parser.add_argument("--link", help="add additional linking options comma seperated, defaults to 'rt,pthreads'", nargs='?', const='rt,pthread')

    args = parser.parse_args()

    if args.mode == "gen":
        sam = Sample(args.name, args.path, c3po=args.c3po, strip=args.strip)
        if args.scan:
            scan_path = os.path.join(sam.path, args.scan)
            paths = [os.path.join(args.scan, file) for file in os.listdir(scan_path) if os.path.isfile(os.path.join(scan_path, file)) and file.endswith(".c")]
            sam.cmake.add_target(args.name, files=paths, libraries=args.link.split(',') if args.link else [])
        else:
            sam.cmake.add_target(args.name)
        sam.gen_scaffold()
        sam.gen_cmake()
        sam.pickle()
    else:
        path = args.path
        if os.path.basename(path).lower() != args.name.lower():
            path = os.path.join(path, args.name)
        sam = unpickle_from(os.path.join(path, ".sample.pickle"))
        print(str(sam.cmake))
        '''
