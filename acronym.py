#!/usr/bin/env python3

import argparse
from acronym.sample import *
from acronym.cmake import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ACRONYM")
    parser.add_argument("name", help="the name of the project to generate")
    parser.add_argument("path", help="path to the project")
    parser.add_argument("mode", help="what operation to perform", choices=["gen","status"])
    parser.add_argument("--scan", help="when rebuilding, scan the specified folder for sources, defaults to 'src/'", nargs='?', const='src/', default='src/')
    parser.add_argument("--c3po", help="enable c3po additional build steps", default=False)

    args = parser.parse_args()

    if args.mode == "gen":
        sam = Sample(args.name, args.path, c3po=args.c3po)
        if args.scan:
            scan_path = os.path.join(sam.path, args.scan)
            paths = [os.path.join(args.scan, file) for file in os.listdir(scan_path) if os.path.isfile(os.path.join(scan_path, file)) and file.endswith(".c")]
            sam.cmake.add_target(args.name, files=paths)
        else:
            sam.cmake.targets.append(Target(args.name))
        sam.gen_scaffold()
        sam.gen_cmake()
        sam.pickle()
    else:
        sam = unpickle_from(os.path.join(args.path, ".sample.pickle"))
        print(str(sam.cmake))
