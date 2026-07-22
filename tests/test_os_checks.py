import unittest
from unittest import mock
import os.path

import msr_parser_code.os_checks as os_checks


#Main test suite for OS Check dependency method
class TestOSChecksDeps(unittest.TestCase):
    '''
    test methods defined in os_checks.py
    Perform mock testing on OS file detection
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

    @mock.patch.dict(os.environ, {})
    def test_both_are_not_defined(self):
        '''
        Case: if there is no dependencies specified at all
        '''
        self.assertEqual(os_checks.check_deps(self._sample_dependency_dict), None) #should just pass back a empty dict, since the program clearly doesn't rely on any dependencies its fine

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

    @mock.patch('msr_parser_code.os_checks.os.path.isfile' , side_effect=Exception())
    def test_user_dep_check_exception(self, os_mock_exists: mock.MagicMock):
        '''
        Case: exception raised at any point, returns nothing
        '''
        os_mock_exists.return_value = Exception() #raised exception checking folders
        self.assertEqual(os_checks.check_deps(self._sample_dependency_dict), None) #we expect NOTHING to be returned (exception occured)

    @classmethod
    def tearDownClass(cls):
        cls._sample_dependency_dict = None

def side_effect(arg):
    if arg == 1:
        return True
    else:
        return False

def side_effect(arg):
    if arg == 1:
        return True
    else:
        return False
    
#Main test suite for OS Check folder methods
class TestOSChecksFolders(unittest.TestCase):
    '''
    test methods defined in os_checks.py
    Perform mock testing folder detection/creation utility methods defined in program
    
    https://stackoverflow.com/questions/32187967/using-mock-to-test-if-directory-exists-or-not
    https://stackoverflow.com/questions/32748212/how-to-test-a-function-that-creates-a-directory

    https://stackoverflow.com/questions/7242433/asserting-successive-calls-to-a-mock-method
    '''
    
    @classmethod
    def setUpClass(cls):
        '''
        NOTE i am trying to test the behaviours of loading paths IF they exist in file system or ENV, thus we should have the same exact 
        deps locations passed in have mock.patch determine if said locations actually exist or not
        '''
        cls._folder_paths = {
            "DATA_DOWNLOAD_FOLDER_PATH": os.path.abspath(os.path.join("./root", "output/")), #NOTE THIS SHOULD ACTUALLY CHANGE IN WORKING_FOLDER_PATHS IF USER PASSES A CUSTOM ONE IN
            "CACHE_DOWNLOAD_SONG_FOLDER_PATH": os.path.abspath(os.path.join("./root", "cache/")),
            "CACHE_SONG_DOWNLOAD_SONG_FOLDER_PATH": os.path.abspath(os.path.join("./root", "cache/songs/")),
            "DEPENDENCIES_FOLDER_PATH": os.path.abspath(os.path.join("./root", "deps/")),
        }

        cls._user_folder_output_path = os.path.abspath(os.path.join("./user", "music/raw"))

        #cls._folder_paths_names = list(cls._folder_paths.values())

        #create mock call objects for all folder paths
        cls._folder_paths_names_calls = []
        for x in cls._folder_paths.values():
            cls._folder_paths_names_calls.append(mock.call(x)) 
        

    @mock.patch('msr_parser_code.os_checks.os.path.exists')
    @mock.patch('msr_parser_code.os_checks.os.makedirs')
    def test_all_folders_exist(self, os_mock_make_folders: mock.MagicMock, os_mock_exists: mock.MagicMock):
        os_mock_exists.return_value = True #every folder exists

        ret = os_checks.create_folders(self._folder_paths)
        #os_mock_make_folders.assert_called_with(self._folder_paths["DEPENDENCIES_FOLDER_PATH"]) 
        os_mock_make_folders.assert_not_called() # We expect NO CALLS to making folder 
        self.assertEqual(ret, self._folder_paths) #No change in folder path expected

    @mock.patch('msr_parser_code.os_checks.os.path.exists')
    @mock.patch('msr_parser_code.os_checks.os.makedirs')
    def test_all_folders_no_exist(self, os_mock_make_folders: mock.MagicMock, os_mock_exists: mock.MagicMock):
        os_mock_exists.return_value = False #assuming no folders exist

        ret = os_checks.create_folders(self._folder_paths)
        #os_mock_make_folders.assert_has_calls([mock.call(self._folder_paths.get("DATA_DOWNLOAD_FOLDER_PATH")), 
        #                                       mock.call(self._folder_paths.get("CACHE_DOWNLOAD_SONG_FOLDER_PATH")), 
        #                                       mock.call(self._folder_paths.get("CACHE_SONG_DOWNLOAD_SONG_FOLDER_PATH")), 
        #                                       mock.call(self._folder_paths.get("DEPENDENCIES_FOLDER_PATH"))], any_order=True) 
        os_mock_make_folders.assert_has_calls(self._folder_paths_names_calls, any_order=True) 
        
        self.assertEqual(ret, self._folder_paths) #No change in folder path expected

    @mock.patch('msr_parser_code.os_checks.os.path.exists')
    @mock.patch('msr_parser_code.os_checks.os.makedirs')
    def test_user_output_folder_set_and_exists(self, os_mock_make_folders: mock.MagicMock, os_mock_exists: mock.MagicMock):
        os_mock_exists.return_value = True #assuming user folder exits TODO make it so specifically ensure that user folder exists

        ret = os_checks.create_folders(self._folder_paths, self._user_folder_output_path)
        os_mock_make_folders.assert_not_called() #ensure folder creation didn't happen
        
        self.assertEqual(ret["DATA_DOWNLOAD_FOLDER_PATH"], self._user_folder_output_path) #we expect that the data download folder path to be replaced by the user defined one

    @mock.patch('msr_parser_code.os_checks.os.path.exists')
    @mock.patch('msr_parser_code.os_checks.os.makedirs')
    def test_user_output_folder_set_and_not_exists(self, os_mock_make_folders: mock.MagicMock, os_mock_exists: mock.MagicMock):
        os_mock_exists.return_value = False #assuming user folder exits TODO make it so specifically ensure that user folder doesn't exists

        ret = os_checks.create_folders(self._folder_paths, self._user_folder_output_path)
        #os_mock_make_folders.assert_not_called() #NOTE doesn't matter, program should terminate anyways
        
        self.assertEqual(ret, None) #we expect NOTHING to be returned (which indicates that program should terminate and user should set a proper one on their end)

    @mock.patch('msr_parser_code.os_checks.os.path.exists' , side_effect=Exception())
    @mock.patch('msr_parser_code.os_checks.os.makedirs')
    def test_user_output_folder_exception(self, os_mock_make_folders: mock.MagicMock, os_mock_exists: mock.MagicMock):
        '''
        Case: exception raised at any point, returns nothing
        '''
        os_mock_exists.return_value = Exception() #raised exception checking folders
        ret = os_checks.create_folders(self._folder_paths, self._user_folder_output_path)
        self.assertEqual(ret, None) #we expect NOTHING to be returned (exception occured)

    @classmethod
    def tearDownClass(cls):
        cls._sample_dependency_dict = None


    

    

