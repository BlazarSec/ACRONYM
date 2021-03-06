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
    # load pickled Sample by path
    def unpickle_from(path, name=""):
        actual_path = Sample.pickle_path(Sample.sample_path(path, name))
        if os.path.exists(actual_path):
            with open(actual_path, "rb") as f:
                obj = pickle.load(f)
                t = type(obj)
                if t is Sample:
                    return obj
                else:
                    raise TypeError(f"Expected pickled Sample, found pickled {t}")

    #normalize path to not duplicate such as ./name/name
    def sample_path(path, name):
        if os.path.basename(path).lower() != name.lower():
            path = os.path.join(path, name)
        return path

    def pickle_path(path):
        return os.path.join(path, ".sample.pickle")

    def __init__(self, path, name, c3po=True, **kwargs):
        self.name = name
        self.c3po = c3po

        self.path = Sample.sample_path(path, name)
        #pass any unconsumed args through to cmake
        self.cmake = Cmake(name, c3po=self.c3po, **kwargs)

    # pickle self to file
    def pickle(self):
        with open(Sample.pickle_path(self.path), "wb") as f:
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
        scaffold(self.path, self.name, c3po=self.c3po)

