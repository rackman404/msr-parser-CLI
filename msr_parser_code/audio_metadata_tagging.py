"""
Metadata Tagging Module

Supports Vorbis Comments for FLAC and ogg
Supports ID3V2 for mp3

Does not support tags for WAV
"""
from mutagen.flac import FLAC, Picture
#TODO IMPLEMENT from mutagen.mp3 import MP3
from mutagen.id3 import ID3

from msr_parser_code.utility import FileFormat
from msr_parser_code import console_gui_utils

#TODO Implement this
def _music_brainz_(song_name: str, song_artist: list[str]) -> dict:
    '''
    NOTE according to their API, we should not make more than 1 call per second, 
    if this is the case, 
    simply wait for 1-2 seconds then make the call (also show this in the GUI)

    refs
    https://musicbrainz.org/doc/MusicBrainz_API
    https://musicbrainz.org/doc/MusicBrainz_API/Rate_Limiting
    '''

def add_metadata(
        file_path: str,
        file_format: FileFormat,
        metadata: dict,
        cover_img_path: str,
        watermark: bool) -> bool:
    '''
    We note that metadata structure either follows guidelines such as 
    https://xiph.org/vorbis/doc/v-comment.html 
    for .FLAC and .ogg or ID3V2 official structure. In addition regardless of file type, 
    this method should ensure that metadata should match with each other as much as possible.

    Some metadata is to be directly inputted using the metadata and cover_img_path parameters 
    however others such as genre or language should make use of some other form of recognition
    to be inputted into the files.

    refs:
    https://mutagen.readthedocs.io/ 
    https://xiph.org/vorbis/doc/v-comment.html
    https://id3.org/id3v2.3.0 
    https://docs.mp3tag.de/mapping/ 

    TODO genres, languages, etc... . These may require the use of some form of neural network stuff
    '''

    try:
        audio = None
        match file_format.value:
            case FileFormat.FLAC.value:
                print ("Adding Vorbis Comments (.FLAC)")
                audio = FLAC(file_path)

                audio["title"] = metadata["songMetaData"]["name"]
                #NOTE should also perform an extra check where if OST is not mentioned,
                #it should also write <Album Name> Single at the end
                audio["album"] = metadata["albumName"]

                #HARD CODED METADATA FIELDS
                #(should not change as all songs here is probably Hypergryph IP)
                #NOTE none of these should have their own try except block
                #as it shouldn't be possible for there to be a exception here
                audio["copyright"] = "Shanghai Hypergryph Network Technology Co., Ltd."
                audio["publisher"] = "Shanghai Hypergryph Network Technology Co., Ltd."
                audio["label"] = "Shanghai Hypergryph Network Technology Co., Ltd."
                audio["organization"] = "Shanghai Hypergryph Network Technology Co., Ltd."

                audio["contact"] = "Shanghai Hypergryph Network Technology Co., Ltd.,"\
                "Room 504-1, 799 Yinxiang Road, Jiading District, Shanghai, China"

                audio["releaseStatus"] = "Official" #songs come from hypergryph itself
                audio["media"] = "Digital Media" #songs are digitally released
                audio["license"] = "All Rights Reserved" #to Hypergryph that is

                #i saw these under properties
                #songs extracted from this website
                audio["contentUrl"] = "https://monster-siren.hypergryph.com"
                #idk if this should be the same as contentUrl
                audio["authorUrl"] = "https://monster-siren.hypergryph.com"
                #technically used in game but promoted through their own music website
                audio["promotionUrl"] = "https://monster-siren.hypergryph.com"

                if watermark is True: #watermark the file if set to true
                    audio["comment"] = "Audio file extracted from "\
                        "https://monster-siren.hypergryph.com's"\
                        "public API using https://github.com/rackman404/msr-parser-CLI,"\
                        "all rights reserved to Hypergryph itself"

                #NOTE i have no clue if hypergryph actually has different fields for both
                #album and song artists but to make sure, we we will do a union operation on both lists.
                all_artists_union_set =  set(metadata["songMetaData"]['artists']) | set(metadata['albumArtists'])
                all_artists = list (all_artists_union_set)
                #TODO idk if the MSR artist (important for consistancy) is always the very first option if we do this,
                #TODO maybe manually rearrange it to the very first element as required

                audio["artist"] = all_artists
                #audio["artist"] = metadata["songMetaData"]["name"] non union operation

                #maybe also define the dimensions of image and what not
                image = Picture()
                image.type = 3
                image.desc = "Front Cover"
                image.mime = "image/png"

                with open(cover_img_path, 'rb') as img_dat:
                    image.data = img_dat.read()

                audio.add_picture(image)

                audio.save(file_path) #save the metadata back to the file
            case FileFormat.MP3.value:
                audio = ID3(file_path)
    except Exception as e:
        console_gui_utils.console_print_err("THERE WAS A ERROR CONVERTING METADATA: " + str(e))
        return

    console_gui_utils.console_print_success("Successfully song inputted metadata (title, cover image, etc..) into song file")

    #print (file_path)
    #audio = FLAC(file_path)
    #print (audio.pprint())
    #print (audio)
    #print (file_format)
