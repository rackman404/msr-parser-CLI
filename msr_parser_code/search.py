from msr_parser_code import utility
from msr_parser_code import console_gui_utils
from msr_parser_code import content_retrieval

#TODO move all MSR requests methods and this search method into a separate file
def search_songs(   
        search_method: utility.DownloadMethod, 
        exact: bool, 
        name: str, 
        #include_instrumental: bool = True, 
        #diff_folder_path: str = None
        ) -> list[utility.SongSearchMetadata]:
    data_songs, data_albums = content_retrieval.msr_get_all_cid()
    songs_found = []

    if (name.isdigit() == True):
        console_gui_utils.console_print_warn("Detected a Content ID: searching by cId")
    else:
       console_gui_utils.console_print_warn("Detected a Name: searching by Song/Album Name") 

    #TODO implement All search and Diff search
    #TODO IMPLEMENT NON EXACT ALBUM SEARCH BY NAME (i.e "miss" returns, dont miss it,  missy, miss you)
    match search_method:
        case utility.DownloadMethod.SINGLE:
            search_key_word = 'name'
            
            if (name.isdigit() == True):
                skip_name_search = True
                search_key_word = 'cid'

            for song in data_songs['data']['list']:
                song_dat: utility.SongSearchMetadata = {
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

        case utility.DownloadMethod.ALBUM:

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