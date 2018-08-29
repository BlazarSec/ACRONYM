"""
Contains utils for mapping runnable commands into memory and execing commands from text input
"""

from inspect import getmembers, isfunction
from os import listdir

import templates

class Instance():
    # instantiate, loading initial packages
    def __init__(self, init_local_packages):
        # load initial packages, indexable by string
        # {"package_name": {"component_name": templates.Component}}
        packages = {}

        for package_dir in listdir(init_local_packages):
            loaded, errors = templates.load_pkgs("{}/{}".format(init_local_packages, package_dir))

            if errors:
                print("[!] One or more errors occurred loading {}:".format(package_dir))

                for e in errors:
                    print(" * " + e)

            packages[package_dir] = loaded

        self.packages = packages

        # load commands
        self.commands = { name: fn for name, fn in _loadcmds_() }

    # attempt to look up function in self.commands and run.
    # command should be a list of strings from line split by space, like ['example', 'arg']
    def try_run(self, command):
        if command[0] in self.commands:
            self.commands[command[0]](self, command[1:])
        else:
            print("[!] {} - no such command\n".format(command[0]))

# load commands from _commands_.py
def _loadcmds_():
    import _commands_

    for member in getmembers(_commands_):
        if isfunction(member[1]):
            yield member
