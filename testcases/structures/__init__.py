class Mapping():
    def __init__(self, name, source=None, required=True, default=None,
                 inherited=False, func=None, allowed_types=str):
        self.name = name
        self.source = source if source is not None else name
        self.required = required
        self.default = default
        self.inherited = inherited
        self.func = func
        self.allowed_types = allowed_types

    # Enable using mapping in dict constructor
    def __iter__(self):
        yield self.name
        yield self
