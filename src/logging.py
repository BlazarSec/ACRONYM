from __future__ import print_function
import sys
import enum
from colorama import Fore, Style

#TODO on windows colorama needs to run its init function for additional sanitization

class LogLevels(enum.Enum):
    DEBUG = 0
    INFO = 1
    ERROR = 2

# these are filewide but the functionality is global so its a fair trade
logging_out_file = sys.stdout
logging_error_file = sys.stderr
logging_level = LogLevels.DEBUG

# only printed in debug mode, ie very verbose
# debug
def dprint(*args, **kwargs):
    if logging_level == LogLevels.DEBUG:
        print(Fore.YELLOW + "[?] ",file=logging_out_file, end='')
        print(*args, file=logging_out_file, **kwargs)

# printed in info mode or higher, ie verbose
# info
def iprint(*args, **kwargs):
    if logging_level == LogLevels.DEBUG or logging_level == LogLevels.INFO:
        print(Fore.CYAN + "[i] ",file=logging_out_file, end='')
        print(*args, file=logging_out_file, **kwargs)
# warn
def wprint(*args, **kwargs):
    if logging_level == LogLevels.DEBUG or logging_level == LogLevels.INFO:
        print(Fore.BLUE + "[i] ",file=logging_out_file, end='')
        print(*args, file=logging_out_file, **kwargs)

# printed in all modes
# thanks marc for the idea https://stackoverflow.com/a/14981125
# error
def eprint(*args, **kwargs):
    print(Fore.RED + "[!] ",file=logging_error_file, end='')
    print(*args, file=logging_error_file, **kwargs)

#normal print to ensure the colors dont carry over
def nprint(*args, **kwargs):
    print(Fore.RESET, end='')
    print(*args)

def reset_print():
    print(Style.RESET_ALL)
