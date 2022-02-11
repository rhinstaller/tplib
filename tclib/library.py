from copy import copy
import os
import fnmatch

from .structures.testcase import TestCase
from .structures.requirement import Requirement
from .structures.testplan import TestPlan
from .exceptions import CollisionError, UnknownParentError, DocfilesError
from .expressions import compile_bool


def _iter_documents(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if fnmatch.fnmatchcase(filename, pattern):
                yield os.path.join(root, filename)

def diff(old, new):
    if old is None:
        old_requirements = set()
        old_cases = set()
        old_testplans = set()
    else:
        old_requirements = set(old.requirements)
        old_cases = set(old.testcases)
        old_testplans = set(old.testplans)
    new_requirements = set(new.requirements)
    new_cases = set(new.testcases)
    new_testplans = set(new.testplans)
    retval = {
        "removed" : {
            "testplans" : old_testplans.difference(new_testplans),
            "requirements" : old_requirements.difference(new_requirements),
            "testcases" : old_cases.difference(new_cases),
        },
        "added" : {
            "testplans" : new_testplans.difference(old_testplans),
            "requirements" : new_requirements.difference(old_requirements),
            "testcases" : new_cases.difference(old_cases),
        },
        "modified" : {
            "testplans" : set(),
            "requirements" : set(),
            "testcases" : set(),
        },
        "unchanged" : {
            "testplans" : old_testplans.intersection(new_testplans),
            "requirements" : old_requirements.intersection(new_requirements),
            "testcases" : old_cases.intersection(new_cases),
        },
    }
    for testplan_id in copy(retval["unchanged"]["testplans"]):
        if old.testplans[testplan_id] != new.testplans[testplan_id]:
            retval["unchanged"]["testplans"].remove(testplan_id)
            retval["modified"]["testplans"].add(testplan_id)
    for requirement_id in copy(retval["unchanged"]["requirements"]):
        if old.requirements[requirement_id] != new.requirements[requirement_id]:
            retval["unchanged"]["requirements"].remove(requirement_id)
            retval["modified"]["requirements"].add(requirement_id)
    for case_id in copy(retval["unchanged"]["testcases"]):
        if old.testcases[case_id] != new.testcases[case_id]:
            retval["unchanged"]["testcases"].remove(case_id)
            retval["modified"]["testcases"].add(case_id)
    return retval

class Library():
    def __init__(self, directory):
        self.directory = directory
        self.testplans = self._load_testplans()
        self.testcases = self._load_testcases()
        self.requirements = self._load_requirements()
        self._calculate_and_stabilize()

    def _load_testplans(self):
        return self._load_structures(self.directory, '*.plan.yaml', TestPlan)

    def _load_testcases(self):
        return self._load_structures(self.directory, '*.tc.yaml', TestCase)

    def _load_requirements(self):
        return self._load_structures(self.directory, '*.req.yaml', Requirement)

    def _load_structures(self, directory, pattern, cls):
        """
        Load structures strored in files of name matching ``pattern`` from
        provided ``directory`` and use the ``cls`` to construct them.

        The structures are loaded in greedy way and in case there's an error
        which prevents constructing the structure, it's skipped and retried
        loading later (hoping that there's the missing information now present).
        """
        structures = dict()
        docfiles = list(_iter_documents(directory, pattern))
        errors = dict()
        while docfiles:
            docfile_loaded = False
            for docfile in copy(docfiles):
                try:
                    structure = cls(docfile, library=self, basedir=directory, possible_parents=structures)
                except UnknownParentError as e:
                    errors[docfile] = e
                    continue
                try:
                    # try to find if structure of the same id
                    other = structures[structure.id]
                    raise CollisionError("Attempted to load two structures of the same type with the same id (name)", structure.filename, other.filename)
                except KeyError:
                    pass
                structures[structure.id] = structure
                docfiles.remove(docfile)
                docfile_loaded = True
                # clean any previously hit errors
                errors.pop(docfile, None)
            if not docfile_loaded:
                break
        if docfiles:
            raise DocfilesError(docfiles, errors)
        return structures

    def _calculate_and_stabilize_structures(self, structures):
        unstable = set(structures.keys())
        last_count = 0
        while len(unstable) != last_count:
            last_count = len(unstable)
            for structure_id in list(unstable):
                if structures[structure_id].stabilize():
                    unstable.remove(structure_id)
        return len(unstable) == 0

    def _calculate_and_stabilize(self):
        self._calculate_and_stabilize_structures(self.requirements)
        self._calculate_and_stabilize_structures(self.testcases)
        self._calculate_and_stabilize_structures(self.testplans)

    # Lookups
    def getTestCasesByNames(self, names, get_from=None):
        """ Finds testcases based on list of names

        :param names: List of testcase names
        :type names: list
        :param get_from: where to look for testcases, defaults to self.testcases
        :type get_from: set or list, optional
        :return: set of found testcases
        :rtype: set

        """
        if get_from is None:
            get_from = self.testcases.values()
        return self._names_to_objects(names, get_from)

    def getRequirementsByNames(self, names, get_from=None):
        """ Finds requirements based on list of names

        :param names: List of requirement names
        :type names: list
        :param get_from:  where to look for requirements, defaults to self.requirements
        :type get_from: set or list, optional
        :return: set of found requirements
        :rtype: set
        """
        if get_from is None:
            get_from = self.requirements.values()
        return self._names_to_objects(names, get_from)

    def _names_to_objects(self, names, get_from):
        """ Finds objects from get_from based on list of names, raises KeyError if object of the name cannot be find.

        :param names: List of object names
        :type names: list
        :param get_from:  where to look for objects
        :type get_from: dict
        :raises KeyError: name in list doesn't correspond to any object in get_from
        :return: set of found objects
        :rtype: set
        """
        get_from = { item.name : item for item in get_from }
        return { get_from[name] for name in names }

    def getRequirementsByQuery(self, query, get_from=None, **kwargs):
        """ Finds requirements based on query, any extra arguments are handover to template.render(),
        reference to object calling this function is expected, for example when called from testplan
        add tp=self

        :param query: jinja2 expression
        :type query: str
        :param get_from: where to look for requirements, defaults to self.requirements.values()
        :type get_from: list or set
        :return: set of found requirements
        :rtype: set
        """
        if query is None:
            return set()

        if get_from is None:
            get_from = self.requirements.values()

        eval_bool_query = compile_bool(query)
        return { requirement for requirement in get_from if eval_bool_query(req=requirement, **kwargs) }

    def getTestCasesByQuery(self, query, get_from=None, **kwargs):
        """ Finds testcases based on query, any extra arguments are handover to template.render(),
        reference to object calling this function is expected, for example when called from testplan
        add tp=self

        :param query: jinja2 expression
        :type query: str
        :param get_from: where to look for testcases, defaults to self.testcases.values()
        :type get_from: list or set
        :return: set of found testcases
        :rtype: set
        """
        if query is None:
            return set()

        if get_from is None:
            get_from = self.testcases.values()

        eval_bool_query = compile_bool(query)
        return { testcase for testcase in get_from if eval_bool_query(tc=testcase, **kwargs) }

    def getTestPlansByQuery(self, query, get_from=None, **kwargs):
        """ Finds testplans based on query, any extra arguments are handover to template.render(),
        reference to object calling this function is expected, for example when called from event
        add event=self

        :param query: jinja2 expression
        :type query: str
        :param get_from: where to look for testplans, defaults to self.testplans.values()
        :type get_from: list or set
        :return: set of found testplans
        :rtype: set
        """
        if query is None:
            return set()

        if get_from is None:
            get_from = self.testplans.values()

        eval_bool_query = compile_bool(query)
        return { testplan for testplan in get_from if eval_bool_query(tp=testplan, **kwargs) }

    def getRequirementsByNamedQuery(self, query_name, get_from=None, **kwargs):
        """ Finds requirements based on query, any extra arguments are handover to template.render(),
        reference to object calling this function is expected, for example when called from testplan
        add tp=self

        :param query_name: Name of query
        :type query_name: str
        :param get_from: where to look for requirements, defaults to self.requirements.values()
        :type get_from: list or set
        :return: set of found requirements
        :rtype: set
        """
        if query_name is None:
            return set()
        raise RuntimeError('named_query is not implemented')

    def getTestCasesByNamedQuery(self, query_name, get_from=None, **kwargs):
        """ Finds testcases based on query, any extra arguments are handover to template.render(),
        reference to object calling this function is expected, for example when called from testplan
        add tp=self

        :param query_name: Name of query
        :type query_name: str
        :param get_from: where to look for testcases, defaults to self.testcases.values()
        :type get_from: list or set
        :return: set of found testcases
        :rtype: set
        """
        if query_name is None:
            return set()
        raise RuntimeError('named_query is not implemented')

    def getTestPlansByNamedQuery(self, query_name, get_from=None, **kwargs):
        """ Finds testplans based on query, any extra arguments are handover to template.render(),
        reference to object calling this function is expected, for example when called from event
        add event=self

        :param query_name: Name of query
        :type query_name: str
        :param get_from: where to look for testplans, defaults to self.testplans.values()
        :type get_from: list or set
        :return: set of found testplans
        :rtype: set
        """
        if query_name is None:
            return set()
        raise RuntimeError('named_query is not implemented')
