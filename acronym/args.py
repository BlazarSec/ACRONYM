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
        <target>
            -first run creates new target
            -print stats and target specific setup
        <target> {a}dd {f}ile <path ...>
        <target> {a}dd {l}ibrary <names ...>
        <target> {a}dd {i}nclude <paths ...>
        <target> {a}dd {debug, release} {flag, define} <options ...>
        <target> {s}et {c3po, strip} {on, off}
    {i}nit <name> <path>
''')

class Args:
    def __init__(self, argv=[]):
        self.target = None
        # no args
        if len(argv) == 1:
            self.mode = "help"
            return

        #commands that prempt paths
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


        # no args
        if not argv:
            self.mode = "stat"
            return

        # global set
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
        # global add
        elif argv[0] in ['a', 'add']:
            if len(argv) < 4:
                self.mode = "help"
                return
            self.mode = "add"

            if argv[1] in ['d', 'debug', 'r', 'release'] and argv[2] in ['f', 'flag', 'd', 'define']:
                self.add = 'debug' if argv[1] in 'debug' else 'release'
                self.type = 'flag' if argv[2] in 'flag' else 'define'
                self.option = argv[3:]
            else:
                self.mode = "help"
                return
        else:
            #handle target based configs

            #check if arg.target
            self.target = argv[0]

            #target no args
            if len(argv) == 1:
                #target stat mode
                self.mode = "stat"
                return

            # target set
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

            # target add
            elif argv[1] in ['a', 'add']:
                if len(argv) < 4:
                    self.mode = "help"
                    return
                self.mode = "add"

                if argv[2] in ['d', 'debug', 'r', 'release'] and argv[3] in ['f', 'flag', 'd', 'define']:
                    self.add = 'debug' if argv[2] in 'debug' else 'release'
                    self.type = 'flag' if argv[3] in 'flag' else 'define'
                    self.option = argv[4:]
                    return

                elif argv[2] in ['f', 'file']:
                    self.add = 'file'
                elif argv[2] in ['l', 'library']:
                    self.add = 'library'
                elif argv[2] in ['i', 'include']:
                    self.add = 'include'

                else:
                    self.mode = "help"
                    return
                #files libs and includes all collect multiple args
                self.option = argv[3:]

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

        a = Args(["test.py", "./", "main"])
        self.assertEquals(a.mode, "stat")
        self.assertEquals(a.target, "main")


    def test_add(self):
        a = Args(["test.py", "a", "d", "f", "-g"])
        self.assertEquals(a.mode, "add")
        self.assertEquals(a.add, "debug")
        self.assertEquals(a.type, "flag")

        a = Args(["test.py", "a"])
        self.assertEquals(a.mode, "help")

        a = Args(["test.py", "add", "debug", "flag", "-g"])
        self.assertEquals(a.mode, "add")
        self.assertEquals(a.add, "debug")
        self.assertEquals(a.type, "flag")

        a = Args(["test.py", "add"])
        self.assertEquals(a.mode, "help")


    def test_set(self):
        a = Args(["test.py", "s", "c", "on"])
        self.assertEquals(a.mode, "set")
        self.assertEquals(a.set, "c3po")
        self.assertEquals(a.state, True)

        a = Args(["test.py", "s"])
        self.assertEquals(a.mode, "help")

        a = Args(["test.py", "set", "c3po", "off"])
        self.assertEquals(a.mode, "set")
        self.assertEquals(a.set, "c3po")
        self.assertEquals(a.state, False)

        a = Args(["test.py", "set"])
        self.assertEquals(a.mode, "help")
