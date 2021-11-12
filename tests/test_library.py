import unittest
from tclib import library

class TestAdditionalStructures(unittest.TestCase):
    def setUp(self):
        self.library_dir = './data/baselib'

        self.tp_data = {'name': 'Additional Testplan',
                       'point_person': 'tester@example.com',
                       'artifact_type': 'vehicle',
                       'execute_on': [{'filter': "event.type == 'assembly'"}],
                       'verified_by': {
                           'test_cases': {
                           'query': '"controls" in tc.tags'
                           },
                           'requirements': {
                           'query': '"additional_req" in req.tags'
                           }
                       },
                       'acceptance_criteria': {
                           'test_cases': {
                           'query': '"controls" in tc.tags'
                           }
                       }
                      }

        self.tc_data = {'name': 'Additional Testcase',
                       'description': 'Some additional testcase',
                       'tags': ['electronics'],
                       'author': 'tester@example.com',
                       'priority': 6,
                       'execution': {'type': 'manual'},
                       'instructions': {'steps': [{'step': 'do something'}]}
                      }

        self.tc_data2 = {'name': 'Additional Testcase 2',
                        'description': 'Some additional testcase 2',
                        'tags': ['additional'],
                        'author': 'tester@example.com',
                        'priority': 4,
                        'execution': {'type': 'manual'},
                        'instructions': {'steps': [{'step': 'do something'}]}
                       }

        self.req_data = {'name': 'Additional Requirement',
                        'description': 'Some additional requirement',
                        'tags': ['additional_req'],
                        'verified_by': {
                            'query': '"engine" in tc.tags or "additional" in tc.tags'
                        }
                       }

    def test_additional_testplan(self):
        # Load additional testplan
        tclib_library = library.Library(self.library_dir, additional_testplans=[self.tp_data])
        tp = tclib_library.testplans['Additional Testplan']
        # Verify testplan was loaded
        self.assertEquals(tp.name, 'Additional Testplan') 
        # Check that stabilization was performed on it
        self.assertIn(tclib_library.testcases['Steering wheel'], tp.verificationTestCases)

    def test_additional_testcase(self):
        # Load additional testcase
        tclib_library = library.Library(self.library_dir, additional_testcases=[self.tc_data])
        tc = tclib_library.testcases['Additional Testcase']
        # Verify testcase was loaded
        self.assertEquals(tc.name, 'Additional Testcase') 
        # Check that stabilization was performed on it
        self.assertIn(tclib_library.requirements['Electronics'], tc.verifiesRequirement)

    def test_additional_requirement(self):
        # Load additional requirement
        tclib_library = library.Library(self.library_dir, additional_requirements=[self.req_data])
        req = tclib_library.requirements['Additional Requirement']
        # Verify requirement was loaded
        self.assertEquals(req.name, 'Additional Requirement') 
        # Check that stabilization was performed on it
        self.assertIn(tclib_library.testcases['Engine quality'], req.verificationTestCases)

    def test_linked_additional_structures(self):
        # Remove query that could silently invalidate this testcase in the future
        del(self.tp_data['verified_by']['test_cases'])
        # Load additional structures
        tclib_library = library.Library(self.library_dir,
                                        additional_testplans=[self.tp_data],
                                        additional_requirements=[self.req_data],
                                        additional_testcases=[self.tc_data2])
        linked_tc = tclib_library.testcases['Additional Testcase 2']
        linked_req = tclib_library.requirements['Additional Requirement']
        linked_tp = tclib_library.testplans['Additional Testplan']
        # Check testing data is still valid (Additional Testcase 2 is not linked to other requirement)
        self.assertEquals(linked_tc.verifiesRequirement, [linked_req])
        # Verify links between additional structures work
        self.assertIn(linked_tc, linked_req.verificationTestCases)
        self.assertIn(linked_tc, linked_tp.verificationTestCases)
