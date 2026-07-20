"""
Converts files to specified format

TODO Provide options to apply filters
"""
import os
import subprocess
import time
from tqdm import tqdm


from msr_parser_code import console_gui_utils


# Function generating random number between 1 and 100 (UNUSED)
#def generate_random_numbers():
#	while True:
#            yield random.randint(1, 100)

def convert_file(file_path_original: str, file_path_new: str, ffmpeg_path: str):
    '''
    we will assume that both file paths have the correct/supported file extensions

    TODO redirect and show stderr if fails to convert to specified format
    https://www.reddit.com/r/ffmpeg/comments/rzxxhf/how_to_catch_ffmpeg_read_error_in_python/
    https://stackoverflow.com/questions/53222231/redirect-stderr-and-stdout-from-ffmpeg-to-a-file-in-python-with-subprocess 

    refs:
    https://stackoverflow.com/questions/43274476/is-there-a-way-to-check-if-a-subprocess-is-still-running
    https://stackoverflow.com/questions/10251391/suppressing-output-in-python-subprocess-call
    '''

    #process_string = f'ffmpeg.exe -y \
    #    -i ' "\"" + file_path_original + "\"" + "\
    #    " + "\"" + file_path_new + "\""

    #Fixed F string Interpolation
    process_string = f"ffmpeg.exe -y \
        -i \"{file_path_original}\" \
        \"{file_path_new}\""

    # shell = true, security issue?
    with subprocess.Popen(
        process_string,
        cwd=os.path.dirname(ffmpeg_path),
        shell = True,
        stdout = subprocess.DEVNULL,
        stderr = subprocess.STDOUT) as process:

        #https://tqdm.github.io/docs/tqdm/
        tot_time = 0
        custom_format = "{desc} | Time Elapsed: {n_fmt} Seconds"
        #NOTE time isn't accurate but whatever, fix later
        with tqdm(total=tot_time,
                desc="Converting File with FFmpeg.exe: | STATUS: Converting",
                bar_format=custom_format) as graphical_bar:
            while True:
                time.sleep(0.15)
                graphical_bar.update(round(tot_time, 4))
                tot_time += 0.15
                poll = process.poll()
                if poll is None:
                    pass
                else:
                    graphical_bar.set_description("Converting File with FFmpeg.exe: | STATUS: " \
                    + console_gui_utils.BColors.OKGREEN.value + ".wav FILE CONVERSION COMPLETE!"\
                    + console_gui_utils.BColors.ENDC.value)
                    break
