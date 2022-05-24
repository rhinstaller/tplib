import unittest
import copy
from distutils import dir_util
import os
import yaml
from tempfile import mkdtemp
from tplib import library


class DiffBase():
    @classmethod
    def setUpClass(cls):
        cls.library_dir = './data/baselib'
        cls.baselib = library.Library(cls.library_dir)
        cls.no_changes = {
            'removed': {'testplans': set(),
                        'requirements': set(),
                        'testcases': set()},
            'added': {'testplans': set(),
                      'requirements': set(),
                      'testcases': set()},
            'modified': {'testplans': set(),
                         'requirements': set(),
                         'testcases': set()},
            'unchanged': {'testplans': {'Main parent plan', 'Sub plan A', 'Plan B'},
                          'requirements': {'Running', 'Electronics', 'Controls'},
                          'testcases': {'Ignition', 'Engine quality', 'Engine fuel consumption', 'Steering wheel'}}
        }

    def setUp(cls):
        cls.modified_library_dir = mkdtemp()
        dir_util.copy_tree(cls.library_dir, cls.modified_library_dir)
        cls.expected = copy.deepcopy(cls.no_changes)

    def test_diff(cls):
        difference = library.diff(cls.baselib, cls.testlib)
        cls.assertEqual(cls.expected, difference)

    def tearDown(cls):
        dir_util.remove_tree(cls.modified_library_dir)

class TestRemovedTestcase(DiffBase, unittest.TestCase):
    def setUp(self):
        super().setUp()
        # Remove testcase 'Engine fuel consumption'
        os.remove(os.path.join(self.modified_library_dir, 'engine_consumption.tc.yaml'))

        self.testlib = library.Library(self.modified_library_dir)

        self.expected['removed']['testcases'] = {'Engine fuel consumption'}
        self.expected['unchanged']['testcases'].remove('Engine fuel consumption')
        self.expected['unchanged']['testplans'].remove('Sub plan A')
        self.expected['unchanged']['requirements'].remove('Running')
        self.expected['modified']['testplans'].add('Sub plan A')
        self.expected['modified']['requirements'].add('Running')

class TestAddedTestcase(DiffBase, unittest.TestCase):
    def setUp(self):
        super().setUp()
        # Remove testcase 'Engine fuel consumption'
        os.remove(os.path.join(self.modified_library_dir, 'engine_consumption.tc.yaml'))

        self.testlib = library.Library(self.modified_library_dir)

        self.expected['added']['testcases'] = {'Engine fuel consumption'}
        self.expected['unchanged']['testcases'].remove('Engine fuel consumption')
        self.expected['unchanged']['testplans'].remove('Sub plan A')
        self.expected['unchanged']['requirements'].remove('Running')
        self.expected['modified']['testplans'].add('Sub plan A')
        self.expected['modified']['requirements'].add('Running')

    def test_diff(self):
        difference = library.diff(self.testlib, self.baselib)
        self.assertEqual(self.expected, difference)

class TestModifiedTestcase(DiffBase, unittest.TestCase):
    def setUp(self):
        super().setUp()
        # Modify testcase 'Ignition'
        with open(os.path.join(self.modified_library_dir, 'ignition.tc.yaml'), 'r+') as tcfile:
            tc = yaml.safe_load(tcfile)
            tc['instructions']['steps'].append({'step': 'Disconnect'})
            yaml.safe_dump(tc, tcfile)

        self.testlib = library.Library(self.modified_library_dir)

        self.expected['unchanged']['testcases'].remove('Ignition')
        self.expected['modified']['testcases'] = {'Ignition'}

class TestRemovedTestplan(DiffBase, unittest.TestCase):
    def setUp(self):
        super().setUp()
        # Remove testplan 'Sub plan A'
        os.remove(os.path.join(self.modified_library_dir, 'sub_a.plan.yaml'))

        self.testlib = library.Library(self.modified_library_dir)

        self.expected['removed']['testplans'].add('Sub plan A')
        self.expected['unchanged']['testplans'].remove('Sub plan A')

class TestAddedTestplan(DiffBase, unittest.TestCase):
    def setUp(self):
        super().setUp()
        # Remove testplan 'Sub plan A'
        os.remove(os.path.join(self.modified_library_dir, 'sub_a.plan.yaml'))

        self.testlib = library.Library(self.modified_library_dir)

        self.expected['added']['testplans'].add('Sub plan A')
        self.expected['unchanged']['testplans'].remove('Sub plan A')

    def test_diff(self):
        difference = library.diff(self.testlib, self.baselib)
        self.assertEqual(self.expected, difference)

class TestModifiedTestplan(DiffBase, unittest.TestCase):
    def setUp(self):
        super().setUp()
        # Modify testplan 'Sub plan A'
        with open(os.path.join(self.modified_library_dir, 'sub_a.plan.yaml'), 'r+') as tcfile:
            tc = yaml.safe_load(tcfile)
            tc['acceptance_criteria']['test_cases']['query'] = '"engine" in tc.tags and "disabled" not in tc.tags and tc.priority > 3'
            yaml.safe_dump(tc, tcfile)

        self.testlib = library.Library(self.modified_library_dir)

        self.expected['unchanged']['testplans'].remove('Sub plan A')
        self.expected['modified']['testplans'].add('Sub plan A')

class TestRemovedRequirement(DiffBase, unittest.TestCase):
    def setUp(self):
        super().setUp()
        # Removed requirement 'Running'
        os.remove(os.path.join(self.modified_library_dir, 'running.req.yaml'))

        self.testlib = library.Library(self.modified_library_dir)

        self.expected['unchanged']['requirements'].remove('Running')
        self.expected['removed']['requirements'].add('Running')
        # Testcases have verifiesRequirement
        self.expected['modified']['testcases'] = {'Ignition', 'Engine quality', 'Engine fuel consumption'}
        self.expected['unchanged']['testcases'].remove('Ignition')
        self.expected['unchanged']['testcases'].remove('Engine quality')
        self.expected['unchanged']['testcases'].remove('Engine fuel consumption')

class TestAddedRequirement(DiffBase, unittest.TestCase):
    def setUp(self):
        super().setUp()
        # Removed requirement 'Running'
        os.remove(os.path.join(self.modified_library_dir, 'running.req.yaml'))

        self.testlib = library.Library(self.modified_library_dir)

        self.expected['unchanged']['requirements'].remove('Running')
        self.expected['added']['requirements'].add('Running')
        # Testcases have verifiesRequirement
        self.expected['modified']['testcases'] = {'Ignition', 'Engine quality', 'Engine fuel consumption'}
        self.expected['unchanged']['testcases'].remove('Ignition')
        self.expected['unchanged']['testcases'].remove('Engine quality')
        self.expected['unchanged']['testcases'].remove('Engine fuel consumption')

    def test_diff(self):
        difference = library.diff(self.testlib, self.baselib)
        self.assertEqual(self.expected, difference)

class TestModifiedRequirement(DiffBase, unittest.TestCase):
    def setUp(self):
        super().setUp()
        # Modified requirement 'Running'
        with open(os.path.join(self.modified_library_dir, 'running.req.yaml'), 'r+') as tcfile:
            tc = yaml.safe_load(tcfile)
            tc['verified_by'].pop('direct_list')
            yaml.safe_dump(tc, tcfile)

        self.testlib = library.Library(self.modified_library_dir)

        self.expected['unchanged']['requirements'].remove('Running')
        self.expected['modified']['requirements'].add('Running')
        # Testcases have verifiesRequirement
        self.expected['modified']['testcases'].add('Ignition')
        self.expected['unchanged']['testcases'].remove('Ignition')
