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
    def __init__(self, name, data, document):
        self.name = name
        super().__init__(data, document=document)


    def feed(self, data):
        if not isinstance(data, list):
            raise TypeError('%s: Phase "%s" contains invalid data. List type was expected.' % (self.document.filename, self._name))
        self._data = [ Instruction(item, library=self.library, document=self.document) for item in data ]
        data.clear()

class SetupPhase(Phase):
    def __init__(self, data, document):
        super().__init__("setup", data, document)

class StepsPhase(Phase):
    def __init__(self, data, document):
        super().__init__("steps", data, document)

class TeardownPhase(Phase):
    def __init__(self, data, document):
        super().__init__("teardown", data, document)

class Instructions(DataObject):
    mapping = dict((
        m('setup', required=False, default=[], func=SetupPhase),
        m('steps', func=StepsPhase),
        m('teardown', required=False, default=[], func=TeardownPhase),
    ))

class Execution(DataObject):
    mapping = dict((
        m('type'),
        m('automation_data', required=False, allowed_types=(object,)),
    ))

class TestCase(DocumentObject):
    mapping = dict((
        m('name'),
        m('description'),
        m('priority', allowed_types=int),
        m('components', required=False, default=(), func=list),
        m('execution', func=Execution),
        m('filter', required=False, default=(), func=list),
        m('instructions', func=Instructions),
        m('configurations', required=False, default=None, allowed_types=(list,type(None))),
        m('author', required=False),
        m('tags', required=False, default=(), func=set)
    ))
    runtime_properties = [
        'verifiesRequirement',
    ]

    def __init__(self, filename, override_data=None, library=None, basedir=None, possible_parents=None):
        super().__init__(filename, override_data=override_data, library=library, basedir=basedir, possible_parents=possible_parents)
        self.verifiesRequirement = []

    @property
    def id(self):
        return self.name

    def __hash__(self):
        return hash((type(self), self._name, id(self.library)))

    def __eq__(self, other):
        if type(self) != type(other):
            return NotImplemented
        if self._data != other._data:
            return False
        if { req.id for req in self.verifiesRequirement } != { req.id for req in other.verifiesRequirement }:
            return False
        return True
