"""
Provides sample abstraction in memory and saving/loading samples to disk.
"""

import pickle

class Sample():
    def __init__(self):
        #self.core
        #self.modules
        pass

    # pickle self to file
    def pickle_to(self, path):
        with open(path, "w") as f:
            pickle.dump(self, f)

    # build C source code at path
    def build_to(self, path):
        pass

# load pickled Sample by path
def unpickle_from(path):
    with open(path, "r") as f:
        obj = pickle.load(f)
        t = type(obj)

        if t is Sample:
            return Sample

        else:
            raise TypeError("Expected pickled Sample, found pickled {}".format(t))
