#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys


def scaffold_skeleton(base_path, project_name):
    path = base_path
    if os.path.basename(base_path).lower() != project_name.lower():
        path = os.path.join(base_path, project_name)
        print("using fullpath {}".format(path))

    if not os.path.exists(path):
        print("creating folder")
        try:
            os.mkdir(path)
        except OSError:
            print("failed to create folder")
            return
    elif not os.path.isdir(path):
        print("path is not a folder")
    else:
        print("folder already exists")

    gitignore_path = os.path.join(path, ".gitignore")
    cmake_path = os.path.join(path, "CMakeLists.txt")
    bin_path = os.path.join(path, "bin")
    src_path = os.path.join(path, "src")
    main_path = os.path.join(path, "src", "main.c")

    if os.path.exists(gitignore_path):
        print("{} already exists".format(gitignore_path))
    else:
        with open(gitignore_path, "w") as f:
            f.write("bin/")

    if os.path.exists(cmake_path):
        print("{} already exists".format(cmake_path))
    else:
        with open(cmake_path, "w") as f:
            f.write("""cmake_minimum_required (VERSION 3.0)
project ({0})

set ({0}_VERSION_MAJOR 1)
set ({0}_VERSION_MINOR 0)

if(NOT CMAKE_BUILD_TYPE)
	set(CMAKE_BUILD_TYPE Release)
endif()


set(CMAKE_C_FLAGS "-Wall -Wextra")
set(CMAKE_C_FLAGS_DEBUG "-g -O0 -fsanitize=address -fno-omit-frame-pointer")
set(CMAKE_C_FLAGS_RELEASE "-Ofast -s -fno-ident  -march=native -flto -DNDEBUG")

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_C_STANDARD 11)

set(CMAKE_MODULE_PATH ${{CMAKE_MODULE_PATH}} "${{CMAKE_CURRENT_LIST_DIR}}")

add_definitions(-D_POSIX_C_SOURCE=200809L)
add_definitions(-D_DEFAULT_SOURCE)

include_directories(src deps/wrappers)

SET(SOURCES
    "src/main.c"
    )

add_executable({0} ${{SOURCES}})

if (CMAKE_BUILD_TYPE EQUAL Release)
    set_target_properties({0} PROPERTIES INTERPROCEDURAL_OPTIMIZATION TRUE POSITION_INDEPENDENT_CODE TRUE)
endif()

set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

target_link_libraries({0} rt Threads::Threads)

""".format(project_name))

    if os.path.exists(bin_path):
        print("{} already exists".format(bin_path))
    else:
        try:
            os.mkdir(bin_path)
        except OSError:
            print("failed to create folder")
            return

    if os.path.exists(src_path):
        print("{} already exists".format(src_path))
    else:
        try:
            os.mkdir(src_path)
        except OSError:
            print("failed to create folder")
            return

    if os.path.exists(main_path):
        print("{} already exists".format(main_path))
    else:
        with open(main_path, "w") as f:
            f.write("""#include <stdio.h>

int main(void) {
   puts("hello world");
   return 0;
}
""")

if __name__ == "__main__":
    #if you want to run this directly make sure to run it from the root of the repo
    #./src/skeleton.py /path/for/code
    if len(sys.argv) != 3:
        print("Please specify a path and a name")
    scaffold_skeleton(sys.argv[1], sys.argv[2])


