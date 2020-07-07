class CollisionError(Exception):
    def __init__(self, message, one, other):
        super().__init__()
        self.message = message
        self.one = one
        self.other = other

    def __str__(self):
        return "%s: '%s', '%s'" % (self.message, self.one, self.other)
