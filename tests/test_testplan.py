import unittest
from tclib.structures import testplan

class TestTestPlan(unittest.TestCase):
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
