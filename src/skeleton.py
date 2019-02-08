#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import logging
from logging import iprint, eprint, dprint, wprint

def contains_end(value, endings):
    for end in endings:
        if value.endswith(end):
            return True
    return False

def build_cmakelists(src_path, include_dirs, project_name, targets=[], constants=[], endings=[".c"]):
    src_files = [f for f in os.listdir(src_path) if os.path.isfile(os.path.join(src_path,f)) and contains_end(f,endings)]

    if len(targets) > 0:
        #remove the files that are containing the mains for the additional targets
        for file in src_files:
            for target in targets:
                if file.startswith(target):
                    src_files.remove(file)
                    #TODO track which file is removed to support more than just c
                    #also check to make sure its just the name + the ending

    src_str = "    \n".join("\"src/" + f + "\"" for f in src_files)

    include_str = "src"

    if len(include_dirs) > 0:
        include_str += " " + " ".join(include_dirs)

    targetstr = "\n".join(targettemplate.format(t) for t in targets) if len(targets) > 0 else simpletargettemplate.format(project_name)

    definitionstr = "add_definitions({})".format(" ".join("-D{}".format(s) for s in constants)) if len(constants) > 0 else ""

    return maintemplate.format(project_name,
                               include_str,
                               definitionstr,
                               targetstr,
                               src_str)



def scaffold_skeleton(path, project_name, git_init=True, folder_init=True, cmake=True):
    #handle people creating a folder for the name of their project before calling the tool
    iprint("using fullpath {}".format(path))

    if not os.path.exists(path):
        iprint("creating folder {}".format(path))
        try:
            os.mkdir(path)
        except OSError:
            eprint("failed to create folder")
            return
    elif not os.path.isdir(path):
        iprint("path is taken by a non folder")
    else:
        wprint("folder already exists")

    if folder_init:
        bin_path = os.path.join(path, "bin")
        src_path = os.path.join(path, "src")
        deps_path = os.path.join(path, "deps")
        if os.path.exists(bin_path):
            wprint("{} already exists".format(bin_path))
        else:
            iprint("creating folder {}".format(bin_path))
            try:
                os.mkdir(bin_path)
            except OSError:
                eprint("failed to create folder")
                return

        if os.path.exists(src_path):
            wprint("{} already exists".format(src_path))
        else:
            iprint("creating folder {}".format(src_path))
            try:
                os.mkdir(src_path)
            except OSError:
                eprint("failed to create folder")
                return

        if os.path.exists(deps_path):
            wprint("{} already exists".format(deps_path))
        else:
            iprint("creating folder {}".format(deps_path))
            try:
                os.mkdir(deps_path)
            except OSError:
                eprint("failed to create folder")
                return

    if git_init:
        gitignore_path = os.path.join(path, ".gitignore")
        git_path = os.path.join(path, ".git")
        if os.path.exists(gitignore_path):
            wprint("{} already exists".format(gitignore_path))
        else:
            iprint("creating file {}".format(gitignore_path))
            with open(gitignore_path, "w") as f:
                f.write("bin/")
        if os.path.exists(git_path):
            wprint("{} already exists".format(git_path))
        else:
            logging.reset_print()
            subprocess.call(['git', 'init', path])

    #call the cmake generator last
    if cmake:
        cmake_path = os.path.join(path, "CMakeLists.txt")
        if os.path.exists(cmake_path):
            wprint("{} already exists".format(cmake_path))
        else:
            iprint("creating file {}".format(cmake_path))
            with open(cmake_path, "w") as f:
                f.write(build_cmakelists(src_path, [], project_name))


if __name__ == "__main__":
    #if you want to run this directly make sure to run it from the root of the repo
    #./src/skeleton.py /path/for/code
    if len(sys.argv) != 3:
        eprint("Please specify a path and a name")
        sys.exit(1)
    scaffold_skeleton(sys.argv[1], sys.argv[2])


class Cmake():
    def __init__(self, name):
        self.name = '_'.join(name.split())
        self.targets = []
        self.debug_flags = []
        self.debug_defines = {}
        self.release_flags = []
        self.release_defines = {}

    def add_debug_define(self, key, value):
        self.debug_defines[key] = value

    def add_release_define(self, key, value):
        self.release_defines[key] = value

    def add_debug_flags(self, flags):
        if isinstance(flags, (list,)):
            for flag in flags:
                self.debug_flags.append(flag)
        else:
            self.debug_flags.append(flags)

    def add_release_flags(self, flags):
        if isinstance(flags, (list,)):
            for flag in flags:
                self.debug_flags.append(flag)
        else:
            self.debug_flags.append(flags)

    def add_target(self, name):
        self.targets.append(Target(name))
        return self.targets[-1]

    def __str__(self):
        cmakelines = ["""#autogenerated by ACRONYM
#changes should be done through the utility to avoid overwrites

cmake_minimum_required(VERSION 3.9.0)
project({0})

#default to release
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "" FORCE)
endif()

#clear defaults
set(CMAKE_C_FLAGS_DEBUG "")
set(CMAKE_C_FLAGS_RELEASE "")

#set some standards
set(CMAKE_C_STANDARD 11)
add_definitions(-D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE)

#ensure IPO and LTO is avalible
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_LINK_WHAT_YOU_USE ON)
include(CheckIPOSupported)
check_ipo_supported(RESULT ipo_supported OUTPUT error)
if(ipo_supported)
    set(CMAKE_INTERPROCEDURAL_OPTIMIZATION_RELEASE ON)
else()
    message(STATUS "IPO / LTO not supported: <${{error}}>")
endif()

#update/pull git submodules
find_package(Git QUIET)
if(GIT_FOUND AND EXISTS "${{PROJECT_SOURCE_DIR}}/.git")
# Update submodules as needed
    option(GIT_SUBMODULE "Check submodules during build" ON)
    if(GIT_SUBMODULE)
        message(STATUS "Submodule update")
        execute_process(COMMAND ${{GIT_EXECUTABLE}} submodule update --init --recursive
                        WORKING_DIRECTORY ${{CMAKE_CURRENT_SOURCE_DIR}}
                        RESULT_VARIABLE GIT_SUBMOD_RESULT)
        if(NOT GIT_SUBMOD_RESULT EQUAL "0")
            message(FATAL_ERROR "git submodule update --init failed with ${{GIT_SUBMOD_RESULT}}, please checkout submodules")
        endif()
    endif()
endif()
""".format(self.name)]

        if len(self.debug_defines) > 0:
            targetlines.append("set(DEBUG_DEFINES {})".format(' '.join("\"-D{}={}\"".format(k,v) for k,v in self.debug_defines.items())))

        if len(self.release_defines) > 0:
            targetlines.append("set(RELEASE_DEFINES {})".format(' '.join("\"-D{}={}\"".format(k,v) for k,v in self.release_defines.items())))

        cmakelines.append("add_definitions(\"$<$<CONFIG:RELEASE>:${RELEASE_DEFINES}>\" \"$<$<CONFIG:DEBUG>:${DEBUG_DEFINES}>\")")

        for target in self.targets:
            cmakelines.append("")
            cmakelines.append(str(target))

        cmakelines.append("")
        return '\n'.join(cmakelines)


class Target():
    def __init__(self, name, strip=True):
        self.name = '_'.join(name.split())
        #TODO add the post build strip dependancy
        self.strip = strip
        self.files = []
        self.libraries= []
        self.includes = []
        self.debug_flags = []
        self.debug_defines = {}
        self.release_flags = []
        self.release_defines = {}

    def add_debug_define(self, key, value):
        self.debug_defines[key] = value

    def add_release_define(self, key, value):
        self.release_defines[key] = value

    def add_debug_flags(self, flags):
        if isinstance(flags, (list,)):
            for flag in flags:
                self.debug_flags.append(flag)
        else:
            self.debug_flags.append(flags)

    def add_release_flags(self, flags):
        if isinstance(flags, (list,)):
            for flag in flags:
                self.debug_flags.append(flag)
        else:
            self.debug_flags.append(flags)

    def add_library(self, library):
        self.libraries.append(library)

    def add_file(self, file):
        self.files.append(file)

    def add_include(self, include):
        self.includes.append(include)

    def __str__(self):
        targetlines = ["#{} specific configuration".format(self.name)]

        targetlines.append("set({}_SOURCES\n    {})".format(self.name, '    \n'.join("\"{}\"".format(file) for file in self.files) if len(self.files) > 0 else ""))

        targetlines.append("add_executable({0} ${{{0}_SOURCES}})".format(self.name))

        if len(self.debug_flags) > 0:
            targetlines.append("set({}_DEBUG {})".format(self.name, ' '.join(debug for debug in self.debug_flags)))

        if len(self.release_flags) > 0:
            targetlines.append("set({}_RELEASE {})".format(self.name, ' '.join(release for release in self.release_flags)))

        if len(self.debug_defines) > 0:
            targetlines.append("set({}_DEBUG_DEFINES {})".format(self.name, ' '.join("\"-D{}={}\"".format(k,v) for k,v in self.debug_defines.items())))

        if len(self.release_defines) > 0:
            targetlines.append("set({}_RELEASE_DEFINES {})".format(self.name, ' '.join("\"-D{}={}\"".format(k,v) for k,v in self.release_defines.items())))

        if len(self.includes) > 0:
            targetlines.append("target_include_directories({} PUBLIC {})".format(self.name, ' '.join(include for include in self.includes)))

        if len(self.libraries) > 0:
            targetlines.append("target_link_libraries({} PRIVATE {})".format(self.name, ' '.join(library for library in self.libraries)))

        targetlines.append("target_compile_options({0} PRIVATE \"$<$<CONFIG:RELEASE>:${{{0}_RELEASE}}>\" \"$<$<CONFIG:DEBUG>:${{{0}_DEBUG}}>\")".format(self.name))

        targetlines.append("target_compile_definitions({0} PRIVATE \"$<$<CONFIG:RELEASE>:${{{0}_RELEASE_DEFINES}}>\" \"$<$<CONFIG:DEBUG>:${{{0}_DEBUG_DEFINES}}>\")".format(self.name))

        return "\n".join(targetlines)
