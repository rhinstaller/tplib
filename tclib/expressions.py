import jinja2
import jinja2.nativetypes

def compile_native(expression):
    expression = "{{ %s }}" % expression
    return jinja2.nativetypes.NativeTemplate(expression).render

def eval(expression, **kwargs):
    return compile_native(expression)(**kwargs)

def compile_str(expression):
    expression = "{{ %s }}" % expression
    return jinja2.Template(expression).render

def eval_str(expression, **kwargs):
    return compile_str(expression)(**kwargs)

def compile_bool(expression):
    render_func = compile_native(expression)
    return lambda **kwargs: bool(render_func(**kwargs))

def eval_bool(expression, **kwargs):
    return compile_bool(expression)(**kwargs)
