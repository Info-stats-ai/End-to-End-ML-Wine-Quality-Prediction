import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name="datascience"

list_of_files=[
    ".gthub/workflows/.gitkeep",
    # for the github actions 
    # .gitkeep is used for the deployment
    f"src/{project_name}/__init__.py",
    # for the initialization of the project
    # to import anywhere w are using __init__.py , 
    # so It acts like a pakage 
    f"src/{project_name}/components/__init__.py",
    # Enitre pipline is developed in one single folder or directory
    # which is our component folder
    # __init .py is for again to import it anywhere
    
    f"src/{project_name}/utils/__init__.py",
    #funcanality which is generic we use it  for that
    f"src/{project_name}/utils/common.py",
    # this utils folder have a file name common.py
    # which contain all the commaon fucntions that are used in the project
    f"src/{project_name}/config/__init__.py",
    
    f"src/{project_name}/config/configuration.py",
    # this config folder have a file name configuration.py
    # which contain all the configuration that are used in the project
    f"src/{project_name}/pipeline/__init__.py",
    # all the different piple , all the traning and testting or inferencing pipelines
    f"src/{project_name}/entity/__init__.py",
    
    f"src/{project_name}/entity/config_entity.py",
    f"src/{project_name}/constants/__init__.py",
    "config/config.yaml",# all config details are in this file
    "params.yaml",  # all params details are in this file
    "schema.yaml", # all schema details are in this file
    # I am using this yml file because it is easy to read and write
    # and it is easy to understand and it is in key value pair format
    "main.py",
    "Dockerfile",
    "setup.py",
    "research/research.ipynb",
    #
    "templates/index.html",
    "app.py"

]


for filepath in list_of_files:
    filepath=Path(filepath)
    filedir,filename=os.path.split(filepath)

    if filedir!="":
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"Creating directory {filedir} for the file : {filename}")
    
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath,"w") as f:

            pass
            logging.info(f"Creating empty file: {filepath}")

    else:
        logging.info(f"{filename} is already exists")
            

