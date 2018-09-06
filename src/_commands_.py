"""
Helper file to cli.py, contains runnable commands to be mapped into memory

commands must follow the calling convention fn(Instance, ["arguments"]) and implement a __help__
attribute, which provides information on the command's use and purpose.
"""
import getopt
import subprocess
from os import environ

import templates

def help(instance, args):
    if args:
        for argv in args:
            if argv in instance.commands:
                print(argv + " - " + instance.commands[argv].__help__)

            else:
                print(argv + " - no such command ('help' to list)")
    
    else:
        for command in list(instance.commands.keys()):
            print(" * " + command)
        
        print("")

help.__help__ = "'help' to list commands, 'help [commands]' to get info on commands\n"

def package(instance, args):
    pass

package.__help__ = """manage packages
Usage:
  package <operation> [args]
"""

def sample(instance, args):
    pass

sample.__help__ = """manage samples
Usage:
  sample <operation> [args]
"""

def shell(insance, args):
    cmd = None

    if len(args):
        cmd = args
    else:
        cmd = [environ.get("SHELL", "sh")]

    try:
        subprocess.run(cmd)
    except subprocess.CalledProcessError as e:
        print("[!] - {}\n".format(e))

shell.__help__ = """pause acronym and access system shell
Usage:
  shell - enter live shell and resume when shell exits.
  shell [command] - execute [command] from shell and resume when command exits.
"""