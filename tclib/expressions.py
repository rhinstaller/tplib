import jinja2

def eval_str(expression, **kwargs):
    expression = "{{ %s }}" % expression
    template = jinja2.Template(expression)
    return template.render(**kwargs)

def eval_bool(expression, **kwargs):
    return eval_str(expression, **kwargs) == "True"
