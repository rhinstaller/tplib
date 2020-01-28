import functools
from . import Mapping as m
from .data_object import DataObject, DocumentObject, ListObject

class VerifiedBy(DataObject):
    mapping = dict((
        m('direct_list', required=False, func=list),
        m('query', required=False),
    ))


class AcceptanceCriteria(DataObject):
    mapping = dict((
        m('direct_list', required=False, func=list),
        m('query', required=False),
        m('named_query', required=False),
    ))


class Requirement(DocumentObject):
    mapping = dict((
        m('name'),
        m('description'),
        m('tags', required=False, default=[], func=set),
        m('verified_by', func=VerifiedBy),
        m('acceptance_criteria', required=False, func=dict),
    ))

    def __init__(self, data, parent=None, library=None):
        self.verificationTestCases = set()
        super().__init__(data, parent=parent, library=library)

    @property
    def id(self):
        return self.name
