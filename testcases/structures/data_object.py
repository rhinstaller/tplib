from abc import ABC, abstractmethod

class GarbageData(Exception):
    pass

class DataObject(ABC):
    mapping = dict()

    def __init__(self, data, parent=None):
        self.data = {}
        self.parent = parent
        self.feed(data)
        if data:
            raise GarbageData(
                "%s document contains additional unexpected data: %s" % (
                    type(self),
                    data
                )
            )

    def _autofeed(self, data):
        for mapping in self.mapping.values():
            try:
                default = mapping.default
                inheritance = mapping.inherited and self.parent is not None
                # obtain value respecting inheritance, default and required flag
                if mapping.required and not inheritance:
                    # required without inheritance allowed
                    value = data.pop(mapping.source)
                elif mapping.required and inheritance:
                    # required with possible inheritance
                    value = data.pop(mapping.source,
                                     getattr(self.parent, mapping.name))
                elif inheritance:
                    # optional with possible inheritance
                    value = data.pop(mapping.source,
                                     getattr(self.parent, mapping.name, default))
                else:
                    # optional without inheritance
                    value = data.pop(mapping.source, default)
                # transform value desired way if desired
                if mapping.func is not None:
                    value = mapping.func(value)
                # assign obtained value
                self.data[mapping.name] = value
            except KeyError as e:
                # add support for validation here!
                raise e


    def feed(self, data):
        self._autofeed(data)


    @property
    def _name(self):
        return self.data.get('name', 'unnamed')


    def __getattr__(self, name):
        try:
            return super().__getattr__(self, name)
        except AttributeError:
            return self.data[name]


    def __repr__(self):
        return '<%s.%s(%s)>' % (
            type(self).__module__,
            type(self).__name__,
            self._name,
        )
