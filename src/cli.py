from os.path import dirname, realpath

import templates

class Instance():
    def __init__(self, init_local_packages=dirname(realpath(__file__))+"/../packages"):
        # loaded packages go here, indexable by string
        # indexed objects are strings mapped to templates.py component objects
        self.packages = {}
        print("DEBUG: LOADED @ {}".format(init_local_packages))

        