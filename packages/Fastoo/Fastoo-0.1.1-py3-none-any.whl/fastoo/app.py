from fastapi import FastAPI
from fastoo.api.file import get_folders

import importlib
import os 
import sys 

# from modules.auth.view import router as login_router   #new 

base_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_path)

def include_router(app):
    for module in get_folders("./modules"):
        module_view = importlib.import_module(f"modules.{module}.view")
        try:
            getattr(module_view, "router")
        except AttributeError:
            raise Exception(f"fastoo error> module {module} should contain a router")
        app.include_router(module_view.router, prefix="")  


def create_application():
    app = FastAPI()
    include_router(app)
    return app


app = create_application()