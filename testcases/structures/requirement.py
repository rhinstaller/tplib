import functools
from . import Mapping as m
from .data_object import DataObject, DocumentObject, ListObject

class VerifiedBy(DataObject):
    mapping = dict((
        m('direct_list', required=False, default=(), func=list),
        m('query', required=False),
    ))


class AcceptanceCriteria(DataObject):
    mapping = dict((
        m('direct_list', required=False, default=(), func=list),
        m('query', required=False),
        m('named_query', required=False),
    ))


class Requirement(DocumentObject):
    mapping = dict((
        m('name'),
        m('description'),
        m('tags', required=False, default=(), func=set),
        m('verified_by', func=VerifiedBy),
        m('acceptance_criteria', required=False, default=(), func=dict),
    ))

    def __init__(self, data, parent=None, library=None):
        self.verificationTestCases = set()
        super().__init__(data, parent=parent, library=library)

    @property
    def id(self):
        return self.name

    def stabilize(self):
        for query_type, query in self.verified_by.data.items():
            if query is None:
                continue
            for testcase in self._findVerificationCases(query_type, query):
                testcase.verifiesRequirement.add(self)
                self.verificationTestCases.add(testcase)
        return True

    def _directListCases(self, cases_list):
        return set(
            [ self.library.testcases[case_name] for case_name in cases_list ]
        )

    def _directQueryCases(self, query):
        raise Exception('NOT IMPLEMENTED')

    def _namedQueryCases(self, query_name):
        raise Exception('NOT IMPLEMENTED')

    def _findVerificationCases(self, query_type, query):
        methods = {
            'direct_list' : self._directListCases,
            'query' : self._directQueryCases,
            'named_query' : self._namedQueryCases,
        }
        try:
            return methods[query_type](query)
        except KeyError:
            raise ValueError("Unknown query type: '%s'" % query_type)
