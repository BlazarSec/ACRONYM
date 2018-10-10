"""
The live sample being worked upon is a member of the Sample class defined here, and
mainly serves as a wrapper over several Component members. Components have defined
interfaces that allow them to hand off data to eachother. Samples can be pickled and
unpickled, allowing users to save their work easily.
"""

import pickle

class Sample():
    def __init__(self, name="Untitled Sample"):
        self.name = name

def unpickle_from(path):
    pass

class Component():
    pass