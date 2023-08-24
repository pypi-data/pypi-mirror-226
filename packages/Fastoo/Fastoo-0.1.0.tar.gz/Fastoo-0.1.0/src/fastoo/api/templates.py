from fastapi.templating import Jinja2Templates

def render_template(template_path, template_vars: dict, request, directory="templates"):
    templates = Jinja2Templates(directory=directory)
    template_vars.update({'request': request})
    return templates.TemplateResponse(template_path, template_vars)