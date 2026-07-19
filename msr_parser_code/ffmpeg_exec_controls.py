import os
import subprocess
import time

import msr_parser_code.console_gui_utils as console_gui_utils
from tqdm import tqdm

import random


# Function generating random number between 1 and 100
def generate_random_numbers():
	while True:
            yield random.randint(1, 100)
             
def convert_file(file_path_original: str, file_path_new: str, ffmpeg_path: str):
    '''
    we will assume that both file paths have the correct/supported file extensions

    TODO 
    https://stackoverflow.com/questions/53222231/redirect-stderr-and-stdout-from-ffmpeg-to-a-file-in-python-with-subprocess redirect and show stderr if fails to convert to specified format
    https://www.reddit.com/r/ffmpeg/comments/rzxxhf/how_to_catch_ffmpeg_read_error_in_python/

    refs:
    https://stackoverflow.com/questions/43274476/is-there-a-way-to-check-if-a-subprocess-is-still-running
    https://stackoverflow.com/questions/10251391/suppressing-output-in-python-subprocess-call
    '''

    #print ("FFMPEG PATH: " + ffmpeg_path)

    process_string = f'ffmpeg.exe -y  -i ' "\"" + file_path_original + "\"" + " " + "\"" + file_path_new + "\"" 
    #print ("converting file in FFmpeg:" + file_path_original + " " + file_path_new )
    #print(process_string)
    process = subprocess.Popen(process_string, cwd=os.path.dirname(ffmpeg_path), shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.STDOUT) # shell = true, security issue?

    tot_time = 0 
    custom_format = "{desc} | Time Elapsed: {n_fmt} Seconds" #https://tqdm.github.io/docs/tqdm/ 
    #NOTE time isn't accurate but whatever, fix later
    with tqdm(total=tot_time, desc="Converting File with FFmpeg.exe: | STATUS: Converting",  bar_format=custom_format) as bar:
        while (True):
            time.sleep(0.15)
            bar.update(round(tot_time, 4))
            tot_time += 0.15
            poll = process.poll()
            if poll is None:
                pass
            else:  
                bar.set_description("Converting File with FFmpeg.exe: | STATUS: " + console_gui_utils.bcolors.OKGREEN + ".wav FILE CONVERSION COMPLETE!" + console_gui_utils.bcolors.ENDC)
                break

    #console_gui_utils.console_print_success(" .wav Conversion complete!")

    '''
    while (True): #check to see if the conversion is still running
        time.sleep(0.5)
        poll = process.poll()
        if poll is None:
            print ("Converting...")
        else:
            console_gui_utils.console_print_success(".wav Conversion complete at: " + file_path_new)
            break
    '''