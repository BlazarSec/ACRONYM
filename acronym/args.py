import unittest
import os

#TODO add removing settings
def args_help():
    print('''symbol meaning:
    <filled by user>
    {list,of,possible,options}
    {m}inimum required option ie 'm' or 'minimum'
interface:
    <path>
    <path> {st}at
        -prints stats and cmake setup
    <path> [modifications, ...]
        {s}et {c3po, strip} {on, off}
        {a}dd {debug, release} {flag, define} <option>
        {a}dd <target>
        <target> {a}dd {f}ile <path>
        <target> {a}dd {l}ibrary <name>
        <target> {a}dd {i}nclude <path>
        <target> {a}dd {debug, release} {flag, define} <option>
        <target> {s}et {c3po, strip} {on, off}
    <path> {i}nit <name>
''')

class Args:
    def __init__(self, argv=[]):
        self.target = None
        # no args
        if len(argv) == 1:
            self.mode = "help"
            return

        if argv[1] in ['h', 'help']:
            self.mode = "help"
            return
        elif argv[1] in ['t', 'test']:
            self.mode = "test"
            return
        elif argv[1] in ['i','init']:
            if len(argv) == 4:
                self.mode = "init"
                self.name = argv[2]
                self.path = argv[3]
            else:
                self.mode = "help"
            return

        # if there was a path consume it
        if os.path.exists(argv[1]):
            self.path = argv[1]
            argv = argv[2:]
        else:
            argv = argv[1:]
            self.path = "./"

        # no args or stat requested
        if len(argv) == 0:
            self.mode = "stat"
            return

        # set c3po on
        if argv[0] in ['s', 'set']:
            if len(argv) != 3:
                self.mode = "help"
                return
            self.mode = "set"
            if argv[1] not in ['c', 'c3po', 's', 'strip']:
                self.mode = "help"
                return
            self.set = 'c3po' if argv[1] in 'c3po' else 'strip'
            if argv[2] not in ['on', 'off']:
                self.mode = "help"
                return
            self.state = (argv[2] == 'on')
        # ./ add debug flag -g
        elif argv[0] in ['a', 'add']:
            if len(argv) != 4:
                self.mode = "help"
                return
            self.mode = "add"
            if argv[1] not in ['d', 'debug', 'r', 'release']:
                self.mode = "help"
                return
            self.add = 'debug' if argv[1] in 'debug' else 'release'
            if argv[2] not in ['f', 'flag', 'd', 'define']:
                self.mode = "help"
                return
            self.type = 'flag' if argv[2] in 'flag' else 'define'
            self.option = argv[3]
        else:
            #handle target based configs
            if len(argv) == 1:
                self.mode = "help"
                return
            #check if arg.target
            self.target = argv[0]
            if len(argv) == 2:
                #target stat mode
                self.mode = "stat"
                return

            if argv[1] in ['s', 'set']:
                if len(argv) != 4:
                    self.mode = "help"
                    return
                self.mode = "set"
                if argv[2] not in ['c3po', 'strip']:
                    self.mode = "help"
                    return
                self.set = 'c3po' if argv[2] in ['c', 'c3po'] else 'strip'
                if argv[3] not in ['on', 'off']:
                    self.mode = "help"
                    return
                self.state = (argv[3] == 'on')
            elif argv[1] in ['a', 'add']:
                if len(argv) != 5:
                    self.mode = "help"
                    return
                self.mode = "add"
                if argv[2] not in ['d', 'debug', 'r', 'release']:
                    self.mode = "help"
                    return
                self.add = 'debug' if argv[2] in 'debug' else 'release'
                if argv[3] not in ['f', 'flag', 'd', 'define']:
                    self.mode = "help"
                    return
                self.type = 'flag' if argv[3] in 'flag' else 'define'
                self.option = argv[4]
            else:
                self.mode = "help"


class ArgsTest(unittest.TestCase):
    def test_help(self):
        a = Args(["test.py"])
        self.assertEquals(a.mode, "help")

        a = Args(["test.py", "help"])
        self.assertEquals(a.mode, "help")


    def test_stat(self):
        a = Args(["test.py", "./"])
        self.assertEquals(a.mode, "stat")

        a = Args(["test.py", "./", "not something useful"])
        self.assertEquals(a.mode, "help")


    def test_add(self):
        a = Args(["test.py", "a", "d", "f", "-g"])
        self.assertEquals(a.mode, "add")

        a = Args(["test.py", "a"])
        self.assertEquals(a.mode, "help")

        a = Args(["test.py", "add", "debug", "flag", "-g"])
        self.assertEquals(a.mode, "add")

        a = Args(["test.py", "add"])
        self.assertEquals(a.mode, "help")


    def test_set(self):
        a = Args(["test.py", "s", "c", "on"])
        self.assertEquals(a.mode, "set")

        a = Args(["test.py", "s"])
        self.assertEquals(a.mode, "help")

        a = Args(["test.py", "set", "c3po", "on"])
        self.assertEquals(a.mode, "set")

        a = Args(["test.py", "set"])
        self.assertEquals(a.mode, "help")
