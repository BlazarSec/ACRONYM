import unittest
import os

#TODO add removing settings
'''
symbol meaning:
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
'''

class Args:
    def __init__(self, argv=[]):
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

        if argv[0] in ['i','init']:
            if len(argv) == 2:
                self.mode = "init"
                self.name = argv[1]
            else:
                self.mode = "help"
        # set c3po on
        elif argv[0] in ['s', 'set']:
            if len(argv) != 3:
                self.mode = "help"
                return
            self.mode = "set"
            #TODO implement set options
        # ./ add debug flag -g
        elif argv[0] in ['a', 'add']:
            if len(argv) != 4:
                self.mode = "help"
                return
            self.mode = "add"
            #TODO implement add options
        else:
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
                self.mode = "set"
            elif argv[1] in ['a', 'add']:
                self.mode = "add"
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
