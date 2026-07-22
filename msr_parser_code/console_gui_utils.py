"""
This module provides a set of terminal based utility methods:
- Colored text using ANSI escape sequences
- Console width/height formatting for headers

NOTE Any method using ANSI for coloring may not work if the terminal does not support it
NOTE There should not be any unit testing done on these methods, literally no point 
"""

from enum import Enum
import shutil

# https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
class BColors(Enum):
    """Data class containing standard terminal supporting colors using ANSI escape sequences"""
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
    Denotes a minor process, will calculate the size of terminal at time of method invocation
    Returns a header with encapsulated msg text full terminal width with '#' padding
    '''
    terminal_width = shutil.get_terminal_size((80, 20)).columns
    print(BColors.HEADER.value + f"{"":#<{terminal_width}}" + BColors.ENDC.value)
    print((BColors.HEADER.value + header_msg + BColors.ENDC.value).center(shutil.get_terminal_size().columns))
    print(BColors.HEADER.value + f"{"":#<{terminal_width}}" + BColors.ENDC.value)

# https://stackoverflow.com/questions/44781484/python-string-formatter-align-center
def console_sub_header(header_msg: str):
    """
    Denotes a minor major process, will calculate the size of terminal at time of method invocation
    Returns a header with encapsulated msg text half terminal width with '#' padding
    """
    terminal_width = shutil.get_terminal_size((80, 20)).columns*0.50
    print((BColors.OKGREEN.value + header_msg + BColors.ENDC.value).center(int(terminal_width),"-"))

def console_start_screen(args: str):
    '''
    To be displayed as the algorithm steps the program takes.
    Composed of several sub headers with help information 

    Keyword arguments:
    args -- a preformatted string of arguments to be displayed to user
    '''

    console_sub_header("Information") #general information
    print ("")
    print ("This CLI Tool will download songs from Hypergryphs CDN Servers"
            " using their public API hosted at https://monster-siren.hypergryph.com")
    print ("The CLI will use the following steps to perform said procedure:")
    print ("0. Initialization:")
    print ("    0.1 - Ensure data folders are created/exists:")
    print ("    0.2 - Ensure either FFmpeg.exe is installed in the Deps folder"
           " or can be accessed from a ENV variable:")
    print ("1 Song/Album Search:")
    print ("    1.1 Song and Album Master List JSON Retrieval: "
           "Retrieves the 2 JSON files stored on their API containing"
            "full list of albums and songs")
    print ("    1.2 Song Search: "
           "Perform the actual search of matching songs, then ask for user validation")
    print ("2 Full Song Metadata JSON Download and Local Caching: \n "
              "Retrieve the full song JSONs that contain"
                 "the actual links to audio file and lyrics, etc..  ")
    print ("3 Song/Album File Downloads and Postprocessing(convert/tagging):")
    print ("    For Each Song:")
    print ("        Download files (.wav, .lrc, .png)")
    print ("        Convert .wav to user specified audio format (if any)")
    print ("        add metadata to new audio file (if converted in previous step)")
    print ("")

    console_sub_header("Help")
    print ("Please use the -help flag or visit the repo hosted at "
           "https://github.com/rackman404/msr-parser-CLI for more information")

    #show which flags and parameters have been set by user input
    console_sub_header("Program Flags and Parameters Set by User")
    print (args)
    print ("")

    #show which flags and parameters have been set by user input


def console_print_err(msg: str, new_line: bool = True):
    """Prints a error message wrapped with red text"""
    print(BColors.FAIL.value + msg + BColors.ENDC.value , end= '\n' if new_line else "")

def console_print_success(msg: str, new_line: bool = True):
    """Prints a success message wrapped with green text"""
    print(BColors.OKGREEN.value + msg + BColors.ENDC.value , end= '\n' if new_line else "")

def console_print_warn(msg: str, new_line: bool = True):
    """Prints a warning message wrapped with yellow text"""
    print(BColors.WARNING.value + msg + BColors.ENDC.value, end= '\n' if new_line else "")

def console_print_blue(msg: str, new_line: bool = True):
    """Prints generic message in blue"""
    print(BColors.OKBLUE.value + msg + BColors.ENDC.value, end= '\n' if new_line else "")


def console_print_development(msg: str, debug_on: bool = True):
    '''
        Bolded text for debug messsages.
        
        TODO maybe reference the TEST global variable on main file and \
            check if this should even print anything

        TODO OR just check if application is a binary built by pyinstaller tbh
    '''
    print(BColors.BOLD.value + "DEBUG: " + msg + BColors.ENDC.value, end= '\n' if debug_on else "")
