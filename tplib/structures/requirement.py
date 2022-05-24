import functools
from . import Mapping as m
from .data_object import DataObject, DocumentObject, ListObject
from ..exceptions import MissingLinkedItem

class QueryObject(DataObject):
    mapping = dict((
        m('direct_list', required=False, func=list, default=()),
        m('query', required=False),
        m('named_query', required=False),
    ))

class Requirement(DocumentObject):
    mapping = dict((
        m('name'),
        m('description', required=False),
        m('tags', required=False, default=(), func=set),
        m('verified_by', required=False, func=QueryObject),
        m('acceptance_criteria', required=False, func=QueryObject),
    ))
    runtime_properties = [
        'verificationTestCases',
        'acceptanceTestCases',
    ]

    def __init__(self, filename, override_data=None, library=None, basedir=None, possible_parents=None):
        self.verificationTestCases = set()
        self.acceptanceTestCases = set()
        super().__init__(filename, override_data=override_data, library=library, basedir=basedir, possible_parents=possible_parents)

    def stabilize(self):
        # Get verificationTestCases
        try:
            self.verificationTestCases |= self.library.getTestCasesByNames(self.verified_by.direct_list)
        except KeyError as key_value:
            raise MissingLinkedItem(key_value, self.name)
        self.verificationTestCases |= self.library.getTestCasesByQuery(self.verified_by.query, req=self)
        self.verificationTestCases |= self.library.getTestCasesByNamedQuery(self.verified_by.named_query, req=self)

        # Get acceptanceTestCases from verificationTestCases
        self.acceptanceTestCases |= self.library.getTestCasesByNames(self.acceptance_criteria.direct_list, get_from=self.verificationTestCases)
        self.acceptanceTestCases |= self.library.getTestCasesByQuery(self.acceptance_criteria.query, get_from=self.verificationTestCases, tp=self)
        self.acceptanceTestCases |= self.library.getTestCasesByNamedQuery(self.acceptance_criteria.named_query, get_from=self.verificationTestCases, tp=self)

        # Mark tescases
        for testcase in self.verificationTestCases:
            testcase.verifiesRequirement.append(self)

    @property
    def id(self):
        return self.name

    def __hash__(self):
        return hash((type(self), self._name, id(self.library)))

    def __eq__(self, other):
        if type(self) != type(other):
            return NotImplemented
        if self._data != other._data:
            return False

        checked_references = [
            'verificationTestCases',
            'acceptanceTestCases'
        ]

        for ref in checked_references:
            if { req.id for req in getattr(self, ref) } != { req.id for req in getattr(other, ref) }:
                return False
        return True
