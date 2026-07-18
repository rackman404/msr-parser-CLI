import shutil

#NOTE there should not be any unit testing done on these methods, literally no point

# CLI Utility Methods and classes
class bcolors: #https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def console_header(header_msg: str):
    '''
    for use in denoting a new major process currently running
    '''
    terminal_width = shutil.get_terminal_size((80, 20)).columns
    print(bcolors.HEADER + f"{"":#<{terminal_width}}" + bcolors.ENDC)
    print((bcolors.HEADER + header_msg + bcolors.ENDC).center(shutil.get_terminal_size().columns))
    print(bcolors.HEADER + f"{"":#<{terminal_width}}" + bcolors.ENDC)


    #print(bcolors.HEADER + "###############################################################" + bcolors.ENDC)
    #print(bcolors.HEADER + header_msg + bcolors.ENDC)
    #print(bcolors.HEADER + "###############################################################" + bcolors.ENDC)

def console_sub_header(header_msg: str):
    '''
    for use in denoting a new minor process currently running
    '''

    terminal_width = shutil.get_terminal_size((80, 20)).columns*0.50
    #print(bcolors.OKGREEN + "----------------------" + header_msg + "----------------------"  + bcolors.ENDC)

    print((bcolors.OKGREEN + header_msg + bcolors.ENDC).center(int(terminal_width),"-")) # https://stackoverflow.com/questions/44781484/python-string-formatter-align-center

#TODO
def console_help_screen():
    '''
    to be displayed if user inputs -help as a program argument
    '''

def console_start_screen(args: any):
    '''
    to be displayed as the algorithm steps the program takes
    '''

    console_sub_header("Information") #general information
    print ("")
    print ("This CLI Tool will download songs from Hypergryphs CDN Servers using their public API hosted at https://monster-siren.hypergryph.com")
    print ("The CLI will use the following steps to perform said procedure:")
    print ("0. Initialization:")
    print ("    0.1 - Ensure data folders are created/exists:")
    print ("    0.2 - Ensure either FFmpeg.exe is installed in the Deps folder or can be accessed from a ENV variable:")
    print ("1 Song/Album Search:")
    print ("    1.1 Song and Album Master List JSON Retrieval: Retrieves the 2 JSON files stored on their API containing the full list of albums and songs")
    print ("    1.2 Song Search: Perform the actual search of matching songs, then ask for user validation")
    print ("2 Full Song Metadata JSON Download and Local Caching: \n    Retrieve the full song JSONs that contain the actual links to audio file and lyrics, etc..  ")
    print ("3 Song/Album File Downloads and Postprocessing(convert/tagging):")
    print ("    For Each Song:")
    print ("        Download files (.wav, .lrc, .png)")
    print ("        Convert .wav to user specified audio format (if any)")
    print ("        add metadata to new audio file (if converted in previous step)")

    print ("")

    console_sub_header("Program Flags and Parameters Set by User") #show which flags and parameters have been set by user input
    print ("")
    print (str(args))
    #.....
    print ("")

    console_sub_header("Help") #show which flags and parameters have been set by user input
    print ("Please use the -help flag or visit the repo hosted at https://github.com/rackman404/msr-parser-CLI for more information")

def console_print_err(msg: str, new_line: bool = True):
    print(bcolors.FAIL + msg + bcolors.ENDC , end= '\n' if new_line == True else "")

def console_print_success(msg: str, new_line: bool = True):
    print(bcolors.OKGREEN + msg + bcolors.ENDC , end= '\n' if new_line == True else "")

def console_print_warn(msg: str, new_line: bool = True):
    print(bcolors.WARNING + msg + bcolors.ENDC, end= '\n' if new_line == True else "")

def console_print_development(msg: str, new_line: bool = True):
    '''
        Bolded for debugging only
        NOTE maybe reference the TEST global variable on main file and check if this should even print anything
        NOTE OR just check if application is a binary built by pyinstaller tbh
    '''
    print(bcolors.BOLD + "DEBUG: " + msg + bcolors.ENDC, end= '\n' if new_line == True else "")