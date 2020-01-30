import functools
from . import Mapping as m
from .data_object import DataObject, DocumentObject, ListObject

class Instruction(DataObject):
    default_result = 'Success'
    mapping = dict((
        m('step'),
        m('result', required=False, default='', allowed_types=str),
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
        m('filter', allowed_types=list),
        m('instructions', func=Instructions),
        m('configurations', required=False, default=None, allowed_types=(list,type(None))),
        m('author', required=False),
        m('tags', required=False, default=[], func=set)
    ))
    runtime_properties = [
        'verifiesRequirement',
    ]

    def __init__(self, data, parent=None, library=None):
        super().__init__(data, parent, library)
        self.verifiesRequirement = []

    @property
    def id(self):
        return self.name
