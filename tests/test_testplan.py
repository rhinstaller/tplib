import unittest
import yaml
from os import path
from tempfile import mkdtemp
from distutils import dir_util
from tplib import library
from tplib.structures import testplan

class TestLoadTestPlan(unittest.TestCase):
    def test_simple_load(self):
        tp = testplan.TestPlan('./data/baselib/main.plan.yaml')
        expected = {'name': 'Main parent plan',
                    'description': 'Main parent test plan',
                    'point_person': 'tester@example.com',
                    'tags': ['main'],
                    'artifact_type': 'vehicle',
                    'execute_on': [{'filter': "event.type == 'assembly'"}],
                    'verified_by': {'test_cases': {}, 'requirements': {}},
                    'reporting': [{'type': 'testdb', 'data': {'table': 'general_testing'}}],
                    'acceptance_criteria': {'test_cases': {}, 'requirements': {}},
                    'configurations': [{'wheels': 4, 'drivetrain': 'gas'},
                                        {'wheels': 4, 'drivetrain': 'electric'},
                                        {'wheels': 8, 'drivetrain': 'gas'},
                                        {'wheels': 8, 'drivetrain': 'electric'}]}
        self.assertEqual(tp.serialize(), expected)

class TestStabilizeTestPlan(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library_dir = './data/baselib'
        cls.baselib = library.Library(cls.library_dir)

    def test_verified_by_tc(self):
        # Test case from direct_list
        self.assertIn(self.baselib.testcases['Ignition'], self.baselib.testplans['Sub plan A'].verificationTestCases)
        # Test case from query
        self.assertIn(self.baselib.testcases['Engine fuel consumption'], self.baselib.testplans['Sub plan A'].verificationTestCases)
        # Test case from named query
        # not implemented

    def test_verified_by_req(self):
        # Requirement from direct_list
        self.assertIn(self.baselib.requirements['Electronics'], self.baselib.testplans['Plan B'].verificationRequirements)
        # Test case from requirement from direct_list
        self.assertIn(self.baselib.testcases['Ignition'], self.baselib.testplans['Plan B'].verificationTestCases)
        # Requirement from query
        self.assertIn(self.baselib.requirements['Controls'], self.baselib.testplans['Plan B'].verificationRequirements)
        # Test case from requirement from query
        self.assertIn(self.baselib.testcases['Steering wheel'], self.baselib.testplans['Plan B'].verificationTestCases)

    def test_acceptance_criteria_tc(self):
        # Test case from direct_list
        self.assertIn(self.baselib.testcases['Ignition'], self.baselib.testplans['Sub plan A'].acceptanceTestCases)
        # Test case from query
        self.assertIn(self.baselib.testcases['Engine quality'], self.baselib.testplans['Sub plan A'].acceptanceTestCases)
        # Test case from named query
        # not implemented

    def test_acceptance_criteria_req(self):
        # Requirement from direct_list
        self.assertIn(self.baselib.requirements['Electronics'], self.baselib.testplans['Plan B'].acceptanceRequirements)
        # Test case from requirement from direct_list
        self.assertIn(self.baselib.testcases['Ignition'], self.baselib.testplans['Plan B'].acceptanceTestCases)
        # Requirement from query
        self.assertIn(self.baselib.requirements['Controls'], self.baselib.testplans['Plan B'].acceptanceRequirements)
        # Test case from requirement from query
        self.assertIn(self.baselib.testcases['Steering wheel'], self.baselib.testplans['Plan B'].acceptanceTestCases)

class TestStabilizeInvalidAcceptance(unittest.TestCase):
    def setUp(self):
        tp = {'name': 'Temporary',
              'description': 'Temporary testplan',
              'point_person': 'tester@example.com',
              'artifact_type': 'vehicle',
              'execute_on': [{'filter': "event.type == 'assembly'"}],
              'verified_by': {
                'requirements': {
                  'query': '"important" in req.tags'
                }
              },
              'acceptance_criteria': {
                'requirements': {
                  'direct_list': ['Electronics'],
                  'query': '"important" in req.tags'
                }
              }
            }

        self.temp_dir = mkdtemp()
        self.temporary_tp = path.join(self.temp_dir, 'temporary.tp.yaml')
        with open(self.temporary_tp, 'w') as file:
            yaml.safe_dump(tp, file)
        self.baselib = library.Library('./data/baselib')

    def tearDown(self):
        dir_util.remove_tree(self.temp_dir)

    def test_invalid_acceptance_requirements(self):
        tp = testplan.TestPlan(self.temporary_tp, library=self.baselib)
        try:
            tp.stabilize()
        except RuntimeError as exp:
            self.assertEqual(str(exp), 'self.acceptanceRequirements is not subset of self.verificationRequirements')
        else:
            self.fail()
