from os import listdir
from os.path import dirname, realpath

import templates

class Instance():
    # instantiate, loading initial packages from 
    def __init__(self, init_local_packages=dirname(realpath(__file__))+"/../packages"):
        # loaded packages go here, indexable by string
        # indexed objects are maps of {"name": templates.Component}
        packages = {}
        print("DEBUG: LOADED @ {}".format(init_local_packages))

        for package_dir in listdir(init_local_packages):
            loaded, errors = templates.load_from(package_dir)

            if errors:
                print("[!] One or more errors occurred loading {}:".format(package_dir))

                for e in errors:
                    print(" * " + e)

            packages[package_dir] = loaded

        self.packages = packages