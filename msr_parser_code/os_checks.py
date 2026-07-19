import os
import msr_parser_code.console_gui_utils as console_gui_utils


def check_deps(dep_paths: dict) -> dict | None:
    '''
    check any binary dependencies. Should first detect any dependencies in predefined dep_key folder then should detect if in ENV as a fall back

    RETURN: A dict containing working file paths, else return NONE

    NOTE there should only be one dependencies for now (FFmpeg), however if additional .exes are required for something like metadata tagging, should be included here 
    '''

    working_dep_paths = {     
    }

    try:
        console_gui_utils.console_sub_header("Checking for Dependencies")
        for dep_key in dep_paths:
            check_rel = os.path.isfile(dep_paths[dep_key]["relative_path"])
            check_env = os.environ.get(dep_paths[dep_key]["env_var"])

            print ("Checking for " + dep_key +"("+dep_paths[dep_key]["relative_path"] + ").... ", end="")
            if (check_rel == False and check_env == None): #first check if in the hard coded path
                console_gui_utils.console_print_err("DOES NOT EXIST AT DEP FOLDER OR ENV")
                return None
            elif (check_rel == True):
                console_gui_utils.console_print_success("exists at relative path, at: " + dep_paths[dep_key]["relative_path"])
                working_dep_paths.update({dep_key: dep_paths[dep_key]["relative_path"]})
            elif (check_env != None):
                console_gui_utils.console_print_success("exists at ENV variable path, at: " + str(check_env))
                working_dep_paths.update({dep_key: check_env})

        console_gui_utils.console_print_success("all dependencies exist")
        return working_dep_paths
    except Exception as e:
        console_gui_utils.console_print_err("ERROR CHECKING DEPENDENCIES: " + str(e))
        return None

    
def create_folders(hard_coded_paths: dict, user_data_output_folder: str = None) -> dict | None:
    '''
    stub, implement later

    PARAMS:
    - hard_coded_paths: the actual hard coded paths
    - user_paths: create any user designated output folder (OPTIONAL)

    RETURN: Dict if no problems creating new folders or if folders already exist, None if a error was encountered

    Refs:
    -- https://stackoverflow.com/questions/70235696/checking-folder-and-if-it-doesnt-exist-create-it
    -- https://stackoverflow.com/questions/73207617/remove-file-name-and-extension-from-path-and-just-keep-path
    '''

    console_gui_utils.console_sub_header("Checking Folders")
    if (user_data_output_folder != None):
        console_gui_utils.console_print_warn("detected user provided output directory, will use it instead of default")
    
    try:
        for folder_key in hard_coded_paths:
            if not os.path.exists(hard_coded_paths[folder_key]): #create any unk directories
                print(console_gui_utils.bcolors.OKGREEN + "created " + hard_coded_paths[folder_key] + " folder" + console_gui_utils.bcolors.ENDC)
                os.makedirs(hard_coded_paths[folder_key])
                pass
            else:
                print(console_gui_utils.bcolors.OKGREEN + "folder exists at: " + hard_coded_paths[folder_key] + " folder" + console_gui_utils.bcolors.ENDC)
        
        if (user_data_output_folder != None):
            console_gui_utils.console_print_warn("detected user provided output directory that doesn't exist, creating now:")
            if not os.path.exists(user_data_output_folder):
                print(console_gui_utils.bcolors.OKGREEN + "created " + user_data_output_folder + " folder" + console_gui_utils.bcolors.ENDC)
                os.makedirs(os.path.dirname(user_data_output_folder))

        '''
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
        new_dict = hard_coded_paths

    except Exception as e:
        console_gui_utils.console_print_err("ERROR CREATING/CHECKING FOLDERS: " + str(e))
        return None

    if (user_data_output_folder != None):
        new_dict["DATA_DOWNLOAD_FOLDER_PATH"] = user_data_output_folder
    
    return new_dict

