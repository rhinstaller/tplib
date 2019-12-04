from . import Mapping as m
from .data_object import DataObject

class Instruction(DataObject):
    pass

class Phase(DataObject):
    pass

class Instructions(DataObject):
    mapping = dict((
        m('setup', required=False, default=[], allowed_types=list),#, func=Phase),
        m('steps', allowed_types=list),#, func=Phase),
        m('teardown', required=False, default=[], allowed_types=list),#, func=Phase),
    ))

class TestCase(DataObject):
    mapping = dict((
        m('name'),
        m('description'),
        m('priority', allowed_types=int),
        m('execution', allowed_types=dict),
        m('filter', allowed_types=list),
        m('instructions', func=Instructions),
        m('configurations', inherited=True, allowed_types=list),
        m('author', required=False),
        m('tags', required=False, default=[], func=set)
    ))
