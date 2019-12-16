import yaml
import functools
from . import Mapping as m
from .data_object import DataObject, ListObject

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


class TestCase(DataObject):
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

    def __init__(self, filename, override_data=None, parent=None):
        self.filename = filename
        data = override_data
        if override_data is None:
            with open(self.filename) as testcase_fo:
                data = yaml.safe_load(testcase_fo)
        super().__init__(data, parent)
