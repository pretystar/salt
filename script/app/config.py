import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
import os
import sys
from pathlib import Path

config_folder = "\\config\\"

def read_config(config):
    #print("====:",sys.argv[0])
    #print("====:",os.path.dirname(__file__))
    #print(os.path.abspath(os.curdir))
    config_file = Path(os.path.dirname(__file__) +"\\..\\"+ config_folder + config + ".yaml")
    try:
        config_file_path = config_file.resolve()
    except FileNotFoundError as e:
        # not exist
        print(e)
    else:
        # Exist
        f = open(config_file_path)
        return yaml.load(f, Loader)