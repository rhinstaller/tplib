import unittest
from tclib.structures import requirement

class TestRequirement(unittest.TestCase):
    def test_simple_load(self):
        req = requirement.Requirement('./data/baselib/running.req.yaml')
        expected = {'name': 'Running',
                    'description': 'The engine must be running',
                    'verified_by': {'direct_list': ['Ignition'],
                                    'query': '"engine" in tc.tags'},
                    'acceptance_criteria': {}}
        self.assertEqual(req.serialize(), expected)
