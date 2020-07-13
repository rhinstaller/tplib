import os
import yaml
import copy
from abc import ABC, abstractmethod
from ..exceptions import UnknownParentError
from ..expressions import eval_bool


## BEGIN OF VERY VERY VERY POOR PLACE FOR MODIFYING YAML DUMP BEHAVIOUR
## Multiline strings should be formatted using '|' character
## Source: https://stackoverflow.com/a/45004775
yaml.SafeDumper.orig_represent_str = yaml.SafeDumper.represent_str

def repr_str(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='|')
    return dumper.orig_represent_str(data)

yaml.add_representer(str, repr_str, Dumper=yaml.SafeDumper)
## END

def dump_or_repr(data, indent):
    try:
        return data.dump(indent)
    except AttributeError:
        return repr(data)

def serialize_value(value):
    if isinstance(value, DataObject):
        return value.serialize()
    if isinstance(value, set):
        return list(value)
    return value

class GarbageData(Exception):
    def __init__(self, instance, data):
        message = "%s document contains additional unexpected data: %s"
        super().__init__(message % (type(instance), data))

class DataObject(ABC):
    mapping = dict()
    runtime_properties = []
    allow_nonstandard_values = True
    parent_key_name = None
    default_data = {}

    def __init__(self, data, library=None, possible_parents=None):
        self.data = {}
        self.parent = None
        self.library = library

        if data is None:
            data = copy.deepcopy(self.default_data)

        self._getParent(data, possible_parents)

        data = self.feed(data)
        if data:
            raise GarbageData(self, data)

    def _getParent(self, data, possible_parents):
        # Try to get reference to parent object
        if possible_parents is None:
            possible_parents = {}
        if self.parent_key_name is not None:
            parent_name = data[self.parent_key_name]
            if parent_name is not None:
                try:
                    self.parent = possible_parents[parent_name]
                except KeyError:
                    raise UnknownParentError('', self.parent_key_name)

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
        return self._autofeed(data)


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

    def _should_serialize_self(self):
        return bool(self.data)

    def _should_serialize_item(self, item):
        mapping = self.mapping[item]
        if mapping.required:
            return True
        if isinstance(self.data[item], DataObject):
            return self.data[item]._should_serialize_self()
        default = mapping.default
        if mapping.func is not None:
            default = mapping.func(default)
        if default == self.data[item]:
            return False
        return True

    def serialize(self):
        return { key : serialize_value(value) for key, value in self.data.items() if self._should_serialize_item(key) }


class ListObject(DataObject):
    default_data = []

    @property
    def _name(self):
        return self.name

    def dumpcontent(self, indent):
        return ",\n".join([
            (indent*" " + "%s") % dump_or_repr(value, indent)
            for value
            in self.data
        ])

    def serialize(self):
        return [ value.serialize() if isinstance(value, DataObject) else value for value in self.data ]


class DocumentObject(DataObject):
    def __init__(self, filename, override_data=None, library=None, basedir=None, possible_parents=None):
        self.filename = filename
        self.basedir = basedir
        if self.basedir is not None:
            self.filename = os.path.relpath(filename, self.basedir)
        data = override_data
        if override_data is None:
            with open(filename) as testcase_fo:
                data = yaml.safe_load(testcase_fo)
        super().__init__(data, library=library, possible_parents=possible_parents)

    def toYaml(self):
        return yaml.safe_dump(self.serialize(), sort_keys=False)
