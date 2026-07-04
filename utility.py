from enum import Enum

class DownloadMethod(Enum):
    SINGLE = "single"
    ALBUM = "album"
    METADATA_ONLY_SINGLE = "metadata_only_single" #option to simply download the song's cover image as a image file as well as a text file containing relevant metadata 

class FileFormat(Enum):
    FLAC = "flac"
    MP3 = "mp3"
    WAV = "wav"
    OGG = "ogg"