

import sys
import unittest
from unittest import mock

from msr_parser_code import utility
from msr_parser_code import arg_parse

class TestArgParse(unittest.TestCase):
    '''
        test arg parse public method

        NOTE apparently just testing the search term or no terms was enough for 100% coverage

        https://stackoverflow.com/questions/39028204/using-unittest-to-test-argparse-exit-errors
    '''

    @classmethod
    def setUpClass(cls):
        '''

        '''
        cls._expected_args = utility.ProgramArguments()
        
        cls._no_args = []
        cls.search_term_only = ['missy']
        

   #def test_no_args(self):    
    #    with self.assertRaises(SystemExit):
    #        arg_parse.parse_args(self._no_args)

    def test_search_term_only(self):    
        parsed = arg_parse.parse_args(self.search_term_only)
        self._expected_args.search_args.search_term = 'missy'
        self.assertEqual(parsed.search_args.search_term, self._expected_args.search_args.search_term)

    @classmethod
    def tearDownClass(cls):
        cls._expected_args = None