class Mapping():
    # TODO: add support for one_of=str(group) which extends required
    # It should be used to group multiple mappings together and only one of
    # the mapping of the group can and has to be set. Mappings of one_of
    # cannot have default value.
    def __init__(self, name, source=None, required=True, default=None,
                 inherited=False, func=None, allowed_types=str):
        self.name = name
        self.source = source if source is not None else name
        self.required = required
        self.default = default
        self.inherited = inherited
        self.func = func
        self.allowed_types = allowed_types
        if not isinstance(allowed_types, tuple):
            self.allowed_types = (self.allowed_types, )
        if self.required == False and self.default is None and type(None) not in self.allowed_types:
            self.allowed_types = self.allowed_types + (type(None), )

    # Enable using mapping in dict constructor
    def __iter__(self):
        yield self.name
        yield self
