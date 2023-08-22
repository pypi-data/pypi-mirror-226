from command_cmd import command_cmd

def echo(text = False,options = False):
    return command_cmd(f'echo {text}',options)
