import subprocess
from os import environ

def load_into(instance):
    for name, cmd in [
        ("help", help),
        ("exit", exit),
        ("shell", shell)
    ]:
        instance.load_cmd(name, cmd)

# end instance loop. TODO save / clean up.
def exit(instance, args):
    instance.stop()

exit.help = "exits the session."

# get information on available commands by listing instance.command keys or finding func's .help attribute.
def help(instance, args):
    if len(args):
        for cmd in args:
            try:
                print(f"{cmd} -\n{instance.commands[cmd].help}\n")

            except AttributeError:
                raise RuntimeError(f"The author of '{cmd}' has not provided helper info for the requested command.")

            except KeyError:
                raise RuntimeError(f"'{cmd}' not found")
    else:
        print("Available commands:")

        for cmd in instance.commands:
            print(" * " + cmd)

        print("")

    return 0

help.help = "list available commands.\nsupply 1 or more args to instead receive a brief summary of those commands."

# access system shell either for temporary session or single command.
def shell(instance, args):
    try:
        subprocess.run(args if len(args) else [environ.get("SHELL", "sh")])
    except subprocess.CalledProcessError as e:
        raise RuntimeError(e)

shell.help = "enter system shell and resume when shell exits.\nif one or more arguments are specified as <command> [args], shell will exit when command is done."