import unittest
from tplib.structures import testcase

class TestTestcase(unittest.TestCase):
    def test_simple_load(self):
        tc = testcase.TestCase('./data/baselib/ignition.tc.yaml')
        expected = {'name': 'Ignition',
                    'description': 'Tests ignition system',
                    'priority': 6,
                    'execution': {'type': 'manual'},
                    'instructions': {'steps': [{'step': 'Connect', 'result': 'Connected'},
                                               {'step': 'Try to start', 'result': 'Started'}]},
                    'author': 'tester@example.com',
                    'tags': ['electronics']}
        self.assertEqual(tc.serialize(), expected)
