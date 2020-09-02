import jinja2
import jinja2.nativetypes

def eval(expression, **kwargs):
    expression = "{{ %s }}" % expression
    template = jinja2.nativetypes.NativeTemplate(expression)
    return template.render(**kwargs)

def eval_str(expression, **kwargs):
    expression = "{{ %s }}" % expression
    template = jinja2.Template(expression)
    return template.render(**kwargs)

def eval_bool(expression, **kwargs):
    return bool(eval(expression, **kwargs))
