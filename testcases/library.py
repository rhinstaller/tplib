from copy import copy
import os
import fnmatch

from .structures.testcase import TestCase
from .structures.requirement import Requirement

def _iter_documents(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if fnmatch.fnmatchcase(filename, pattern):
                yield os.path.join(root, filename)

def diff(old, new):
    old_requirements = set(old.requirements)
    old_cases = set(old.testcases)
    new_requirements = set(new.requirements)
    new_cases = set(new.testcases)
    retval = {
        "removed" : {
            "testplans" : set(),
            "requirements" : old_requirements.difference(new_requirements),
            "testcases" : old_cases.difference(new_cases),
        },
        "added" : {
            "testplans" : set(),
            "requirements" : new_requirements.difference(old_requirements),
            "testcases" : new_cases.difference(old_cases),
        },
        "changed" : {
            "testplans" : set(),
            "requirements" : set(),
            "testcases" : set(),
        },
        "unchanged" : {
            "testplans" : set(),
            "requirements" : old_requirements.intersection(new_requirements),
            "testcases" : old_cases.intersection(new_cases),
        },
    }
    # WILL ACTIVATE LATER WHEN TESTPLANS ARE ADDED
    #for testplan_id in copy(retval["unchanged"]["testplans"]):
    #    if old.testplans[testplan_id] != new.testplans[testplan_id]:
    #        retval["unchanged"]["testplans"].remove(testplan_id)
    #        retval["changed"]["testplans"].add(testplan_id)
    for requirement_id in copy(retval["unchanged"]["requirements"]):
        if old.requirements[requirement_id] != new.requirements[requirement_id]:
            retval["unchanged"]["requirements"].remove(requirement_id)
            retval["changed"]["requirements"].add(requirement_id)
    for case_id in copy(retval["unchanged"]["testcases"]):
        if old.testcases[case_id] != new.testcases[case_id]:
            retval["unchanged"]["testcases"].remove(case_id)
            retval["changed"]["testcases"].add(case_id)
    return retval

class Library():
    def __init__(self, directory):
        self.directory = directory
        self.testcases = self._load_testcases()
        self.requirements = self._load_requirements()
        self._calculate_and_stabilize()

    def _load_testcases(self):
        return self._load_structures(self.directory, '*.tc.yaml', TestCase)

    def _load_requirements(self):
        return self._load_structures(self.directory, '*.req.yaml', Requirement)

    def _load_structures(self, directory, pattern, cls):
        structures = dict()
        for docfile in _iter_documents(directory, pattern):
            structure = cls(docfile, library=self, basedir=directory)
            structures[structure.id] = structure
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
