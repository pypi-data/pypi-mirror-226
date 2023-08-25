import click 
import os 
import sys
from shutil import copytree
from shutil import ignore_patterns
from pathlib import Path
from fastoo import __version__
from string import Template

from fastoo.api.file import trymkfile
from fastoo.api.file import trymkdir

@click.group()
def cli():
    pass


@cli.command("new")
@click.argument("projname", required=False, default="")
@click.option("--verbose", "-v", is_flag=True, default=False)
@click.option("--modules", "-m", is_flag=True, default=False)
def new(projname, verbose, modules):
    modules_flag = modules
    src_fastoo = Path(__file__).parent.parent.absolute()
    here = os.getcwd()
    root_proj_path = os.path.join(here, projname)
    project_path = root_proj_path
    # copy the src/fastoo/ content to the new project
    copytree(
        src_fastoo,
        project_path,
        ignore=ignore_patterns(
            "__main__.py",
            "app.txt",
            "api",
            ".tox",
            ".coverage",
            "*.db",
            "coverage.xml",
            "setup.cfg",
            "instance",
            "migrations",
            "__pycache__",
            "*.pyc",
            "sphinx_source",
            "config.json",
            "pyproject.toml",
            "modules",
            "static",
        ),
    )

    if modules_flag:
        copytree(
            os.path.join(src_fastoo, "modules"),
            os.path.join(project_path, "modules"),
        )
    else:
        trymkdir(os.path.join(project_path, "modules"), verbose=verbose)

    trymkfile(
        os.path.join(root_proj_path, "requirements.txt"),
        f"fastoo=={__version__}\n")
    
    click.echo(f"✔️  Fastoo app <{projname}> created!")


@cli.command("module", help="Create new module")
@click.argument("name", required=False, default="")
@click.option("--verbose", "-v", is_flag=True, default=False)
def module(name, verbose):
    '''
    Create new module
    '''
    src_fastoo = Path(__file__).parent.parent.absolute()
    here = os.getcwd()

    # verify if in correct folder
    if not "app.py" in os.listdir(os.getcwd()):
        sys.exit("fastoo> Please use this command in the correct directory, missing app.py")
    if not "cli.py" in os.listdir(os.getcwd()):
        sys.exit("fastoo> Please use this command in the correct directory, missing cli.py")
    if not "config.py" in os.listdir(os.getcwd()):
        sys.exit("fastoo> Please use this command in the correct directory, missing config.py")
    
    # create modules folder if not there
    try:
        os.mkdir("modules")
    except:
        pass 

    # create new module
    ## create new folder
    module_path = os.path.join(here, "modules", name)
    trymkdir(module_path, verbose=verbose)
    ## create view.py
    trymkfile(
        os.path.join(module_path, "view.py"),"""
from fastoo import render_template
from fastoo.api.module import Module

from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends

from typing import Annotated

from pydantic_settings import BaseSettings

from init import get_settings


module = Module(__file__, render_own_templates=True)
router = APIRouter(prefix=module.url_prefix, include_in_schema=False)


@router.get("/")
def login(request: Request, settings: Annotated[BaseSettings, Depends(get_settings)]):
    with module.set(request) as m:
        return module.render_template("index.html", {"app_name": settings.app_name})
""")
    ## create business.py
    trymkfile(
    os.path.join(module_path, "business.py"),"""
""")
    ## create models.py
    trymkfile(
        os.path.join(module_path, "models.py"),"""
""")
    ## create info.toml
    trymkfile(
        os.path.join(module_path, "info.toml"),f"""
[base]
url_prefix = "/{name.lower()}"
""")
    ## create templates folder
    trymkdir(os.path.join(module_path, "templates"), verbose=verbose)
    ## create template index
    index_html = Template("""
Fastoo running successfully. <br>App name: $open app_name $close
""")
    index_html = index_html.substitute(open='{{',close='}}')
    trymkfile(
        os.path.join(os.path.join(module_path, "templates"), "index.html"), index_html)


    click.echo(f"✔️   Fastoo module <{name}> created!")



cli.add_command(new)
cli.add_command(module)