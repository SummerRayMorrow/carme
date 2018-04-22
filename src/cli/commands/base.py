"""
Variables and Functions used by multiple CLI commands
"""
import os, subprocess, logging, ruamel.yaml

from os import path, pardir,getcwd

# Global Constants
CLI_DIR     =   path.abspath(path.join(path.dirname(__file__), pardir))
BASE_DIR    =   path.dirname(CLI_DIR)
DATA_DIR    =   path.join(BASE_DIR, 'data')
DOCKER_DIR  =   path.join(DATA_DIR, 'docker')
LAUNCH_DIR  =   path.join(DATA_DIR, 'launch_files')
NOTEBOOKS_DIR=  path.join(DATA_DIR, 'notebooks')
CWD=getcwd()


def get_project_root():
    """
    Traverses up until it finds the folder with `carme-config.yaml` in it.
    @return: The absolute path to the project root or None if not in a project
    """
    cd = os.getcwd()
    while not os.path.exists(os.path.join(cd, "carme-config.yaml")):
        if cd == "/":
            return None
        cd = os.path.dirname(cd)
    return os.path.abspath(cd)

def get_project_commands():
    """
    Gets the list of commands from the commands directory.
    @return: A commented list of the commands
    """
    ROOT_DIR=get_project_root()
    CARME_COMMANDS=os.path.join(ROOT_DIR, 'commands/carme-commands.yaml')
    if os.path.isfile(CARME_COMMANDS):
        commands=load_yaml(CARME_COMMANDS)
    else:
        print("No commands file found.")
        exit()
    return commands


def setup_logger():
    """
    Sets up logging
    """
    FORMAT = 'carme: [%(levelname)s] %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT)


def bash_command(command, syntax):
    try:
        print("Executing "+command+":\n", syntax)
        result= subprocess.call(syntax, shell=True, executable='/bin/bash')
        return result
    except subprocess.CalledProcessError as e:
        print("error")
    return(e.output.decode("utf-8"))

def get_config(ROOT_DIR):
    kwargs=load_yaml(os.path.join(ROOT_DIR, 'carme-config.yaml'))
    kwargs['root_dir']= ROOT_DIR
    kwargs['cwd']=os.getcwd()
    return kwargs

def load_yaml(file):
    try:
        with open(file, 'r') as yaml:
            kwargs=ruamel.yaml.round_trip_load(yaml, preserve_quotes=True)
        return kwargs
    except subprocess.CalledProcessError as e:
        print("error")
    return(e.output.decode("utf-8"))

def append_config(carme_config,file):
    if os.path.isfile(file):
        print('Adding configuration to carme-config.yaml.')
        kwargs=load_yaml(file)
        ruamel.yaml.round_trip_dump(kwargs, open(carme_config, 'a'))
        kwargs=load_yaml(carme_config)
    else:
        print('The configuration for the application ', app, 'is not available.' )

def update_config(carme_config,key,value):
    kwargs=load_yaml(carme_config)
    kwargs[key]=value
    ruamel.yaml.round_trip_dump(kwargs, open(carme_config, 'w'))
    kwargs=load_yaml(carme_config)
    return kwargs
