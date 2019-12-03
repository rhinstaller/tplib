from .data_object import DataObject

class NotTestCase(Exception):
    pass

class Mapping():
    def __init__(self, name, source=None, required=True, default=None,
                 inherited=False, func=None):
        self.name = name
        self.source = source if source is not None else name
        self.required = required
        self.default = default
        self.inherited = inherited
        self.func = func

    # Enable using mapping in dict constructor
    def __iter__(self):
        yield self.name
        yield self

m = Mapping

class TestCase(DataObject):
    mapping = dict((
        m('name'),
        m('description'),
        m('priority'),
        m('execution'),
        m('filter'),
        m('instructions'),
        m('configurations', inherited=True),
        m('author', required=False),
        m('tags', required=False, default=[], func=set)
    ))
