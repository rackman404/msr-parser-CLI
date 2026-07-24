

import sys
import unittest
from unittest import mock

from msr_parser_code import utility
from msr_parser_code import arg_parse

class TestArgParse(unittest.TestCase):
    '''
        test arg parse public method

        NOTE apparently just testing the search term or no terms was enough for 100% coverage (still test other possible scenarios as well)

        https://stackoverflow.com/questions/39028204/using-unittest-to-test-argparse-exit-errors
    '''

    @classmethod
    def setUpClass(cls):
        '''

        '''
        
        cls._no_args = []
        cls.search_term_only = ['missy']
        cls.help = ['-h']
        cls.mispelled_arg = ['missy', '-m', 'singe']
        cls.multple_arg = ['missy', '-m', 'album', '-f', 'mp3', '--nolyrics', '-w']
        
    def test_no_args(self):    
        '''should exit application on no args'''
        with self.assertRaises(SystemExit):
            arg_parse.parse_args(self._no_args)

    def test_search_term_only(self):    
        '''only search term should be altered as a argument'''
        expected_args = utility.ProgramArguments()
        parsed = arg_parse.parse_args(self.search_term_only)
        expected_args.search_args.search_term = 'missy'

        #search term should've been set and nothing else
        self.assertEqual(parsed.search_args, expected_args.search_args) 
        self.assertEqual(parsed.download_args, expected_args.download_args) 
        self.assertEqual(parsed.convert_args, expected_args.convert_args) 
        self.assertEqual(parsed.metadata_args, expected_args.metadata_args) 

    def test_help(self):    
        '''should exit application on -h flag'''
        with self.assertRaises(SystemExit):
            arg_parse.parse_args(self.help)

    def test_mispelled_arg(self):    
        '''should exit application on -h flag'''
        with self.assertRaises(SystemExit):
            arg_parse.parse_args(self.mispelled_arg)

    def test_multiple_arg(self):    
        '''should be capable of handling multiple args and flags set'''
        expected_args = utility.ProgramArguments()
        parsed = arg_parse.parse_args(self.multple_arg)
        expected_args.search_args.search_term = 'missy'
        expected_args.search_args.mode = utility.DownloadMethod.ALBUM
        expected_args.download_args.lyrics = False
        expected_args.metadata_args.watermark = True
        expected_args.convert_args.convert_format = utility.FileFormat.MP3

        self.assertEqual(parsed.search_args, expected_args.search_args) 
        self.assertEqual(parsed.download_args, expected_args.download_args) 
        self.assertEqual(parsed.convert_args, expected_args.convert_args) 
        self.assertEqual(parsed.metadata_args, expected_args.metadata_args) 


    @classmethod
    def tearDownClass(cls):
        #TODO figure out what actually has to be teared down 
        #cls._expected_args = None
        ...