

from enum import Enum
import sys
import time

import requests
import json
import os


import msr_parser_code.ffmpeg_exec_controls as ffmpeg_exec_controls
import msr_parser_code.audio_metadata_tagging as audio_metadata_tagging
import msr_parser_code.console_gui_utils as console_gui_utils
import msr_parser_code.os_checks as os_checks
from msr_parser_code.arg_parse import parse_args

from tqdm import tqdm

from msr_parser_code.utility import FileFormat, DownloadMethod, SongSearchMetadata, MSRSongDataAPIFull, MSRSongDataAPIPartial, MSRAlbumDataAPIFull, MSRMasterListAlbums, MSRMasterListSongs, ProgramArguments, ConversionArguments, SearchArguments

#NOTE IMPORTANT, when using PyInstaller, shi may not work cause the launched executable will run in a temp folder somewhere different that the actual directory of the built exe.
#https://stackoverflow.com/questions/404744/determining-application-path-in-a-python-exe-generated-by-pyinstaller
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    cwd = os.path.dirname(sys.executable)
    print('running in a PyInstaller bundle')
else:
    cwd = os.path.dirname(__file__)
    print('running in a normal Python process')


#type MSR_file_dat = tuple[float, float]

#api paths
MSR_SONG_PATH = r"https://monster-siren.hypergryph.com/api/song/"

MSR_ALL_SONGS_PATH  = r"https://monster-siren.hypergryph.com/api/songs"
MSR_ALL_ALBUMS_PATH  = r"https://monster-siren.hypergryph.com/api/albums"

#data paths

CID_SONG_CACHE_FILE_PATH = os.path.abspath(os.path.join(cwd, "./cache/cid_song_cache.json")) #needed mainly for testing purposes, rather not constantly ping their servers for specific song cIds when testing this program
CID_ALBUM_CACHE_FILE_PATH = os.path.abspath(os.path.join(cwd, "./cache/cid_album_cache.json")) #needed mainly for testing purposes, rather not constantly ping their servers for specific song cIds when testing this program

GLOBAL_REQUESTS_HEADER = {'user-agent': 'MSR-Python-CLI-Downloader/V0.1 (email:jacky.zhang404@gmail.com gitrepo: https://github.com/rackman404/msr-parser-CLI)'}
GLOBAL_TIMEOUT = 5
GLOBAL_RECONNECT_TIMER = 2.5

"""
DATA_DOWNLOAD_FOLDER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "./output/"))
CACHE_DOWNLOAD_SONG_FOLDER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "./cache/songs")) 
"""

FOLDER_PATHS = {
    "DATA_DOWNLOAD_FOLDER_PATH": os.path.abspath(os.path.join(cwd, "./output//")), #NOTE THIS SHOULD ACTUALLY CHANGE IN WORKING_FOLDER_PATHS IF USER PASSES A CUSTOM ONE IN
    "CACHE_DOWNLOAD_SONG_FOLDER_PATH": os.path.abspath(os.path.join(cwd, "./cache//")),
    "CACHE_SONG_DOWNLOAD_SONG_FOLDER_PATH": os.path.abspath(os.path.join(cwd, "./cache/songs//")),
    
    "DEPENDENCIES_FOLDER_PATH": os.path.abspath(os.path.join(cwd, "./deps//")),
     
}

POSSIBLE_DEPENDENCIES_PATHS = {
    "FFMPEG": {
        "relative_path": os.path.abspath(os.path.join(cwd, "./deps/ffmpeg.exe")),
        "env_var": "ffmpeg",
    }
}

#NOTE To be set in os_checks.py during program initialiaztion, ik that these are constants AND that we can just set this with ternarys but fuck it we ball
WORKING_DEPENDENCIES_PATHS = None
WORKING_FOLDER_PATHS = None 

# --------------

#Content Retrieval and Parsing Methods
def save_json_msr(data_type: str, file_output_path: str):
    '''
        requests content at msr API, will check if request times out or if there was a general connection error (i.e user doesn't have internet) and will recursively continue connecting
        until successful or user quits

        Keyword arguments:
        data_type -- simply the url to request data file
        file_output_path -- where data file should be stored
    '''

    #print("(REMOVE ON BUILD) request was made")
    console_gui_utils.console_print_warn("Waiting one second before making API call")
    time.sleep(1)
    try:
        console_gui_utils.console_print_success("Downloading a metadata json from ("+data_type+") ")
        r = requests.get(data_type, headers=GLOBAL_REQUESTS_HEADER, timeout=GLOBAL_TIMEOUT)
    except requests.exceptions.Timeout as e:
        console_gui_utils.console_print_err("took too long (timed out for "+GLOBAL_TIMEOUT+" seconds) to request data at: " + str(e) + " Will make another attempt in "+str(GLOBAL_RECONNECT_TIMER)+" second (if not working, close program with CTRL+C):")
        time.sleep(GLOBAL_RECONNECT_TIMER)
        save_json_msr(data_type, file_output_path)
        return
    except requests.exceptions.ConnectionError as e:
        console_gui_utils.console_print_err("General connection error: " + str(e) + " Will make another attempt in "+str(GLOBAL_RECONNECT_TIMER)+" second (if not working, close program with CTRL+C):")
        time.sleep(GLOBAL_RECONNECT_TIMER)
        save_json_msr(data_type, file_output_path)
        return
    
    r.raise_for_status()
    data = json.loads(r.text)
    #print (data)
    with open(file_output_path, "w+") as file: #w+ in case file doesn't exist
        json.dump(data, file, indent=2)

def msr_get_all_cid(get_from_api: bool = False) -> tuple[MSRMasterListSongs, MSRMasterListAlbums]:
    '''
    Retrieves a list of all content ids (and associated info) of both songs and albums then stores them locally (to avoid having to constantly ping their servers for stuff)
    params:
    get_from_api: bool - force retrieve from public api even if a local cache of data exists
    '''

    console_gui_utils.console_sub_header("1.1. Song and Album Master List JSON Retrieval")
    if (os.path.isfile(CID_SONG_CACHE_FILE_PATH) == False or (get_from_api == True)):
        #console_gui_utils.console_header("Song contentID and master list Download")
        if (get_from_api == True):
            print ("force retrieving songs cache from MSR api:")
        else:
            print ("local content cache does not exist, requesting SONG data from msr API:")
        save_json_msr(MSR_ALL_SONGS_PATH, CID_SONG_CACHE_FILE_PATH)
        print ("success \n ------------------------------------")
    if (os.path.isfile(CID_ALBUM_CACHE_FILE_PATH) == False or (get_from_api == True)):
        #console_gui_utils.console_header("Album contentID and master list Download")
        if (get_from_api == True):
            print ("force retrieving songs cache from MSR api:")
        else:
            print ("local content cache does not exist, requesting ALBUM data from msr API:")
        save_json_msr(MSR_ALL_ALBUMS_PATH, CID_ALBUM_CACHE_FILE_PATH)
        print ("success \n ------------------------------------")

    console_gui_utils.console_print_success("local master JSON lists exists, retrieving jsons now")
    with open(CID_SONG_CACHE_FILE_PATH, "r") as file:
        data_songs = json.load(file)
        file.close()
    with open(CID_ALBUM_CACHE_FILE_PATH, "r") as file:
        data_albums = json.load(file)
        file.close()
    #print (data_songs)
    return data_songs, data_albums


def download_file(url: str, fileName: str):
    '''

    refs:
    #https://stackoverflow.com/questions/16694907/download-a-large-file-in-python-with-requests
    # https://stackoverflow.com/questions/62508831/how-can-i-get-size-of-file-while-downloading-it-in-python 
    '''
    true_file_path = os.path.join(WORKING_FOLDER_PATHS["DATA_DOWNLOAD_FOLDER_PATH"], fileName)

    if (os.path.isfile(true_file_path) == True):
        console_gui_utils.console_print_warn("WARNING: There is a file with the same exact file name (" + fileName + ") already in the download destination, skipping download")
        return true_file_path

    console_gui_utils.console_print_warn("Waiting one second before making API call" )
    time.sleep(1)
    with requests.get(url, headers=GLOBAL_REQUESTS_HEADER, stream=True) as r:
        #print("(REMOVE ON BUILD) request was made")
        #gui stuff
        r.raise_for_status()
        downloaded_size = 0

        #print(int(r.headers.get('Content-Length', 0)))
        #print(console_gui_utils.bcolors.OKGREEN + "Downloading " + console_gui_utils.bcolors.ENDC)
        total_size = int(r.headers.get('Content-Length', 0))
        with open(true_file_path, 'wb') as f, tqdm(unit='B', total=total_size, desc=fileName, unit_scale=True, unit_divisor=1024) as bar:
            for chunk in r.iter_content(chunk_size=1024*1024):
                size = f.write(chunk)
                bar.update(size)
                downloaded_size += size
            """ without gui stuff
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
            """
            
            pass
    #print(fileName + " downloaded")
    return true_file_path 

def msr_get_song_single_cid(cid: str) -> MSRSongDataAPIFull:
    '''
    because the URLs to the lrc and wav files are hidden in the individual song api JSONs and not in the master JSON list, we must request this for each song we find in user downloads
    '''
    data = None
    if (os.path.isfile(os.path.join(WORKING_FOLDER_PATHS["CACHE_DOWNLOAD_SONG_FOLDER_PATH"], cid + ".json")) == False):
        print ("downloading individual song JSON of cId: " + cid)
        save_json_msr(MSR_SONG_PATH + cid, os.path.join(WORKING_FOLDER_PATHS["CACHE_DOWNLOAD_SONG_FOLDER_PATH"], cid + ".json"))
        #print (json.loads(r.text))
    else:
        print("local cache of song JSON exists of cId: " + cid)
        pass
    with open(os.path.join(WORKING_FOLDER_PATHS["CACHE_DOWNLOAD_SONG_FOLDER_PATH"], cid + ".json"), "r") as file:
        json_raw = json.load(file)
        #print (data['data'])
        data = json_raw['data']
        file.close()

    return data #ignore the code and msg that the api prints out

#TODO implement args, do not pass random variables in
def main(
        args: ProgramArguments,
        #download_method: DownloadMethod, 
        #name: str, 
        #exact: bool, 
        #file_format: FileFormat, 
        #lyrics: bool, 
        #watermark: bool = True
    ):
    '''
    should be the main part of the program (but after the part where user args are parsed (i.e download method, name, etc...))
    NOTE name should either search for Content ID or name depending on if it is composed of only int values or has non int values 
    (would be easier for example if user can simply input the cID shown on the website URL if the name has smth like chinese characters for example)
    NOTE i realize that the url will not show album cID but only song cID, unsure what to do. Perhaps add a optional parameter to enable a "download all songs that share the same album cID as the user inputted album cID given the song cID"
    NOTE ADD OPTIONAL -ignore_instrumental flag, would search through and ignore the songs with (instrumental) in the name

    NOTE deal with cID as a input option later, fully implement search by name first

    
    2 parts:
    1. search routine where we find applicable songs to download
    2. download routine, batch download everything then post process them

    params:
    download_method - the type of search and download we are performing
    name - depending on download method, could simply mean the name of album or name of single song
    exact - wheather or not should download any song that contains the name as a substring or if song/album name MUST match user defined name (NOTE: this should only apply to songs not albums)
    format - file format
    lyrics - if we should also download the .lrc file if there is one 
    
    IMPLEMENT LATER
    downloadPath - if user can specify an
    useFoldersForAlbum - if files should simply download in the output directory or if they can be downloaded
    plainLyrics - if the lrc file should be compressed into a plain lyrics paragraph and embedded into the file's metadata (which some formats like ID3 should support)
    '''

    console_gui_utils.console_header("1. Song/Album Search")
    songs_found = search_songs(search_method=args.search_args.mode, exact=args.search_args.exact, name=args.search_args.search_term)
    
    #present user with download options and ask them if they wish to proceed (if there were any songs found at all)
    if (len(songs_found) != 0):
        #show the names of songs to download and allow the user to make a Y/N choice wheather to continue
        console_gui_utils.console_print_success(str(len(songs_found)) + " songs were found matching search criteria, they are:")
        console_gui_utils.console_print_blue("--------------------")
        
        print(f"{"Song Name":<100} {"Album Name"}")
        for song in songs_found:
                print(f"{song['song_data']['name']:<100} {song['albumName']}")
        console_gui_utils.console_print_blue("--------------------")
        if (args.user_confirmation == True):  
            user_confirmation = input("do you wish to continue to downloads? Y/N ")
            if (user_confirmation == "Y"):
                console_gui_utils.console_print_success("will now download at (PATH: " + WORKING_FOLDER_PATHS["DATA_DOWNLOAD_FOLDER_PATH"] + ")")
            else:
                print("Exiting...")
                sys.exit()
                return       
    else:
        console_gui_utils.console_print_err("No Songs were found terminating")
        print("Exiting...")
        sys.exit()
        return    


    console_gui_utils.console_header("2. Full Song Metadata JSON Download and Local Caching")
    #extraction of full metadata details (i.e coverURL, contentURL, etc...) for each song
    #songs = [] #songs and all appropriate download links and metadata
    for song in songs_found:
        song['songMetaData'] = msr_get_song_single_cid(song['song_data']['cid']) #make a request to their API
        

    console_gui_utils.console_header("3. Song/Album File Downloads and Postprocessing(convert/tagging)")
    #2 download routine, batch download everything
    for song in songs_found:  
        console_gui_utils.console_sub_header("-")
        console_gui_utils.console_sub_header("Current Song: " + song['songMetaData']['name'])
        console_gui_utils.console_sub_header("-")

        console_gui_utils.console_print_blue(">>>>>>>>>>>>>>>>> Downloading all required Assets (i.e .lrc file (if applicable), .png file, .wav file)")
        file_path = download_file(song["songMetaData"]["sourceUrl"], song["songMetaData"]['name'] + ".wav")
        file_path = download_file(song["coverImgUrl"], song["songMetaData"]['name'] + ".png")
        if (args.download_args.lyrics == False or song["songMetaData"]["lyricUrl"] == None):
            console_gui_utils.console_print_warn("either no lyrics exists for this song or user has disabled lyric download. Skipping lyric download for song")
        else:
            lrc_path = download_file(song["songMetaData"]["lyricUrl"], song["songMetaData"]['name'] + ".lrc")
        #2.1 for each file we should convert file and add metadata in first before moving onto the next song to download
        if (args.convert_args.convert_format == FileFormat.WAV):
            console_gui_utils.console_print_warn("no file conversions or metadata has been added (.wav was specified by user and .wav does not support metadata)")
        else:
            console_gui_utils.console_print_blue(">>>>>>>>>>>>>>>>> Now converting .wav to ." + args.convert_args.convert_format.value + " ")
            ffmpeg_exec_controls.convert_file(os.path.join(WORKING_FOLDER_PATHS["DATA_DOWNLOAD_FOLDER_PATH"], song["songMetaData"]['name'] + ".wav"), os.path.join(WORKING_FOLDER_PATHS["DATA_DOWNLOAD_FOLDER_PATH"], song["songMetaData"]['name'] + "." + args.convert_args.convert_format.value), ffmpeg_path=WORKING_DEPENDENCIES_PATHS["FFMPEG"])
            
            #2.1 now adding metadata
            console_gui_utils.console_print_blue(">>>>>>>>>>>>>>>>> Now Adding Metadata to converted file")
            audio_metadata_tagging.add_metadata(os.path.join(WORKING_FOLDER_PATHS["DATA_DOWNLOAD_FOLDER_PATH"], song["songMetaData"]['name'] + "." + args.convert_args.convert_format.value), args.convert_args.convert_format, song, os.path.join(WORKING_FOLDER_PATHS["DATA_DOWNLOAD_FOLDER_PATH"], song["songMetaData"]['name'] + ".png"), args.metadata_args.watermark)
        print("") #print new line to make it easier to read output

#TODO move all MSR requests methods and this search method into a separate file
def search_songs(   
        search_method: DownloadMethod, 
        exact: bool, 
        name: str, 
        #include_instrumental: bool = True, 
        #diff_folder_path: str = None
        ) -> list[SongSearchMetadata]:
    data_songs, data_albums = msr_get_all_cid()
    songs_found = []

    if (name.isdigit() == True):
        console_gui_utils.console_print_warn("Detected a Content ID: searching by cId")
    else:
       console_gui_utils.console_print_warn("Detected a Name: searching by Song/Album Name") 

    #TODO implement All search and Diff search
    #TODO IMPLEMENT NON EXACT ALBUM SEARCH BY NAME (i.e "miss" returns, dont miss it,  missy, miss you)
    match search_method:
        case DownloadMethod.SINGLE:
            search_key_word = 'name'
            
            if (name.isdigit() == True):
                skip_name_search = True
                search_key_word = 'cid'

            for song in data_songs['data']['list']:
                song_dat: SongSearchMetadata = {
                    "song_data": None, #NOTE incomplete song data from master list HERE
                    "songMetaData": None, #NOTE To be Added in later step
                    "albumName": "",
                    "albumArtists": "",
                    "coverImgUrl": ""
                }
                #raw = {}
                if (name in song[search_key_word] and exact == False): #Will return multiple as we are checking if a substring of this exists
                    song_dat["song_data"] = song
                elif (song[search_key_word] == name and exact == True): #Will return only one as we are now checking for exact match   
                    song_dat["song_data"] = song

                for album in data_albums['data']:
                    if (album['cid'] == song['albumCid']):
                        song_dat["albumName"] = album['name']
                        song_dat["albumArtists"] = album["artistes"]
                        song_dat["coverImgUrl"] = album['coverUrl']
                        break
                #songs_found.append(raw)  
                if (song_dat["song_data"] != None):    
                    songs_found.append(song_dat)

        case DownloadMethod.ALBUM:

            album_cid = "" #intermediate data

            temp_alb = ""
            temp_art = ""
            temp_cover = ""

            
            if (name.isdigit() == True): #NOTE, while it is possible for user to have entered album ID, you can't actually see it in the website, most likely they will pass a song id OF the album
                console_gui_utils.console_print_warn("NOTE: As Album Search is enabled, program will search by album using provided song cID")
                for song in data_songs['data']['list']: #get the album id given song id
                    if (name in song['cid']):
                        console_gui_utils.console_print_development("found matching cid")
                        album_cid = song['albumCid']

                        for album in data_albums['data']:
                            if (album['cid'] == album_cid):
                                temp_alb = album['name']
                                temp_art = album["artistes"]
                                temp_cover = album['coverUrl']

                                break #no need to search for more at this point
                        break #ditto

            else: #search by name for cID
                for album in data_albums['data']:
                    if (album['name'] == name):
                        album_cid = album['cid']

                        temp_alb = album['name']
                        temp_art = album["artistes"]
                        temp_cover = album['coverUrl']
                        break

            if (album_cid == ""):
                return [] #return a empty list since a vaid album was not matched above
            
            print ("found matching album cID: " + album_cid)
            for song in data_songs['data']['list']:
                song_dat = {
                    "song_data": None, #NOTE incomplete song data from master list HERE
                    "albumName": temp_alb,
                    "albumArtists": temp_art,
                    "coverImgUrl": temp_cover
                }
                if (song['albumCid'] == album_cid):
                    song_dat["song_data"] = song
                    songs_found.append(song_dat)
        case _:
            print("ERROR: proper download method not specified")

    #TODO Implement include_instrumental (strip all songs with (instrumental) in their songs)
    sorted_songs_found = songs_found
    if (len(songs_found) != 0):
        sorted_songs_found = sorted(songs_found, key=lambda d: d['albumName']) #sort by album name so they (download/get presented by user) by album (idr where i got this code snippet ngl)

    return sorted_songs_found



def init():
    #initialization
    console_gui_utils.console_header("Program Initialization")
    #create_folders() #TODO delete when method below is done
    folders = os_checks.create_folders(hard_coded_paths=FOLDER_PATHS, user_data_output_folder=None)
    if (folders == None):
        console_gui_utils.console_print_err("Somehow an error occurred creating folders, exiting...")
        sys.exit()  
    #print (deps_path)
    deps_path = os_checks.check_deps(POSSIBLE_DEPENDENCIES_PATHS) 
    if (deps_path == None):
      console_gui_utils.console_print_err("DEPENDENCIES (i.e FFmpeg.exe) not detected in ENV or in deps folder, exiting...")
      sys.exit()  
    else:
        return folders, deps_path

#TODO do this bruh (put this into arg_parse.py as well maybe)
def parse_params(args: ProgramArguments):
    '''
    parse the arguments to show to user
    '''
    param_string = ""
    param_string += "Raw: " + str(args) + "\n"
    param_string += "Formatted: \n"

    return param_string 

if __name__ == "__main__":
    WORKING_FOLDER_PATHS, WORKING_DEPENDENCIES_PATHS = init()
    args = sys.argv[1:]
    parsed_args = parse_args(sys.argv[1:])

    console_gui_utils.console_header("Program Start") 

    param_string = parse_params(parsed_args)
    console_gui_utils.console_start_screen(param_string) #TODO, pass the parsed args in here to show to console 
    #TODO add another user confirmation just to see if args are correct

    main(parsed_args)


    pass