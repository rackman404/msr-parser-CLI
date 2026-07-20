"""
Data class definitions and enums used as program arguments
and by other modules
"""

from enum import Enum
from typing import TypedDict #using this for type hinting in dicts

#using this cause i don't wanna create init and stuff for simple data classes
#(so that i can access data using dot notation on class attribute)
from dataclasses import dataclass

class DownloadMethod(Enum):
    '''Possible search options when downloading'''
    SINGLE = "single"
    ALBUM = "album"
    ALL = "all"

    def __str__(self):
        return self.value

class FileFormat(Enum):
    '''Supported formats for converting wav -> new file format'''
    FLAC = "flac"
    MP3 = "mp3"
    WAV = "wav"
    OGG = "ogg"

    def __str__(self):
        return self.value

@dataclass
class SearchArguments:
    '''Search arguments for search module'''
    search_term: str
    mode: DownloadMethod = DownloadMethod.SINGLE
    exact: bool = True

@dataclass
class DownloadArguments:
    '''download arguments for download module'''
    lyrics: bool = True

@dataclass
class MetadataArguments:
    '''metadata arguments for metadata module'''
    watermark: bool = False

@dataclass
class ConversionArguments:
    '''conversion arguments for ffmpeg module'''
    # ffmpeg/metadata specific
    convert_format: FileFormat = FileFormat.WAV
    add_metadata: bool = True # add metadata data at all
    music_brainz: bool = True # use music brainz api to fill missing metadata fields

@dataclass
class ProgramArguments:
    '''
    Container for all pipeline specific arguments.
    Also contains common arguments for overall workflow
    '''
    search_args: SearchArguments
    convert_args: ConversionArguments
    download_args: DownloadArguments
    metadata_args: MetadataArguments

    #common args below
    user_confirmation: bool = True #true for requires confirmation

###
#NOTE SCHEMA DEFINITIONS

class MSRSongDataAPIFull(TypedDict):
    '''
    What MSR uses for their full song data JSONs
    '''
    data: str
    name: str
    albumCid: str
    sourceUrl: str
    lyricUrl: str
    mvUrl: str
    mvCoverUrl: str
    artists: list[str]

class MSRSongDataAPIPartial(TypedDict):
    '''
    What MSR uses for their partial song data entry JSONs (from within the master list of songs)
    '''
    cid: str
    name: str
    albumCid: str
    artists: list[str]

class MSRAlbumDataAPIFull(TypedDict):
    '''
    What MSR uses for their full album data entry JSONs (from within the master list of albums)
    '''
    cid: str
    name: str
    coverUrl: str
    artistes: list[str]

#NOTE MASTER LISTS
class MSRMasterListDataSong(TypedDict):
    '''
    Typed dict formatting for master JSON list
    '''
    list: list[MSRSongDataAPIPartial]
    autoplay: str

class MSRMasterListSongs(TypedDict):
    '''
    Typed dict formatting for song JSON
    '''
    code: int
    msg: str
    data: MSRMasterListDataSong

class MSRMasterListAlbums(TypedDict):
    '''
    Typed dict formatting for album JSON
    '''
    code: int
    msg: str
    data: list[MSRAlbumDataAPIFull]

class SongSearchMetadata(TypedDict):
    '''
    What should be returned when searching for song data
    '''
    song_data: MSRSongDataAPIPartial  #NOTE incomplete song data from master list HERE
    songMetaData: MSRSongDataAPIFull #NOTE To be Added in later step
    albumName: str
    albumArtists: str
    coverImgUrl: str
