from enum import Enum
import sys
import time
import argparse

import requests
import json
import os

import ffmpeg_exec_controls
import audio_metadata_tagging
import console_gui_utils
import os_checks

from tqdm import tqdm

from utility import FileFormat, DownloadMethod

#type MSR_file_dat = tuple[float, float]

#api paths
MSR_SONG_PATH = r"https://monster-siren.hypergryph.com/api/song/"

MSR_ALL_SONGS_PATH  = r"https://monster-siren.hypergryph.com/api/songs"
MSR_ALL_ALBUMS_PATH  = r"https://monster-siren.hypergryph.com/api/albums"

#data paths

CID_SONG_CACHE_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "./cache/cid_song_cache.json")) #needed mainly for testing purposes, rather not constantly ping their servers for specific song cIds when testing this program
CID_ALBUM_CACHE_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "./cache/cid_album_cache.json")) #needed mainly for testing purposes, rather not constantly ping their servers for specific song cIds when testing this program

GLOBAL_REQUESTS_HEADER = {'user-agent': 'MSR-Python-CLI-Downloader/V0.1 (email:jacky.zhang404@gmail.com gitrepo:)'}
GLOBAL_TIMEOUT = 5
GLOBAL_RECONNECT_TIMER = 2.5

"""
DATA_DOWNLOAD_FOLDER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "./output/"))
CACHE_DOWNLOAD_SONG_FOLDER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "./cache/songs")) 
"""

FOLDER_PATHS = {
    "DATA_DOWNLOAD_FOLDER_PATH": os.path.abspath(os.path.join(os.path.dirname(__file__), "./output/")), #NOTE THIS SHOULD ACTUALLY CHANGE IN WORKING_FOLDER_PATHS IF USER PASSES A CUSTOM ONE IN
    "CACHE_SONG_DOWNLOAD_SONG_FOLDER_PATH": os.path.abspath(os.path.join(os.path.dirname(__file__), "./cache/songs")), 
    "CACHE_DOWNLOAD_SONG_FOLDER_PATH": os.path.abspath(os.path.join(os.path.dirname(__file__), "./cache/")) 
}

POSSIBLE_DEPENDENCIES_PATHS = {
    "FFMPEG": {
        "relative_path": os.path.abspath(os.path.join(os.path.dirname(__file__), "./deps/ffmpeg.exe")),
        "env_var": "ffmpeg",
    }
}

#NOTE To be set in os_checks.py during program initialiaztion, ik that these are constants AND that we can just set this with ternarys but fuck it we ball
WORKING_DEPENDENCIES_PATHS = None
WORKING_FOLDER_PATHS = None 

''' obsolete
def create_folders():
    console_gui_utils.console_sub_header("Checking Folders")
    
    #kinda stupid to hardcode each folder like this but theres really only 3 folders to do this to so whatever
    if not os.path.exists(os.path.dirname(CID_SONG_CACHE_FILE_PATH)): #recursively create any unknown directories
        print(console_gui_utils.bcolors.OKGREEN + "created JSON cache folder" + console_gui_utils.bcolors.ENDC)
        os.makedirs(os.path.dirname(CID_SONG_CACHE_FILE_PATH))
    else:
        print(console_gui_utils.bcolors.OKGREEN + "cache exists already" + console_gui_utils.bcolors.ENDC)
    if not os.path.exists((DATA_DOWNLOAD_FOLDER_PATH)): #recursively create any unknown directories
        print(console_gui_utils.bcolors.OKGREEN + "created song output folder" + console_gui_utils.bcolors.ENDC)
        os.makedirs((DATA_DOWNLOAD_FOLDER_PATH))
    else:
        print(console_gui_utils.bcolors.OKGREEN + "song output exists already" + console_gui_utils.bcolors.ENDC)
    if not os.path.exists((CACHE_DOWNLOAD_SONG_FOLDER_PATH)): #recursively create any unknown directories
        print(console_gui_utils.bcolors.OKGREEN + "created specific song output folder" + console_gui_utils.bcolors.ENDC)
        os.makedirs((CACHE_DOWNLOAD_SONG_FOLDER_PATH))
    else:
        print(console_gui_utils.bcolors.OKGREEN + "specific song JSON cache exists already" + console_gui_utils.bcolors.ENDC)
'''


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
    print(console_gui_utils.bcolors.WARNING + "Waiting one second before making API call" + console_gui_utils.bcolors.ENDC)
    time.sleep(1)
    try:
        print(console_gui_utils.bcolors.OKGREEN + "Downloading a metadata json from ("+data_type+") " + console_gui_utils.bcolors.ENDC)
        r = requests.get(data_type, headers=GLOBAL_REQUESTS_HEADER, timeout=GLOBAL_TIMEOUT)
    except requests.exceptions.Timeout as e:
        print (console_gui_utils.bcolors.FAIL + "took too long (timed out for "+GLOBAL_TIMEOUT+" seconds) to request data at: " + str(e) + " Will make another attempt in "+str(GLOBAL_RECONNECT_TIMER)+" second (if not working, close program with CTRL+C):" + console_gui_utils.bcolors.ENDC)
        time.sleep(GLOBAL_RECONNECT_TIMER)
        save_json_msr(data_type, file_output_path)
        return
    except requests.exceptions.ConnectionError as e:
        print (console_gui_utils.bcolors.FAIL + "General connection error: " + str(e) + " Will make another attempt in "+str(GLOBAL_RECONNECT_TIMER)+" second (if not working, close program with CTRL+C):" + console_gui_utils.bcolors.ENDC)
        time.sleep(GLOBAL_RECONNECT_TIMER)
        save_json_msr(data_type, file_output_path)
        return
    
    r.raise_for_status()
    data = json.loads(r.text)
    #print (data)
    with open(file_output_path, "w+") as file: #w+ in case file doesn't exist
        json.dump(data, file, indent=2)

def msr_get_all_cid(get_from_api: bool = False):
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

    print (console_gui_utils.bcolors.OKGREEN + "local master JSON lists exists, retrieving jsons now" + console_gui_utils.bcolors.ENDC)
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
        print(console_gui_utils.bcolors.WARNING + "WARNING: There is a file with the same exact file name (" + fileName + ") already in the download destination, skipping download" + console_gui_utils.bcolors.ENDC)
        return true_file_path

    print(console_gui_utils.bcolors.WARNING + "Waiting one second before making API call" + console_gui_utils.bcolors.ENDC)
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

def msr_get_song_single_cid(cid: str) -> dict:
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



def user_download(
        download_method: DownloadMethod, 
        name: str, 
        exact: bool, 
        file_format: FileFormat, 
        lyrics: bool, 
        watermark: bool = True
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
    data_songs, data_albums = msr_get_all_cid()
    
    songs_found = [] #should be formatted as {"partial_song_data": data from master list of songs, "album name": name of album (not including in the master list of songs)}
    #TODO Reinclude the album name (by referencing album master list) in the songs_found list so that it can be printed out for display to user
    #TODO Put this in a separate method
    match download_method:
        case DownloadMethod.SINGLE:
            for song in data_songs['data']['list']:
                #raw = {}
                if (name in song['name'] and exact == False): #Will return multiple as we are checking if a substring of this exists
                    songs_found.append(song)
                elif (song['name'] == name and exact == True): #Will return only one as we are now checking for exact match   
                    songs_found.append(song)
                #songs_found.append(raw)       

        case DownloadMethod.ALBUM:
            album_cid = "" #intermediate data
            for album in data_albums['data']:
                if (album['name'] == name):
                    album_cid = album['cid']
                    break
            for song in data_songs['data']['list']:
                if (song['albumCid'] == album_cid):
                    songs_found.append(song)
            #print(songs) 
        case _:
            print("ERROR: proper download method not specified")

    
    #present user with download options and ask them if they wish to proceed (if there were any songs found at all)
    if (len(songs_found) != 0):
        #show the names of songs to download and allow the user to make a Y/N choice wheather to continue
        print(console_gui_utils.bcolors.OKGREEN + str(len(songs_found)) + " songs were found matching search criteria, they are:" + console_gui_utils.bcolors.ENDC)
        print(console_gui_utils.bcolors.OKBLUE + "--------------------" + console_gui_utils.bcolors.ENDC)
        for song in songs_found:
                print(console_gui_utils.bcolors.OKBLUE + "|song: " + song['name'] + console_gui_utils.bcolors.ENDC)
        print(console_gui_utils.bcolors.OKBLUE + "--------------------" + console_gui_utils.bcolors.ENDC)
        user_confirmation = input("do you wish to continue to downloads? Y/N ")
        if (user_confirmation == "Y"):
            print(console_gui_utils.bcolors.OKGREEN + "will now download at (PATH: " + WORKING_FOLDER_PATHS["DATA_DOWNLOAD_FOLDER_PATH"] + ")" + console_gui_utils.bcolors.ENDC)
        else:
            print("Exiting...")
            return       
    else:
        print(console_gui_utils.bcolors.FAIL + "No Songs were found terminating" + console_gui_utils.bcolors.ENDC)


    console_gui_utils.console_header("2. Full Song Metadata JSON Download and Local Caching")
    #extraction of full metadata details (i.e coverURL, contentURL, etc...) for each song
    songs = [] #songs and all appropriate download links and metadata
    for song in songs_found:
        full_song_data = msr_get_song_single_cid(song['cid']) #make a request to their API
        for album in data_albums['data']:
            if (album['cid'] == song['albumCid']):
                songs.append({
                    "songMetaData": full_song_data,
                    "coverImgUrl": album['coverUrl'],
                    "albumName": album['name'],
                    "albumArtists": album["artistes"] #usually just MSR but may be more            
                })
                break

    console_gui_utils.console_header("3. Song/Album File Downloads and Postprocessing(convert/tagging)")
    #2 download routine, batch download everything
    for song in songs:  
        console_gui_utils.console_sub_header("-")
        console_gui_utils.console_sub_header("Current Song: " + song['songMetaData']['name'])
        console_gui_utils.console_sub_header("-")

        print(console_gui_utils.bcolors.OKBLUE + ">>>>>>>>>>>>>>>>> Downloading all required Assets (i.e .lrc file (if applicable), .png file, .wav file)" + console_gui_utils.bcolors.ENDC)
        file_path = download_file(song["songMetaData"]["sourceUrl"], song["songMetaData"]['name'] + ".wav")
        file_path = download_file(song["coverImgUrl"], song["songMetaData"]['name'] + ".png")
        if (lyrics == False or song["songMetaData"]["lyricUrl"] == None):
            print (console_gui_utils.bcolors.WARNING + "either no lyrics exists for this song or user has disabled lyric download. Skipping lyric download for song" + console_gui_utils.bcolors.ENDC)
        else:
            lrc_path = download_file(song["songMetaData"]["lyricUrl"], song["songMetaData"]['name'] + ".lrc")
        #2.1 for each file we should convert file and add metadata in first before moving onto the next song to download
        if (file_format == FileFormat.WAV):
            print (console_gui_utils.bcolors.WARNING + "no file conversions or metadata has been added (.wav was specified by user and .wav does not support metadata)" + console_gui_utils.bcolors.ENDC)
        else:
            print (console_gui_utils.bcolors.OKBLUE + ">>>>>>>>>>>>>>>>> Now converting .wav to ." + file_format.value + " " + console_gui_utils.bcolors.ENDC)
            ffmpeg_exec_controls.convert_file(os.path.join(WORKING_FOLDER_PATHS["DATA_DOWNLOAD_FOLDER_PATH"], song["songMetaData"]['name'] + ".wav"), os.path.join(WORKING_FOLDER_PATHS["DATA_DOWNLOAD_FOLDER_PATH"], song["songMetaData"]['name'] + "." + file_format.value), ffmpeg_path=WORKING_DEPENDENCIES_PATHS["FFMPEG"])
            
            #2.1 now adding metadata
            print (console_gui_utils.bcolors.OKBLUE + ">>>>>>>>>>>>>>>>> Now Adding Metadata to converted file" + console_gui_utils.bcolors.ENDC)
            audio_metadata_tagging.add_metadata(os.path.join(WORKING_FOLDER_PATHS["DATA_DOWNLOAD_FOLDER_PATH"], song["songMetaData"]['name'] + "." + file_format.value), file_format, song, os.path.join(WORKING_FOLDER_PATHS["DATA_DOWNLOAD_FOLDER_PATH"], song["songMetaData"]['name'] + ".png"), watermark)
        print("") #print new line to make it easier to read output





def user_input_parsed(input: list[str]):
    '''
    Where program Args should be processed, should return a error and failed exit code if formatted incorrectly. Should a list of args selected afterwards before proceeding to main code
    '''

    print ("user inputted: " + input + " as args.")


    #user_download(download_method=DownloadMethod.ALBUM, name="涤墨作战OST", exact=False, file_format=FileFormat.FLAC, lyrics=True)

    pass

# manual testing method
def test():
    #write_to_file("test", CID_CACHE_FILE_PATH)
    #data_songs, data_albums = msr_get_all_cid()

    #some examples just to check if format of the json is as expected (as well as possible input parsing options we can try out from the user)
    '''
    #example of retrieving from the fifth song stored in the overall cache (but not necessarilly the song with cid = 5)
    print (data_songs['data']['list'][5]) #{'cid': '779450', 'name': '夏日远去之后', 'albumCid': '5198', 'artists': ['塞壬唱片-MSR']}
    '''

    '''
    #example of retrieving a song based on name
    song_name = "Battleplan Obliteration" #user input
    for song in data_songs['data']['list']:
        if (song_name in song['name']): #Will return multiple as we are checking if a substring of this exists
            print(song) #{'cid': '697687', 'name': 'Battleplan Obliteration', 'albumCid': '1015', 'artists': ['塞壬唱片-MSR']} {'cid': '697687', 'name': 'Battleplan Obliteration', 'albumCid': '1015', 'artists': ['塞壬唱片-MSR']}
        if (song['name'] == song_name): #Will return only one as we are now checking for exact match
            print(song) #{'cid': '697687', 'name': 'Battleplan Obliteration', 'albumCid': '1015', 'artists': ['塞壬唱片-MSR']}
    '''
    
    #example of retrieving all songs of a given album given the name
    """
    album_name = "Innocence" #user input
    album_cid = "" #intermediate data
    songs = []#user output
    for album in data_albums['data']:Y
        if (album['name'] == album_name):
            album_cid = album['cid']
            break
    for song in data_songs['data']['list']:
        if (song['albumCid'] == album_cid):
            songs.append(song)
    print (album_cid)   #7762
    print (songs) #[{'cid': '953947', 'name': 'Innocence (Instrumental)', 'albumCid': '7762', 'artists': ['塞壬唱片-MSR']}, {'cid': '232224', 'name': 'Innocence', 'albumCid': '7762', 'artists': ['塞壬唱片-MSR']}]
    """

    #user_download(download_method=DownloadMethod.SINGLE, name="Battleplan Obliteration", exact=True, file_format=FileFormat.FLAC, lyrics=True)
    #user_download(download_method=DownloadMethod.SINGLE, name="Heavenly Me", exact=True, file_format=FileFormat.FLAC, lyrics=True) #song has multiple song artists
    user_download(download_method=DownloadMethod.ALBUM, name="涤墨作战OST", exact=False, file_format=FileFormat.FLAC, lyrics=True)

    #user_download(download_method=DownloadMethod.SINGLE, name="Battleplan", exact=True, file_format=FileFormat.FLAC, lyrics=True) #should show nothing
    #user_download(download_method=DownloadMethod.SINGLE, name="Battleplan", exact=False, file_format=FileFormat.FLAC, lyrics=True) #should show all battleplan OST songs
    #user_download(download_method=DownloadMethod.ALBUM, name="人们，我们OST", exact=True, file_format=FileFormat.FLAC, lyrics=True) #NOTE should deal with the fact that there may be non standard characters that hypergryph uses (，)
    

if __name__ == "__main__":

    #premain
    #args = sys.argv[1:]
    #parse_user_input(args)
    #parsed_args = user_input_parsed()

    console_gui_utils.console_header("Program Start")
    console_gui_utils.console_start_screen()

    #initialization
    console_gui_utils.console_header("Program Initialization")
    #create_folders() #TODO delete when method below is done
    WORKING_FOLDER_PATHS = os_checks.create_folders(hard_coded_paths=FOLDER_PATHS, user_data_output_folder=None)
    if (WORKING_FOLDER_PATHS == None):
        console_gui_utils.console_print_err("Somehow an error occurred creating folders, exiting...")
        sys.exit()  

    #print (deps_path)
    deps_path = os_checks.check_deps(POSSIBLE_DEPENDENCIES_PATHS) 
    if (deps_path == None):
      console_gui_utils.console_print_err("DEPENDENCIES (i.e FFmpeg.exe) not detected in ENV or in deps folder, exiting...")
      sys.exit()  
    else:
        WORKING_DEPENDENCIES_PATHS = deps_path

    #REAL MAIN
    #user_download() #passed in arg from parsed_args (assuming they are valid)
    #fake main for just testing the main part of program
    test()

    pass