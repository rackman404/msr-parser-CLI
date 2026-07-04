import os
import msr_parser_main 
import console_gui_utils


def check_deps() -> dict | None:
    '''
    check any binary dependencies. Should first detect any dependencies in predefined dep_key folder then should detect if in ENV as a fall back

    RETURN: A dict containing working file paths, else return NONE

    NOTE there should only be one dependencies for now (FFmpeg), however if additional .exes are required for something like metadata tagging, should be included here 
    '''

    working_dep_paths = {     
    }

    try:
        console_gui_utils.console_sub_header("Checking for Dependencies")
        for dep_key in msr_parser_main.POSSIBLE_DEPENDENCIES_PATHS:
            check_rel = os.path.isfile(msr_parser_main.POSSIBLE_DEPENDENCIES_PATHS[dep_key]["relative_path"])
            check_env = msr_parser_main.POSSIBLE_DEPENDENCIES_PATHS[dep_key]["env_path"]

            print ("Checking for " + dep_key +"("+msr_parser_main.POSSIBLE_DEPENDENCIES_PATHS[dep_key]["relative_path"] + ").... ", end="")
            if (check_rel == False and check_env == None): #first check if in the hard coded path
                console_gui_utils.console_print_err("DOES NOT EXIST AT DEP FOLDER OR ENV")
                return None
            elif (check_rel == True):
                console_gui_utils.console_print_success("exists at relative path, at: " + msr_parser_main.POSSIBLE_DEPENDENCIES_PATHS[dep_key]["relative_path"])
                working_dep_paths.update({dep_key: msr_parser_main.POSSIBLE_DEPENDENCIES_PATHS[dep_key]["relative_path"]})
            elif (check_env != None):
                console_gui_utils.console_print_success("exists at ENV variable path, at: " + str(check_env))
                working_dep_paths.update({dep_key: check_env})

        console_gui_utils.console_print_success("all dependencies exist")
        return working_dep_paths
    except Exception as e:
        console_gui_utils.console_print_err("ERROR CHECKING DEPENDENCIES: " + str(e))
        return None

    
def create_folders() -> bool:
    '''
    stub, implement later

    RETURN: True if no problems creating new folders or if folders already exist, False if a error was encountered
    '''

    try:



        return True
    except Exception as e:
        console_gui_utils.console_print_err("ERROR CREATING/CHECKING FOLDERS: " + str(e))
        return False


