from pathlib import PurePath
from command_cmd import command_cmd


def mkdir(destination = False,obtions = False,debug=False):
    if (debug):
        print(destination,obtions)
    if (destination):
        destination = PurePath(destination)
        return command_cmd(f'mkdir {destination}',obtions)
    return False