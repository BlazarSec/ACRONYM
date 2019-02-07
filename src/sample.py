"""
Provides sample abstraction in memory and saving/loading samples to disk.
"""

import pickle
import skeleton
import subprocess
import os
from logging import iprint, eprint, dprint, wprint, nprint

class Sample():
    def __init__(self, name, path):
        #self.core
        #self.modules
        self.include_dirs = []
        self.name = name
        if os.path.basename(path).lower() != name.lower():
            path = os.path.join(path, name)
        self.path = path
        self.targets = []
        self.constants = []

    # pickle self to file
    def pickle(self):
        with open(os.path.join(self.path, ".sample.pickle"), "wb") as f:
            pickle.dump(self, f)

    # just register another path to be included in the cmake
    def add_local_dir(self, path):
        self.include_dirs.append(path)

    def add_git_repo(self, url):
        output = subprocess.getoutput("cd {}; git clone --recursive {}".format(os.path.join(self.path, "deps"), url))
        lines = output.splitlines()
        repo = lines[0].split("'")[1]
        repopath = os.path.join(self.path, "deps", repo)

        nprint(output)

        self.add_local_dir(repopath)


    # pass in all the required args from the sample to the cmakebuilder for further parsing
    def cmake(self):
        cmakestr = skeleton.build_cmakelists(os.path.join(self.path, "src"), self.include_dirs, self.name, self.targets, self.constants)
        cmake_path = os.path.join(self.path, "CMakeLists.txt")
        if os.path.exists(cmake_path):
            wprint("{} already exists".format(cmake_path))
        else:
            iprint("creating file {}".format(cmake_path))
            with open(cmake_path, "w") as f:
                f.write(cmakestr)

    def scaffold(self):
        skeleton.scaffold_skeleton(self.path, self.name, cmake=False)

    # build a string to use to display the currently selected sample
    # TODO indicate if changes need saving or not
    def prompt(self):
        return "[{}]".format(self.name)

class RAT(Sample):
    def __init__(self, name, path, host):
        super().__init__(name, path)
        self.constants.append(host)


# load pickled Sample by path
def unpickle_from(path):
    with open(path, "rb") as f:
        obj = pickle.load(f)
        t = type(obj)

        if t is Sample:
            return obj
        else:
            raise TypeError("Expected pickled Sample, found pickled {}".format(t))
