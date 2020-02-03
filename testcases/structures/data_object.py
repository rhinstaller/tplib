import yaml
from abc import ABC, abstractmethod

def dump_or_repr(data, indent):
    try:
        return data.dump(indent)
    except AttributeError:
        return repr(data)

class GarbageData(Exception):
    def __init__(self, instance, data):
        message = "%s document contains additional unexpected data: %s"
        super().__init__(message % (type(instance), data))

class DataObject(ABC):
    mapping = dict()
    runtime_properties = []
    allow_nonstandard_values = True

    def __init__(self, data, parent=None, library=None):
        self.data = {}
        self.parent = parent
        self.library = library
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
                validate = False
                print(self.filename)
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


    def stabilize(self):
        # Should be overloaded if data object needs stabilization
        # This should be used for calculation of various values
        # from the library. Once the object has all needed values
        # calculated, it should return True. If some more data
        # is still needed, False should be returned.
        return True


    @property
    def _name(self):
        return self.data.get('name')


    def __getattr__(self, name):
        try:
            return super().__getattr__(self, name)
        except AttributeError:
            return self.data[name]


    def __eq__(self, other):
        if type(self) != type(other):
            return NotImplemented
        if self.data != other.data:
            return False
        # !!! NOT A GOOD IDEA - THERE'S INFINITE RECURSION !!!
        #for prop in self.runtime_properties:
        #    if getattr(self, prop) != getattr(other, prop):
        #        return False
        return True


    def __ne__(self, other):
        if type(self) != type(other):
            return NotImplemented
        return not (self == other)


    def __getitem__(self, name):
        return self.data[name]


    def __repr__(self):
        return '<%s.%s(%s)>' % (
            type(self).__module__,
            type(self).__name__,
            self._name,
        )


    def __iter__(self):
        return self.data.__iter__()


    def dumpname(self):
        name = self._name
        if name is not None:
            return '%s.%s(%s)' % (
                type(self).__module__,
                type(self).__name__,
                name,
            )
        return '%s.%s' % (
            type(self).__module__,
            type(self).__name__,
        )

    def dumpcontent(self, indent):
        return ",\n".join([
            (indent*" " + "%s: %s") % (key, dump_or_repr(value, indent))
            for key, value
            in self.data.items()
        ])

    def dumpproperties(self, indent):
        return ",\n".join([
            (indent*" " + "%s: %s") % (prop_name, repr(getattr(self, prop_name)))
            for prop_name
            in self.runtime_properties
        ])

    def dump(self, indent=0):
        format_string_bare = """<%(name)s{
%(indent)s  DATA:
%(content)s
%(indent)s}>"""
        format_string_propeties = """<%(name)s{
%(indent)s  DATA:
%(content)s
%(indent)s  PROPERTIES:
%(properties)s
%(indent)s}>"""
        if self.runtime_properties:
            format_string = format_string_propeties
        else:
            format_string = format_string_bare
        return format_string % {
            'name' : self.dumpname(),
            'content' : self.dumpcontent(indent+4),
            'properties' : self.dumpproperties(indent+4),
            'indent' : indent*" ",
        }

class ListObject(DataObject):
    @property
    def _name(self):
        return self.name

    def dumpcontent(self, indent):
        return ",\n".join([
            (indent*" " + "%s") % dump_or_repr(value, indent)
            for value
            in self.data
        ])

class DocumentObject(DataObject):
    def __init__(self, filename, override_data=None, parent=None, library=None):
        self.filename = filename
        data = override_data
        if override_data is None:
            with open(self.filename) as testcase_fo:
                data = yaml.safe_load(testcase_fo)
        super().__init__(data, parent, library)
