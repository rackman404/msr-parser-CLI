import mutagen

from mutagen.flac import FLAC, Picture
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TCON, TPUB, TLAN, TCOP, TRCK, APIC

from mutagen.oggvorbis import OggVorbis
from mutagen.flac import Picture, error as FLACError

from enum import Enum

from utility import FileFormat 
import console_gui_utils



def music_brainz_(song_name: str, song_artist: list[str]) -> dict:
    '''

    NOTE according to their API, we should not make more than 1 call per second, if this is the case, simply wait for 1-2 seconds then make the call (also show this in the GUI)

    refs
    - https://musicbrainz.org/doc/MusicBrainz_API
    - https://musicbrainz.org/doc/MusicBrainz_API/Rate_Limiting
    '''
    pass

def add_metadata(file_path: str, file_format: FileFormat, metadata: dict, cover_img_path: str, watermark: bool) -> bool:
    '''
    We note that metadata structure either follows guidelines such as https://xiph.org/vorbis/doc/v-comment.html for .FLAC and .ogg or ID3V2 official structure.
    In addition regardless of file type, this method should ensure that metadata should match with each other as much as possible.

    Some metadata is to be directly inputted using the metadata and cover_img_path parameters however others such as genre or language should make use of some other form of recognition
    to be inputted into the files.

    refs:
    - https://mutagen.readthedocs.io/ 
    - https://xiph.org/vorbis/doc/v-comment.html
    - https://id3.org/id3v2.3.0 
    - https://docs.mp3tag.de/mapping/ 

    TODO genres, languages, etc... . These may require the use of some form of neural network stuff
    '''

    try:
        audio = None
        #print (file_format.value == FileFormat.FLAC.value) #NOTE (FIX LATER) I HAVE NO CLUE WHY THE OBJECT ITSELF CANNOT BE COMPARED CORRECTLY IN THIS SEPARATE FILE COMPARED TO MAIN FILE,
        match file_format.value:
            case FileFormat.FLAC.value:
                print ("Adding Vorbis Comments (.FLAC)")  
                audio = FLAC(file_path)

                audio["title"] = metadata["songMetaData"]["name"]
                audio["album"] = metadata["albumName"] #NOTE should also perform an extra check where if OST is not mentioned, it should also write <Album Name> Single at the end

                #HARD CODED METADATA FIELDS (should not change given that every song hosted on their content servers is probably made/commissioned and owned by hypergryph)
                #NOTE none of these should have their own try except block as it shouldn't be possible for there to be a exception here
                audio["copyright"] = u"Shanghai Hypergryph Network Technology Co., Ltd." #assuming every song probably does belong to hypergryph
                
                audio["publisher"] = u"Shanghai Hypergryph Network Technology Co., Ltd." #assuming every song probably does belong to hypergryph
                audio["label"] = u"Shanghai Hypergryph Network Technology Co., Ltd." #assuming every song probably does belong to hypergryph
                audio["organization"] = u"Shanghai Hypergryph Network Technology Co., Ltd." #assuming every song probably does belong to hypergryph
                
                audio["contact"] = "Shanghai Hypergryph Network Technology Co., Ltd., Room 504-1, 799 Yinxiang Road, Jiading District, Shanghai, China"
                audio["releaseStatus"] = "Official" #songs come from hypergryph itself
                audio["media"] = "Digital Media" #songs are digitally released
                audio["license"] = "All Rights Reserved" #to Hypergryph that is

                #i saw these under properties
                audio["contentUrl"] = u"https://monster-siren.hypergryph.com" #songs extracted from this website
                audio["authorUrl"] = u"https://monster-siren.hypergryph.com" #idk if this should be the same as contentUrl
                audio["promotionUrl"] = u"https://monster-siren.hypergryph.com" #technically used in game but promoted through their own music website

                if (watermark == True): #watermark the file if set to true
                    audio["comment"] = u"Audio file extracted from https://monster-siren.hypergryph.com's public API using https://github.com/rackman404/msr-parser-CLI, all rights reserved to Hypergryph itself"

                #get the year based on date already embedded in file (some files mmight not have the date, but just in case we shall wrap it in a try except block)
                '''
                try:
                    #print(audio["date"])
                    date = audio["date"][0] #based on battle plan obliteration file, date=2026-06-06
                    audio["year"] = date.split("-")[0] #year of release (song files should already have date released pre tagged but not year itself)
                except Exception as e:
                    console_gui_utils.console_print_err("METADATA ERR: Failed to add date tag (exception msg: " + str(e) + ") - moving on to next metadata tag")
                '''
    
                """implement later
                audio["track"] = 0 #order of this track relative to others
                audio["totalTracks"] = 0 #total number of tracks in album
                
                audio["releaseType"] = "" #if song is album or single/EP NOTE: check the album name, if it contains EP or no mention of OST, its a Single, ELSE, it is a Album
                audio["lyricist"] = "" #lyric writer
                audio["genre"] = ["Soundtrack", ""] #song genre (ex. rock, pop, etc..), first element should be soundtrack (it is a video game after all), next element should be determined through other means
                audio["language"] = "" #languages used in song

                audio["BPM"] = 0

                audio["year"] = 0 #year of release (song files should already have date released pre tagged but not year itself)
                audio["COMMENT"] = ""

                audio["syncedLyrics"] = "" #NOTE: apparently ID3V2 DOES support synced lyrics, would have been nice to know for a separate project lmao 
                audio["unsyncedLyrics"] ""
                """


                """ iterate through all artists (and album artists (maybe do a union operation on both to check for similar artists)) 
                aArtists = "" #album artists
                for rawAArtists in metadata["albumArtists"]:
                    if (aArtists == ""):
                        aArtists += rawAArtists 
                    else:
                        aArtists +=  "\\" + "\\" + rawAArtists 
                audio["albumArtist"] = aArtists
                """

                """ didn't even realize we could just add the array itself lmao
                sArtists = "" #song artists
                for rawSArtists in metadata["songMetaData"]['artists']:
                    if (sArtists == ""):
                        sArtists += rawSArtists 
                    else:
                        sArtists +=  "\\" + "\\" + rawSArtists 
                """

                #NOTE i have no clue if hypergryph actually has different fields for both album and song artists but to make sure, we we will do a union operation on both lists.
                all_artists_union_set =  set(metadata["songMetaData"]['artists']) | set(metadata['albumArtists'])
                all_artists = list (all_artists_union_set) #idk if the MSR artist (important for consistancy) is always the very first option if we do this, maybe manually rearrange it to the very first element as required

                audio["artist"] = all_artists
                #audio["artist"] = metadata["songMetaData"]["name"] non union operation
                
                #maybe also define the dimensions of image and what not
                image = Picture()
                image.type = 3 
                image.desc = "Front Cover"
                image.mime = "image/png" 

                image.data = open(cover_img_path, 'rb').read()
                audio.add_picture(image)

                audio.save(file_path) #save the metadata back to the file

                """ignore this random stuff
                audio.delete(file_path)
                audio.save(file_path)

                audio = ID3() #i am assuming we won't have any id3 headers, so have to append one to the file

                title = metadata["songMetaData"]["name"]
                audio.add(TIT2(encoding=3, text=title)) #song title 
                audio.add(TALB(encoding=3, text=metadata["albumName"])) #song album name

                imagedata = open(cover_img_path, 'rb').read()
                audio.add(APIC(3, 'image/png', 3, 'Front cover', imagedata)) #song album name

                audio.save(file_path)

                audio = FLAC(file_path)
                #audio.save(file_path)
                """
            case FileFormat.MP3.value:
                audio = ID3(file_path)
    except Exception as e:
        print (console_gui_utils.bcolors.FAIL + "THERE WAS A ERROR CONVERTING METADATA: " + str(e) + console_gui_utils.bcolors.ENDC)
        return
    
    console_gui_utils.console_print_success("Successfully song inputted metadata (title, cover image, etc..) into song file") 

    #print (file_path)

    #audio = FLAC(file_path)
    #print (audio.pprint())

    #print (audio)   
    #print (file_format)
