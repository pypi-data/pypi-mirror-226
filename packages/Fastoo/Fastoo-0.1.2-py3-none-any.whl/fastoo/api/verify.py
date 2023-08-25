import toml
import os 
from fastoo.api.file import path_exists

def verify_module(module):
    toml_content = None 

    if not path_exists(module.info_toml_path):
        raise Exception(f"fastoo-error> module should contain info.toml file for module {module.path}")
    
    with open(module.info_toml_path) as f:
        toml_content = toml.load(f)

    if "base" not in toml_content:
        raise Exception(f"fastoo-error> info.toml should contain a section named [base] for module {module.path}")
    
    try:
        toml_content["base"]["url_prefix"]
    except KeyError:
        raise Exception(f'fastoo-error> [base] section in info.toml should contain url_prefix="/path" for module {module.path}')
    
    # if not toml_content["base"]["url_prefix"].strip():
    #     raise Exception(f"fastoo-error> [base] -> url_prefix cannot be empty for module {module.path}")
    
    return toml_content
