import functools
from . import Mapping as m
from .data_object import DataObject, DocumentObject, ListObject
from ..expressions import eval_bool
from ..exceptions import MissingLinkedItem


class QueryObject(DataObject):
    mapping = dict((
        m('direct_list', required=False, func=list, default=()),
        m('query', required=False),
        m('named_query', required=False),
    ))

class Selection(DataObject):
    mapping = dict((
        m('test_cases', required=False, func=QueryObject),
        m('requirements', required=False, func=QueryObject),
    ))

class Reportings(ListObject):
    @property
    def name(self):
        return 'Reportings_ListObject'

    def feed(self, data):
        if not isinstance(data, list):
            raise TypeError('%s: Reporting contains invalid data: %r. List type was expected.' % (self.document.filename, data))
        self.data = [ Reporting(item, library=self.library, document=self.document) for item in data ]
        data.clear()

class Reporting(DataObject):
    mapping = dict((
        m('type'),
        m('condition', required=False),
        m('data', required=False, allowed_types=object),
    ))

class ExecuteOnList(ListObject):
    @property
    def name(self):
        return 'ExecuteOn_ListObject'

    def feed(self, data):
        if not isinstance(data, list):
            raise TypeError('%s: execute_on contains invalid data: %r. List type was expected.' % (self.document.filename, data))
        self.data = [ ExecuteOn(item, library=self.library, document=self.document) for item in data ]
        data.clear()

class ExecuteOn(DataObject):
    mapping = dict((
        m('filter', required=False, allowed_types=str),
    ))

class TestPlan(DocumentObject):
    parent_key_name = 'parent_plan'
    mapping = dict((
        m('name'),
        m('description', required=False),
        m('point_person', inherited=True),
        m('tags', required=False, default=(), func=set, inherited=True),
        m('artifact_type', inherited=True),
        m('execute_on', inherited=True, required=False, func=ExecuteOnList),
        m('parent_plan', required=False),
        m('verified_by', required=False, func=Selection),
        m('reporting', inherited=True, func=Reportings, required=False),
        m('acceptance_criteria', required=False, func=Selection),
        m('configurations', required=False, default=None, inherited=True, allowed_types=(list,type(None))),
        m('document', required=False)
    ))
    runtime_properties = [
        'verificationTestCases',
        'acceptanceTestCases',
        'verificationRequirements',
        'acceptanceRequirements'
    ]

    def __init__(self, filename, library=None, basedir=None, possible_parents=dict()):
        self.verificationTestCases = set()
        self.verificationRequirements = set()
        self.acceptanceTestCases = set()
        self.acceptanceRequirements = set()
        super().__init__(filename, library=library, basedir=basedir, possible_parents=possible_parents)

    def stabilize(self):
        # Get verificationRequirements
        try:
            self.verificationRequirements |= self.library.getRequirementsByNames(self.verified_by.requirements.direct_list)
        except KeyError as key_value:
            raise MissingLinkedItem(key_value, self.name)
        self.verificationRequirements |= self.library.getRequirementsByQuery(self.verified_by.requirements.query, tp=self)
        self.verificationRequirements |= self.library.getRequirementsByNamedQuery(self.verified_by.requirements.named_query, tp=self)

        # Get verificationTestCases
        self.verificationTestCases |= self.library.getTestCasesByNames(self.verified_by.test_cases.direct_list)
        self.verificationTestCases |= self.library.getTestCasesByQuery(self.verified_by.test_cases.query, tp=self)
        self.verificationTestCases |= self.library.getTestCasesByNamedQuery(self.verified_by.test_cases.named_query, tp=self)

        # Add testcases verified by verificationRequirements to verificationTestCases
        for requirement in self.verificationRequirements:
            self.verificationTestCases |= requirement.verificationTestCases

        # Get acceptanceRequirements
        self.acceptanceRequirements |= self.library.getRequirementsByNames(self.acceptance_criteria.requirements.direct_list)
        self.acceptanceRequirements |= self.library.getRequirementsByQuery(self.acceptance_criteria.requirements.query, tp=self)
        self.acceptanceRequirements |= self.library.getRequirementsByNamedQuery(self.acceptance_criteria.requirements.named_query, tp=self)

        # Check that acceptanceRequirements is subset of verificationRequirements
        if not self.acceptanceRequirements.issubset(self.verificationRequirements):
            raise RuntimeError("self.acceptanceRequirements is not subset of self.verificationRequirements")

        # Get acceptanceTestCases from acceptanceRequirements
        for requirement in self.acceptanceRequirements:
            self.acceptanceTestCases |= requirement.acceptanceTestCases

        # Get acceptanceTestCases from verificationTestCases
        self.acceptanceTestCases |= self.library.getTestCasesByNames(self.acceptance_criteria.test_cases.direct_list, get_from=self.verificationTestCases)
        self.acceptanceTestCases |= self.library.getTestCasesByQuery(self.acceptance_criteria.test_cases.query, get_from=self.verificationTestCases, tp=self)
        self.acceptanceTestCases |= self.library.getTestCasesByNamedQuery(self.acceptance_criteria.test_cases.named_query, get_from=self.verificationTestCases, tp=self)

    def eval_execute_on(self, *args, **kwargs):
        if not self.execute_on:
            return True

        for plan_filter in self.execute_on:
            if 'filter' in plan_filter:
                if eval_bool(plan_filter.filter, tp=self, *args, **kwargs):
                    return True

        return False

    @property
    def id(self):
        return self.name

    def __hash__(self):
        return hash((type(self), self._name, id(self.library)))

    def __eq__(self, other):
        if type(self) != type(other):
            return NotImplemented
        if self.data != other.data:
            return False

        checked_references = [
            'verificationTestCases',
            'acceptanceTestCases',
            'verificationRequirements',
            'acceptanceRequirements'
        ]

        for ref in checked_references:
            if { req.id for req in getattr(self, ref) } != { req.id for req in getattr(other, ref) }:
                return False
        return True
