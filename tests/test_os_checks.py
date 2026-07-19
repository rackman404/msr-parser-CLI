import unittest
from unittest import mock
import os.path

import msr_parser_code.os_checks as os_checks


#Main test suite for OS Check script methods
class TestOSChecks(unittest.TestCase):
    '''
    test methods defined in os_checks.py
    Perform mock testing on OS file detection and folder detection/creation utility methods defined in program
    '''

    @classmethod
    def setUpClass(cls):
        '''
        NOTE i am trying to test the behaviours of loading paths IF they exist in file system or ENV, thus we should have the same exact 
        deps locations passed in have mock.patch determine if said locations actually exist or not
        '''
        cls._sample_dependency_dict = {
            "foo":{"relative_path": "relpath", "env_var": "foo"}
        }


    def test_no_files_at_all(self):
        '''
        Case: if there is no dependencies specified at all
        '''
        self.assertEqual(os_checks.check_deps({}), {}) #should just pass back a empty dict, since the program clearly doesn't rely on any dependencies its fine
    
    @mock.patch.dict(os.environ, {"foo": "envpath"})
    def test_dep_exists_in_ENV_and_rel(self):
        '''
        Case: if a dependency exists in the relative pathing (with a vaild os.path.isfile) AND env pathing
        '''

        #https://stackoverflow.com/questions/19672138/how-do-i-mock-the-filesystem-in-python-unit-tests
        os.path.isfile = lambda path: path == "relpath" # mock a valid isfile
        correct_dict = {"foo": "relpath"}

        self.assertEqual(os_checks.check_deps(self._sample_dependency_dict), correct_dict) #should pass a dict showing {"foo": "relpath"}, since we prioritize that over the ENV one

    @mock.patch.dict(os.environ, {})
    def test_dep_exists_in_rel(self):
        '''
        Case: if a dependency exists only in relative pathing 
        '''
        os.path.isfile = lambda path: path == "relpath"  
        correct_dict = {"foo": "relpath"}

        self.assertEqual(os_checks.check_deps(self._sample_dependency_dict), correct_dict) #should pass a dict showing {"foo": "relpath"}, since only rel has a path

    @mock.patch.dict(os.environ, {"foo": "envpath"})
    def test_dep_exists_in_env(self):
        '''
        Case: if a dependency exists only in env
        '''
        os.path.isfile = lambda path: path == "" 
        correct_dict = {"foo": "envpath"}

        self.assertEqual(os_checks.check_deps(self._sample_dependency_dict), correct_dict) #should pass a dict showing {"foo": "envpath"}, since only rel has a path

    @classmethod
    def tearDownClass(cls):
        cls._sample_dependency_dict = None


    #NOTE we will not be testing the folder creation method, this should literally always work since either it creates the folders, or they already exist (same behaviour is expected when given a user defined folder)

    

