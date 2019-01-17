"""
Provides sample abstraction in memory and saving/loading samples to disk.
"""

import pickle
import skeleton
import os

class Sample():
    def __init__(self, name, path):
        #self.core
        #self.modules
        self.include_dirs = []
        self.name = name
        if os.path.basename(path).lower() != name.lower():
            path = os.path.join(path, name)
        self.path = path

    # pickle self to file
    def pickle(self):
        with open(os.path.join(self.path, ".sample.pickle"), "wb") as f:
            pickle.dump(self, f)

    # just register another path to be included in the cmake
    def add_local_dir(self, path):
        include_dirs.append(path)

    # build C source code at path
    # path is the project root
    def build_to(self, path):
        skeleton.build_cmakelists()

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
