import click 
import os 
from shutil import copytree
from shutil import ignore_patterns
from pathlib import Path
from fastoo import __version__

from fastoo.api.file import trymkfile

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

    trymkfile(
        os.path.join(root_proj_path, "requirements.txt"),
        f"fastoo=={__version__}\n")


cli.add_command(new)