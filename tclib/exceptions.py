class CollisionError(Exception):
    def __init__(self, message, one, other):
        super().__init__()
        self.message = message
        self.one = one
        self.other = other

    def __str__(self):
        return "%s: '%s', '%s'" % (self.message, self.one, self.other)

class UnknownParentError(Exception):
    """
    Raised in DataObject constructor when the object has specified parent
    but no such parent can be found in provided library.

    :param structure_desc: Description of the structure for which the parent couldn't be found.
    :type structure_desc: str
    :param parent_spec: Specification of the parent which couldn't be found.
    :type parent_spec: str
    """
    def __init__(self, structure_desc, parent_spec):
        super().__init__()
        self.structure_desc = structure_desc
        self.parent_spec = parent_spec

    def __str__(self):
        return "Cannot find parent '%s' for '%s'" % (
            self.parent_spec,
            self.structure_desc,
        )

class DocfilesError(Exception):
    def __init__(self, docfiles):
        super().__init__()
        self.docfiles = docfiles

    def __str__(self):
        return "Couldn't process following docfiles: %s" % ', '.join([
            "'%s'" % docfile for docfile in self.docfiles
        ])

class GarbageData(Exception):
    def __init__(self, instance, data):
        message = "%s in %s document contains additional unexpected data: %s"
        super().__init__(message % (type(instance), instance.document.filename, data))