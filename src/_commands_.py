"""
Helper file to cli.py, contains runnable commands to be mapped into memory

commands must follow the calling convention fn(Instance, ["arguments"]) and implement a __help__
attribute, which provides information on the command's use and purpose.
"""
import getopt

import templates

def help(instance, args):
    if args:
        for argv in args:
            if argv in instance.commands:
                print(argv + " - " + instance.commands[argv].__help__, end="\n\n")

            else:
                print(argv + " - no such command")
    
    else:
        for command in list(instance.commands.keys()):
            print(" * " + command)

help.__help__ = "'help' to list commands, 'help [commands]' to get info on commands"