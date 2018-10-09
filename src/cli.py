"""
The CLI must be able to load and run commands that operate on packages, samples, etc.
For this reason, commands are structured as functions indexed by string. When the user
desires to run a particular command, their command must be parsed into a string
representing the name of the desired command and a list of arg strings. Loaded commands
are then indexed with this name to find the desired function, which is then called and
supplied a reference to the CLI instance and the arg list. These functions also return an
integer status code, and implement the .help attribute, which is used to provide a short
snippet of the command's use and purpose.

By convention, supplementary packages to acronym.py which provide commands contain an acmd
module, which supplies a function load_into(), which is provided a reference to the CLI
instance. This is not mandated however, as loading any command must be explicitly performed.

Exceptions that are expected by commands should be handled internally or passed up to the
caller as RuntimeErrors, so that they can be caught by the caller in an except RuntimeError
block. Since RuntimeError is essentially never used by builtins, we're coopting it here for
use in place of a CalledCommandError. A FileNotFoundError expected by a commmand, for
example, should never be passed back to the caller, but could be excepted as fnf
and raised as RuntimeError(fnf).

The user's session must be able to break out of itself, so the input loop is owned by the
Instance class. A function is supplied as the loop_func attribute, and called in succession
while the looping attribute is set.
"""
class Instance():
    def __init__(self, loop=None):
        self.commands = {}
        self.looping = False
        self.loop_func = loop

    # bind a function to a name within the instance so that it can be invoked as a command.
    def load_cmd(self, name, func):
        if name in self.commands:
            raise ValueError("'{}' is already defined".format(name))

        self.commands[name] = func

    def start(self):
        self.looping = True

        while self.looping:
            self.loop_func()

    def stop(self):
        self.looping = False

    # run specified command with args
    def run(self, cmd, args):
        return self.commands[cmd](self, args)

# accept string and return list of parsed commands ready to be run
def cstrparse(raw):
    # determine split points to divide into command strings, ex. user supplies 'foo; bar'
    splits = [0]

    for idx, char in enumerate(raw):
        if char == ';' and (idx == 0 or raw[idx - 1] != '\\'):
            splits.append(idx)

    splits.append(None)
    cstrs = [raw[splits[i]:splits[i+1]] for i in range(len(splits) - 1)]

    # parse command strings into tuples of (command, args)

    cmds = []
    for cstr in cstrs:
        cstr = cstr.strip(" \n;")
        in_quote = False
        words = []

        # blocks of text wrapped in quotes should not be split
        for word in cstr.split(" "):
            if '"' in word and "\\\"" not in word:
                if in_quote:
                    in_quote = False
                    words[-1] += " " + word.replace('"', "")
                else:
                    in_quote = True
                    words.append(word.replace('"', ""))
                continue
            if in_quote:
                words[-1] += " " + word
            else:
                words.append(word)

        cmds.append((words[0], words[1:]))

    return cmds