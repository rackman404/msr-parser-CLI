from enum import Enum
from typing import TypedDict #using this for type hinting in dicts
from dataclasses import dataclass #using this cause i don't wanna create init and stuff for simple data classes (so that i can access data using dot notation on class attribute)


class DownloadMethod(Enum):
    SINGLE = "single"
    ALBUM = "album"
    ALL = "all"

    def __str__(self):
        return self.value
    
class FileFormat(Enum):
    FLAC = "flac"
    MP3 = "mp3"
    WAV = "wav"
    OGG = "ogg"

    def __str__(self):
        return self.value

@dataclass
class SearchArguments:
    # search specific
    search_term: str
    mode: DownloadMethod = DownloadMethod.SINGLE
    exact: bool = True

@dataclass
class DownloadArguments:
    # download specific
    lyrics: bool = True

@dataclass
class MetadataArguments:
    # download specific
    watermark: bool = False

@dataclass
class ConversionArguments:
    # ffmpeg/metadata specific
    convert_format: FileFormat = FileFormat.WAV  
    add_metadata: bool = True # add metadata data at all
    music_brainz: bool = True # use music brainz api to fill missing metadata fields and add missing artists
    
@dataclass
class ProgramArguments:
    '''
    Below are the specified program arguments,  
    '''
    search_args: SearchArguments
    convert_args: ConversionArguments
    download_args: DownloadArguments
    metadata_args: MetadataArguments

    #common args below
    
    pass




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
    pass

class MSRSongDataAPIPartial(TypedDict):
    '''
        What MSR uses for their partial song data entry JSONs (from within the master list of songs)
    '''
    cid: str
    name: str
    albumCid: str
    artists: list[str]
    pass


class MSRAlbumDataAPIFull(TypedDict):
    '''
        What MSR uses for their full album data entry JSONs (from within the master list of albums)
    '''
    cid: str
    name: str
    coverUrl: str
    artistes: list[str]
    pass

#NOTE MASTER LISTS
class MSRMasterListDataSong(TypedDict):
    list: list[MSRSongDataAPIPartial]
    autoplay: str

#class MSRMasterListDataAlbum(TypedDict):
#    data: list[MSRAlbumDataAPIFull]

class MSRMasterListSongs(TypedDict):
    code: int
    msg: str
    data: MSRMasterListDataSong

class MSRMasterListAlbums(TypedDict):
    code: int
    msg: str
    data: list[MSRAlbumDataAPIFull]

###

class SongSearchMetadata(TypedDict):
    '''
    What should be returned when searching for song data
    '''
    song_data: MSRSongDataAPIPartial  #NOTE incomplete song data from master list HERE
    songMetaData: MSRSongDataAPIFull #NOTE To be Added in later step
    albumName: str
    albumArtists: str
    coverImgUrl: str


