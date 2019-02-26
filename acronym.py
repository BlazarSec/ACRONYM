#!/usr/bin/env python3

import argparse
from acronym.sample import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ACRONYM")
    parser.add_argument("name", help="the name of the project to generate")
    parser.add_argument("path", help="path to the project")
    parser.add_argument("mode", help="what operation to perform", choices=["gen","status"])

    args = parser.parse_args()

    if args.mode == "gen":
        sam = Sample(args.name, args.path)
        sam.gen_scaffold()
        sam.gen_cmake()
        sam.pickle()
    else:
        sam = unpickle_from(os.path.join(args.path, ".sample.pickle"))
        print(str(sam.cmake))
