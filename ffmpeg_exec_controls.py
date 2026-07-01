import os
import subprocess
import time

import console_gui_utils

FFMPEG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "./deps/"))


def convert_file(file_path_original: str, file_path_new: str):
    '''
    we will assume that both file paths have the correct/supported file extensions

    refs:
    https://stackoverflow.com/questions/43274476/is-there-a-way-to-check-if-a-subprocess-is-still-running
    https://stackoverflow.com/questions/10251391/suppressing-output-in-python-subprocess-call
    '''

    process_string = f'ffmpeg.exe -y  -i ' "\"" + file_path_original + "\"" + " " + "\"" + file_path_new + "\"" 
    #print ("converting file in FFmpeg:" + file_path_original + " " + file_path_new )
    #print(process_string)
    process = subprocess.Popen(process_string, cwd=FFMPEG_PATH, shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.STDOUT) # shell = true, security issue?

    while (True): #check to see if the conversion is still running
        time.sleep(0.5)
        poll = process.poll()
        if poll is None:
            print ("Converting...")
        else:
            console_gui_utils.console_print_success(".wav Conversion complete at: " + file_path_new)
            break