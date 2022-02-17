import unittest
from tclib import library
from tclib.structures import requirement

class TestLoadRequirement(unittest.TestCase):
    def test_simple_load(self):
        req = requirement.Requirement('./data/baselib/running.req.yaml')
        expected = {'name': 'Running',
                    'description': 'The engine must be running',
                    'verified_by': {'direct_list': ['Ignition'],
                                    'query': '"engine" in tc.tags'},
                    'acceptance_criteria': {}}
        self.assertEqual(req.serialize(), expected)

class TestStabilizeRequirement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library_dir = './data/baselib'
        cls.baselib = library.Library(cls.library_dir)

    def test_verified_by_tc(self):
        # Test case from direct_list
        self.assertIn(self.baselib.testcases['Ignition'], self.baselib.requirements['Running'].verificationTestCases)
        # Test case from query
        self.assertIn(self.baselib.testcases['Ignition'], self.baselib.requirements['Electronics'].verificationTestCases)

    def test_acceptance_criteria_tc(self):
        # Test case from direct_list
        self.assertIn(self.baselib.testcases['Steering wheel'], self.baselib.requirements['Controls'].acceptanceTestCases)
        # Test case from query
        self.assertIn(self.baselib.testcases['Ignition'], self.baselib.requirements['Electronics'].acceptanceTestCases)
