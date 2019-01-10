#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess

def build_cmakelists(src_path, include_dirs, project_name):
    src_str = "    \n".join("\"src/" + f + "\"" for f in os.listdir(src_path) if os.path.isfile(os.path.join(src_path,f)) and f.endswith(".c"))

    include_str = "src"
    if len(include_dirs) > 0:
        include_dirs += " " + " ".join(include_dirs)

    return """cmake_minimum_required (VERSION 3.0)
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

include_directories({1})

SET(SOURCES
    {2}
    )

add_executable({0} ${{SOURCES}})

if (CMAKE_BUILD_TYPE EQUAL Release)
    set_target_properties({0} PROPERTIES INTERPROCEDURAL_OPTIMIZATION TRUE POSITION_INDEPENDENT_CODE TRUE)
endif()

set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

target_link_libraries({0} rt Threads::Threads)

""".format(project_name, include_str, src_str)

def scaffold_skeleton(base_path, project_name):
    path = base_path
    if os.path.basename(base_path).lower() != project_name.lower():
        path = os.path.join(base_path, project_name)
        print("using fullpath {}".format(path))

    if not os.path.exists(path):
        print("creating folder {}".format(path))
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
    git_path = os.path.join(path, ".git")
    main_path = os.path.join(path, "src", "main.c")

    if os.path.exists(gitignore_path):
        print("{} already exists".format(gitignore_path))
    else:
        print("creating file {}".format(gitignore_path))
        with open(gitignore_path, "w") as f:
            f.write("bin/")

    if os.path.exists(bin_path):
        print("{} already exists".format(bin_path))
    else:
        print("creating folder {}".format(bin_path))
        try:
            os.mkdir(bin_path)
        except OSError:
            print("failed to create folder")
            return

    if os.path.exists(src_path):
        print("{} already exists".format(src_path))
    else:
        print("creating folder {}".format(src_path))
        try:
            os.mkdir(src_path)
        except OSError:
            print("failed to create folder")
            return

    if os.path.exists(main_path):
        print("{} already exists".format(main_path))
    else:
        print("creating file {}".format(main_path))
        with open(main_path, "w") as f:
            f.write("""#include <stdio.h>

int main(void) {
   puts("hello world");
   return 0;
}
""")
    if os.path.exists(git_path):
        print("{} already exists".format(git_path))
    else:
        subprocess.call(['git', 'init', path])

    #call the cmake generator last
    if os.path.exists(cmake_path):
        print("{} already exists".format(cmake_path))
    else:
        print("creating file {}".format(cmake_path))
        with open(cmake_path, "w") as f:
            f.write(build_cmakelists(src_path, [], project_name))


if __name__ == "__main__":
    #if you want to run this directly make sure to run it from the root of the repo
    #./src/skeleton.py /path/for/code
    if len(sys.argv) != 3:
        print("Please specify a path and a name")
    scaffold_skeleton(sys.argv[1], sys.argv[2])


