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


