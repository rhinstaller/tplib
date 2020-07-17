import functools
from . import Mapping as m
from .data_object import DataObject, DocumentObject, ListObject

class Instruction(DataObject):
    default_result = 'Success'
    mapping = dict((
        m('step'),
        m('result', required=False, default=default_result, allowed_types=str),
    ))
    def feed(self, data):
        if isinstance(data, str):
            data = {'step' : data, 'result' : self.default_result}
        return self._autofeed(data)


class Phase(ListObject):
    def __init__(self, name, data):
        self.name = name
        super().__init__(data)


    def feed(self, data):
        if not isinstance(data, list):
            raise TypeError('Phase "%s" contains invalid data. List type was expected.' % self._name)
        self.data = [ Instruction(item) for item in data ]
        data.clear()


class Instructions(DataObject):
    mapping = dict((
        m('setup', required=False, default=[],
          func=functools.partial(Phase, 'setup'),
        ),
        m('steps', func=functools.partial(Phase, 'steps')),
        m('teardown', required=False, default=[],
          func=functools.partial(Phase, 'teardown')
        ),
    ))


class TestCase(DocumentObject):
    mapping = dict((
        m('name'),
        m('description'),
        m('priority', allowed_types=int),
        m('execution', allowed_types=dict),
        m('filter', required=False, default=(), func=list),
        m('instructions', func=Instructions),
        m('configurations', required=False, default=None, allowed_types=(list,type(None))),
        m('author', required=False),
        m('tags', required=False, default=(), func=set)
    ))
    runtime_properties = [
        'verifiesRequirement',
    ]

    def __init__(self, data, library=None, basedir=None, possible_parents=None):
        super().__init__(data, library=library, basedir=basedir, possible_parents=possible_parents)
        self.verifiesRequirement = []

    @property
    def id(self):
        return self.name

    def __hash__(self):
        return hash((type(self), self._name, id(self.library)))

    def __eq__(self, other):
        if type(self) != type(other):
            return NotImplemented
        if self.data != other.data:
            return False
        if { req.id for req in self.verifiesRequirement } != { req.id for req in other.verifiesRequirement }:
            return False
        return True
