import unittest

import msr_parser_main
from msr_parser_code.utility import DownloadMethod, SongSearchMetadata, MSRSongDataAPIFull, MSRSongDataAPIPartial, MSRAlbumDataAPIFull, MSRMasterListAlbums, MSRMasterListSongs
import msr_parser_code.utility as utility


def helper_parse_to_name(songs: list[SongSearchMetadata]) -> list[str]:
    song_names=[]
    
    for song in songs:
        song_names.append(song['song_data']['name'])
    return song_names


class TestSearch(unittest.TestCase):
    '''
        test main file search methods (i.e search for matching names/cID)
        NOTE each test method should should test using provided name AND the equivalent cID for full coverage (and also to avoid having alot of test methodds)
    '''
    
    @classmethod
    def setUpClass(cls):
        '''
        NOTE SETUP THE EXPECTED DICT TO COMPARE TO HERE
        '''
        cls.expected_songs_found: list[SongSearchMetadata] = [] #empty by default NVM actually
 
    def test_defaults(self):
        '''
        Case: if no arguments were specified and only a name was provided 

        Provided Args:
        - Default Search
        - Default Exactness
        - Name "Battleplan Obliteration" OR "CID

        Expected: Return 1 Song:
            Battleplan Obliteration
        '''

        search_args_name = utility.SearchArguments(search_term="Battleplan Obliteration") #DEFAULTS
        search_args_cid = utility.SearchArguments(search_term="697687") #DEFAULTS

        songs_found_name = helper_parse_to_name(msr_parser_main.search_songs(
            search_method= search_args_name.mode, 
            exact = search_args_name.exact, 
            name= search_args_name.search_term
        ))

        songs_found_cid = helper_parse_to_name(msr_parser_main.search_songs(
            search_method= search_args_cid.mode, 
            exact = search_args_cid.exact, 
            name= search_args_cid.search_term
        ))

        self._expected_songs_found = [ 
            "Battleplan Obliteration"
        ]

        self.assertCountEqual(songs_found_name, self._expected_songs_found)
        self.assertCountEqual(songs_found_cid, self._expected_songs_found)

    def test_album_exact(self):
        '''
        Case: Cases for every Search Album 

        '''
        search_args_name = utility.SearchArguments(exact=True,mode= DownloadMethod.ALBUM, search_term="涤墨作战OST") #name exists
        songs_found_name = helper_parse_to_name(msr_parser_main.search_songs(
            search_method= search_args_name.mode, 
            exact = search_args_name.exact, 
            name= search_args_name.search_term
        ))
        self._expected_songs_found = [ 
            "Battleplan Obliteration",
            "Battleplan Obliteration (Instrumental)",
            "Swelling Ink"
        ]
        self.assertCountEqual(songs_found_name, self._expected_songs_found)

        search_args_name_incorrect = utility.SearchArguments(exact=True,mode= DownloadMethod.ALBUM, search_term="涤墨作OST") #name doesn't exist
        songs_found_name_incorrect = helper_parse_to_name(msr_parser_main.search_songs(
            search_method= search_args_name_incorrect.mode, 
            exact = search_args_name_incorrect.exact, 
            name= search_args_name_incorrect.search_term
        ))
        self._expected_songs_found = []
        self.assertCountEqual(songs_found_name_incorrect, self._expected_songs_found)

        search_args_cid = utility.SearchArguments(exact=True,mode= DownloadMethod.ALBUM, search_term="697687") #cID exists
        songs_found_cid = helper_parse_to_name(msr_parser_main.search_songs(
            search_method= search_args_cid.mode, 
            exact = search_args_cid.exact, 
            name= search_args_cid.search_term
        ))
        self._expected_songs_found = [ 
            "Battleplan Obliteration",
            "Battleplan Obliteration (Instrumental)",
            "Swelling Ink"
        ]
        self.assertCountEqual(songs_found_cid, self._expected_songs_found)

        search_args_cid_incorrect = utility.SearchArguments(exact=True,mode= DownloadMethod.ALBUM, search_term="666666") #cID doesn't exist
        songs_found_cid_incorrect = helper_parse_to_name(msr_parser_main.search_songs(
            search_method= search_args_cid_incorrect.mode, 
            exact = search_args_cid_incorrect.exact, 
            name= search_args_cid_incorrect.search_term
        ))
        self._expected_songs_found = []
        self.assertCountEqual(songs_found_cid_incorrect, self._expected_songs_found)

        
        
        
    
class TestMain(unittest.TestCase):
    '''
    stub, test main file related methods (i.e does arg parser work)
    '''
    pass

class TestFullEndToEnd(unittest.TestCase):
    '''
    stub, test the entire thing end to end (i.e can it successfully run the entire thing and download the correct files/convert them given correct parameters)
    '''
    pass
