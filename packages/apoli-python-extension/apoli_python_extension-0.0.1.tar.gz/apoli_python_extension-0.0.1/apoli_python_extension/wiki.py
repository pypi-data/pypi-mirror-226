import shutil
import os
from git import Repo
from git import rmtree
from apoli_python_extension.generate_types import generate_types

def update_wiki():
    if os.path.exists("./wiki/"):
        rmtree('./wiki/')
    Repo.clone_from("https://github.com/apace100/origins-docs.git", "./wiki/")
    generate_types()
    rmtree('./wiki/')
    print("Wiki has successfully been updated!")

