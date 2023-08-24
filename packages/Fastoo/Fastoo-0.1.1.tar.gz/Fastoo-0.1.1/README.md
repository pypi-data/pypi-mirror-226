# fastoo

A powerful framework for dealing with FastAPI apps.

It includes various utilities for building big FastAPI apps, inclding templates and modules.

## Quickstart

-m means add default modules

```
python -m pip install fastoo==0.1.1
fastoo new blog -m
cd blog
uvicorn app:app --reload
```

### Configs

Define configuration profile in init (development, production, testing)

In your apps import get_settings from init


### Render templates 

consider this

```
.
├── api
│   ├── __init__.py
│   ├── module.py
│   └── templates.py
├── app.py
├── cli.py
├── config.py
├── __init__.py
├── init.py
├── modules
│   └── auth
│       ├── business.py
│       ├── models.py
│       ├── templates
│       │   └── abc.html
│       └── view.py
└── templates
    └── themes
        ├── back
        └── front
            └── dingy
                └── index.html
```

imports 

```python


from fastoo.api.module import Module

from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends

from typing import Annotated

from pydantic_settings import BaseSettings

from init import get_settings

```
If we set render_own_templates to True, render_template will look in a folder called templates in the mdoules folder 

```python

router = APIRouter(include_in_schema=False)
module = Module(__file__, render_own_templates=True)

@router.get("/login/")
def login(request: Request):
    with module.set(request) as m:
        return module.render_template("abc.html", {})
```

This can be overriden using 

```py
module = Module(__file__, render_own_templates=True, templates="custom/path")
```

If you don't want the whole goodies, just call


```py
from fastoo import render_template
...

    return render_template("template/path", {}, request, directory="custom/templates/path")
```

## Modules

Modules must contain info.toml like this

```toml
[base]
url_prefix = "/auth"
```