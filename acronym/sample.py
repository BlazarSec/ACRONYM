"""
Provides sample abstraction in memory and saving/loading samples to disk.
"""

import pickle
import subprocess
import os
from .logging import iprint, eprint, dprint, wprint, nprint
from .cmake import Cmake
from .skeleton import scaffold

class Sample():
    def __init__(self, name, path):
        self.name = name

        #normalize path to not duplicate such as ./name/name
        if os.path.basename(path).lower() != name.lower():
            path = os.path.join(path, name)
        self.path = path
        self.cmake = Cmake(name)

    # pickle self to file
    def pickle(self):
        with open(os.path.join(self.path, ".sample.pickle"), "wb") as f:
            pickle.dump(self, f)

    #(re)generate the cmake file
    def gen_cmake(self):
        cmake_path = os.path.join(self.path, "CMakeLists.txt")
        if os.path.exists(cmake_path):
            wprint("{} already exists, regenerating".format(cmake_path))
        else:
            iprint("creating file {}".format(cmake_path))
        with open(cmake_path, "w") as f:
            f.write(self.cmake.compile())

    #build the directory structure
    def gen_scaffold(self):
        scaffold(self.path, self.name)

    # build a string to use to display the currently selected sample
    # TODO indicate if changes need saving or not
    def prompt(self):
        return "[{}]".format(self.name)

# load pickled Sample by path
def unpickle_from(path):
    with open(path, "rb") as f:
        obj = pickle.load(f)
        t = type(obj)

        if t is Sample:
            return obj
        else:
            raise TypeError("Expected pickled Sample, found pickled {}".format(t))
