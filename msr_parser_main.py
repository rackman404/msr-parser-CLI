

from enum import Enum
import sys
import time

import requests
import json
import os


from msr_parser_code import content_retrieval
import msr_parser_code.ffmpeg_exec_controls as ffmpeg_exec_controls
import msr_parser_code.audio_metadata_tagging as audio_metadata_tagging
import msr_parser_code.console_gui_utils as console_gui_utils
import msr_parser_code.os_checks as os_checks
from msr_parser_code.arg_parse import parse_args

from tqdm import tqdm

from msr_parser_code.search import search_songs
from msr_parser_code.utility import FileFormat, DownloadMethod, SongSearchMetadata, MSRSongDataAPIFull, MSRSongDataAPIPartial, MSRAlbumDataAPIFull, MSRMasterListAlbums, MSRMasterListSongs, ProgramArguments, ConversionArguments, SearchArguments

#NOTE IMPORTANT, when using PyInstaller, shi may not work cause the launched executable will run in a temp folder somewhere different that the actual directory of the built exe.
#https://stackoverflow.com/questions/404744/determining-application-path-in-a-python-exe-generated-by-pyinstaller
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    cwd = os.path.dirname(sys.executable)
    print('running in a PyInstaller bundle')
else:
    cwd = os.path.dirname(__file__)
    print('running in a normal Python process')


#data paths

CID_SONG_CACHE_FILE_PATH = os.path.abspath(os.path.join(cwd, "./cache/cid_song_cache.json")) #needed mainly for testing purposes, rather not constantly ping their servers for specific song cIds when testing this program
CID_ALBUM_CACHE_FILE_PATH = os.path.abspath(os.path.join(cwd, "./cache/cid_album_cache.json")) #needed mainly for testing purposes, rather not constantly ping their servers for specific song cIds when testing this program



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

#TODO implement args, do not pass random variables in
def main(args: ProgramArguments):
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
            console_gui_utils.console_print_warn("do you wish to continue to downloads? Y/N " , new_line= False)
            user_confirmation = input()
            if (user_confirmation.lower() == "y"):
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
        song['songMetaData'] = content_retrieval.msr_get_song_single_cid(song['song_data']['cid']) #make a request to their API
        

    console_gui_utils.console_header("3. Song/Album File Downloads and Postprocessing(convert/tagging)")
    #2 download routine, batch download everything
    for song in songs_found:  
        console_gui_utils.console_sub_header("-")
        console_gui_utils.console_sub_header("Current Song: " + song['songMetaData']['name'])
        console_gui_utils.console_sub_header("-")

        console_gui_utils.console_print_blue(">>>>>>>>>>>>>>>>> Downloading all required Assets (i.e .lrc file (if applicable), .png file, .wav file)")
        file_path = content_retrieval.download_file(song["songMetaData"]["sourceUrl"], song["songMetaData"]['name'] + ".wav", WORKING_FOLDER_PATHS["DATA_DOWNLOAD_FOLDER_PATH"])
        file_path = content_retrieval.download_file(song["coverImgUrl"], song["songMetaData"]['name'] + ".png", WORKING_FOLDER_PATHS["DATA_DOWNLOAD_FOLDER_PATH"])
        if (args.download_args.lyrics == False or song["songMetaData"]["lyricUrl"] == None):
            console_gui_utils.console_print_warn("either no lyrics exists for this song or user has disabled lyric download. Skipping lyric download for song")
        else:
            lrc_path = content_retrieval.download_file(song["songMetaData"]["lyricUrl"], song["songMetaData"]['name'] + ".lrc", WORKING_FOLDER_PATHS["DATA_DOWNLOAD_FOLDER_PATH"])
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


def init() -> tuple[dict, dict]:
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
    if (parsed_args.user_confirmation == True):  
        console_gui_utils.console_print_warn("Are these arguments correct? Y/N " , new_line= False)
        user_confirmation = input()
        if user_confirmation.lower() != "y":
            print("Exiting...")
            sys.exit()

    main(parsed_args)


    pass