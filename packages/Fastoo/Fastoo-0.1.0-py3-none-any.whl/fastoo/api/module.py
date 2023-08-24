import os
from fastoo.api.templates import render_template
from fastoo.api.verify import verify_module

class ReqMan:
    def __init__(self, module, request):
        self.module = module
        self.module.request = request

    def __enter__(self):
        return self.module 

    def __exit__(self, type, value, traceback):
        self.module.request = None

class Module:
    def __init__(self, path, templates="templates", render_own_templates=False):
        '''
        path: __file__
        '''
        self.path = path
        self.request = None
        self.base_dir = os.path.dirname(os.path.abspath(path))
        self.info_toml_path = os.path.join(self.base_dir, "info.toml")

        if render_own_templates:
            self.templates = os.path.join(self.base_dir, templates)
        else:
            self.templates = templates 

        info = verify_module(self)

        self.url_prefix = info["base"]["url_prefix"]


    def set(self, request):
        return ReqMan(self, request)
    
    def render_template(self, path, template_vars):
        if self.request is None:
            raise Exception("Please call <with module.set(request) as m:> to set the current request")
        
        print(self.templates)
        return render_template(path, template_vars, self.request, directory=self.templates)
        
    
