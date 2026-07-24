import json
import os
import time

import requests
from tqdm import tqdm

from msr_parser_code import utility
from msr_parser_code import console_gui_utils
from msr_parser_main import CID_ALBUM_CACHE_FILE_PATH, CID_SONG_CACHE_FILE_PATH, FOLDER_PATHS




GLOBAL_REQUESTS_HEADER = {'user-agent': 'MSR-Python-CLI-Downloader/V0.1 (email:jacky.zhang404@gmail.com gitrepo: https://github.com/rackman404/msr-parser-CLI)'}
GLOBAL_TIMEOUT = 5
GLOBAL_RECONNECT_TIMER = 2.5

#api paths
MSR_SONG_PATH = r"https://monster-siren.hypergryph.com/api/song/"
MSR_ALL_SONGS_PATH  = r"https://monster-siren.hypergryph.com/api/songs"
MSR_ALL_ALBUMS_PATH  = r"https://monster-siren.hypergryph.com/api/albums"


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

def msr_get_all_cid(get_from_api: bool = False) -> tuple[utility.MSRMasterListSongs, utility.MSRMasterListAlbums]:
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


def download_file(url: str, fileName: str, download_path: str):
    '''

    refs:
    #https://stackoverflow.com/questions/16694907/download-a-large-file-in-python-with-requests
    # https://stackoverflow.com/questions/62508831/how-can-i-get-size-of-file-while-downloading-it-in-python 
    '''
    true_file_path = os.path.join(download_path, fileName)

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

def msr_get_song_single_cid(cid: str) -> utility.MSRSongDataAPIFull:
    '''
    because the URLs to the lrc and wav files are hidden in the individual song api JSONs and not in the master JSON list, we must request this for each song we find in user downloads
    '''

    data = None
    if (os.path.isfile(os.path.join(FOLDER_PATHS["CACHE_DOWNLOAD_SONG_FOLDER_PATH"], cid + ".json")) == False):
        print ("downloading individual song JSON of cId: " + cid)
        save_json_msr(MSR_SONG_PATH + cid, os.path.join(FOLDER_PATHS["CACHE_DOWNLOAD_SONG_FOLDER_PATH"], cid + ".json"))
        #print (json.loads(r.text))
    else:
        print("local cache of song JSON exists of cId: " + cid)
        pass
    with open(os.path.join(FOLDER_PATHS["CACHE_DOWNLOAD_SONG_FOLDER_PATH"], cid + ".json"), "r") as file:
        json_raw = json.load(file)
        #print (data['data'])
        data = json_raw['data']
        file.close()

    return data #ignore the code and msg that the api prints out
