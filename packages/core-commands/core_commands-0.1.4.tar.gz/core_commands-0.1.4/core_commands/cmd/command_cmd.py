from subprocess import run

def command_cmd(command_,options):
        #TODO: deberia verificar que si el sistema es windows.
        if (options):
            return run(f'{command_}',options,shell=True) 
        return run(f'{command_}',shell=True)