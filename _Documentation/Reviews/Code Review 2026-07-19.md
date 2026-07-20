
# Overview
- using Pylint. All code modules are linted and fixed as much as possible.
- TODO TMMRW, Refactor search and download related methods out of main.
	- Thinking about remaking some methods to make them more easily testable by unit tests
- Also Lint main itself

---
# Formatting
### Overall
- Removed some obsolete code blocks
- Formatting
	- Stuff such as Trailing Whitespaces and long lines are removed when possible
	- changed import msr_parser_code.{MOD_NAME} as {MOD_NAME} to from msr_parser_code import {MOD_NAME}
	- prefixed methods with "\_" in modules if they are not expected to be called outside of module 
	- Added return types and param types if i forgot them before
	- Removal of parentheses in if statements
- Console_GUI:
	- Refactored everything to only use the methods defined in this module and not directly add ANSI colors themselves (except for one use in ffmpeg_exec_controls)

### Console GUI Utils
- Original Pylint Score: 5/10
- New Pylint Score (After refactor): 10/10

Notes:
- Not much to refactor/format, literally just utility functions and print statements
- Mainly reformatted to be more readable

Unique Problems:
- Most print statements were way too long
	- Used \ and a new line to format strings better
	- LATER: possibly format strings out of doc into separate localization files?
- Added doc strings to every method and further formatting to long comments
- Added module doc string
- Changed casing of BColors and allowed it to inherit from Enum so that its a proper Enum (instead of just being a random ass class)

### Arg Parse
- Original Pylint Score: 0/10
- New Pylint Score (After refactor): 10/10

Unique Problems:
- Used a built in keyword "input" for the parsing methods. Replaced them with more descriptive and unique param names (raw_args, namespace_args)
- Specified the exact type of the mapping function parameter (argparse.Namespace)

### OS Checks
- Original Pylint Score: 2.29/10
- New Pylint Score (After refactor): 8.09/10

Unique Problems:
- W0631: Using possibly undefined loop variable 'folder_key' (undefined-loop-variable)
	- Fixed by ensuring that folder_key = None before starting loop

Known Issues:
- C0121: Singleton-comparison
	- Too used to using == and != for comparisons and equality checks
- W0718: Catching too general exception
	- Im not dealing with every case that folder creation could possibly fail


### FFmpeg Exec Controls
- Original Pylint Score: 0/10
- New Pylint Score (After refactor): 10/10

Unique Problems:
- Fixed Interpolated variables in process string
	- Added them using {var_name} instead of + var_name +
- Fixed "with" for launching a new subprocess
Before (R1732: Consider using 'with' for resource-allocating operations (consider-using-with)):
``` python
process = subprocess.Popen(
        process_string,
        cwd=os.path.dirname(ffmpeg_path),
        shell = True,
        stdout = subprocess.DEVNULL,
        stderr = subprocess.STDOUT)

    #https://tqdm.github.io/docs/tqdm/ 
    tot_time = 0
    custom_format = "{desc} | Time Elapsed: {n_fmt} Seconds"
    #NOTE time isn't accurate but whatever, fix later
    with tqdm(total=tot_time,
              desc="Converting File with FFmpeg.exe: | STATUS: Converting",
              bar_format=custom_format) as graphical_bar:
        while (True):
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
```

After (simply wrapped the code below into the new with statement above)
``` python
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
            while (True):
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
```

### Utility
- Original Pylint Score: 2.32/10
- New Pylint Score (After refactor): 10/10

No unique issues, just formatting issues

### Audio Metadata Tagging
- Original Pylint Score: 2.32/10
- New Pylint Score (After refactor): 7.14/10

Unique Problems:
- Removed all u'string' (u prefix). Used this cause the mutagen docs used it too but python uses Unicode by default anyways

Known Problems:
- TODO and Unused Args and some long comments


# Final
Full Code = 9.18/10
NOTE: have not refactored main, thats a tmmrw thing to do