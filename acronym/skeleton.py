#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from .logging import iprint, eprint, dprint, wprint, reset_print

def contains_end(value, endings):
    for end in endings:
        if value.endswith(end):
            return True
    return False

def dirmake(path):
    if os.path.exists(path):
        wprint("{} already exists".format(path))
    else:
        iprint("creating folder {}".format(path))
        try:
            os.mkdir(path)
        except OSError:
            eprint("failed to create folder")
            return False
    return True

def scaffold(path, project_name, c3po=True):
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

    bin_path = os.path.join(path, "bin")
    dirmake(bin_path)
    src_path = os.path.join(path, "src")
    dirmake(src_path)


    if c3po:
        iprint("initializing blank c3po copies")
        c3po_path = os.path.join(path, "c3po")
        dirmake(c3po_path)
        gen_path = os.path.join(path, "gen")
        dirmake(gen_path)
        for file in [os.path.join(gen_path, file) for file in os.listdir(src_path) if os.path.isfile(os.path.join(src_path, file)) and (file.endswith(".c") or file.endswith(".h"))]:
            #create them blank
            open(file, 'a').close()

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
        reset_print()
        subprocess.call(['git', 'init', path])
