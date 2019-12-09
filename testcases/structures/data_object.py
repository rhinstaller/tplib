from abc import ABC, abstractmethod

class GarbageData(Exception):
    def __init__(self, instance, data):
        message = "%s document contains additional unexpected data: %s"
        super().__init__(message % (type(instance), data))

class DataObject(ABC):
    mapping = dict()
    allow_nonstandard_values = True

    def __init__(self, data, parent=None):
        self.data = {}
        self.parent = parent
        data = self.feed(data)
        if data:
            raise GarbageData(self, data)

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
                # transform value desired way if desired or check allowed types
                # if no transformation should be done
                if mapping.func is not None:
                    value = mapping.func(value)
                elif not isinstance(value, mapping.allowed_types):
                    raise TypeError("Wrong type of: %s. Expected one of: %s, was: %s" % (mapping.name, mapping.allowed_types, type(value)))
                # assign obtained value
                self.data[mapping.name] = value
            except KeyError as e:
                # add support for validation here!
                if validate:
                    print(e)
                else:
                    raise e

        # process x- values if allowed
        if self.allow_nonstandard_values:
            for key in list(data.keys()):
                if key.startswith('x-'):
                    self.data[key] = data.pop(key)

        return data


    def feed(self, data):
        data = self._autofeed(data)


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


    def dump(self, indent=2):
        def dump_or_repr(data, indent):
            try:
                return data.dump(indent)
            except AttributeError:
                return repr(data)

        return '<%s.%s(%s){\n%s}>' % (
            type(self).__module__,
            type(self).__name__,
            self._name,
            ",\n".join([
                (indent*" " + "%s: %s") % (key, dump_or_repr(value, indent+2))
                for key, value
                in self.data.items()
            ]),
        )

class ListObject(DataObject):
    @property
    def _name(self):
        return self.name

    def dump(self, indent=2):
        def dump_or_repr(data, indent):
            try:
                return data.dump(indent)
            except AttributeError:
                return repr(data)

        return '<%s.%s(%s){\n%s}>' % (
            type(self).__module__,
            type(self).__name__,
            self._name,
            ",\n".join([
                (indent*" " + "%s") % dump_or_repr(value, indent+2)
                for value
                in self.data
            ]),
        )
