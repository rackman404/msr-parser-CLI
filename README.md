# msr-parser-CLI

<a id="readme-top"></a>

<div align="center">
  <h1 align="center">MSR Parser Python CLI (any maybe) GUI</h3>
   <h3 align="center">Version: Pre-V1.0 or smth</h3>

  <p align="center">
    Python based CLI tool (Later with simple GUI as well maybe) for downloading and auto tagging song content from  <a href="(https://monster-siren.hypergryph.com)">Hypergryph's Official Music Website</a>.
    <br />
    <a href="https://github.com/TBA/TBA/tree/main/_Documentation"><strong>See User Manual (None right Now)»</strong></a>
    <br />
  </p>
</div>


<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#overview">Overview</a> </li>
    <li><a href="#telemetry">Telemetry</a> </li>
	<li><a href="#built-with">Built With</a></li>
    <li><a href="#getting-started-development">Getting Started (Development)</a></li>
    <li><a href="#documentation">Documentation</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#attributions-and-acknowledgements">Attributions and Acknowledgments</a></li>
  </ol>
</details>


# Overview
![preview](_Documentation/Images/preview_07_18_2.png)
![preview](_Documentation/Images/preview_07_18.png)
<sub>Preview </sub>

<img width="800" height="450" alt="Image" src="https://github.com/user-attachments/assets/bef0aeb1-20ce-4fce-8a90-61367e1d7ef5" />
<sub>Preview With sample Album Download</sub>


Python CLI for downloading songs from Arknights Soundtrack. Extremely overkill but I kind of wanted to write unit tests in Python and make an actual CLI tool for fun. 


# Requirements

### If running straight from the .py file
- Install required python deps from the requirements.txt
- Add FFmpeg.exe to deps folder
- Run the CLI in terminal with Python msr_parser_main.py {args}
TODO: add picture of this
### If running from .exe (compiled from PyInstaller)
- Add FFmpeg.exe to deps folder
- Run the exe in terminal with msr_parser_main.exe {args}
TODO: add picture of this


# Usage

Run the thing from command line from a terminal. Supply with [Arguments](https://cs.stanford.edu/people/nick/py/python-main.html) (google if you don't know how idk). Il add a GUI that wraps around the CLI if i get bored or smth.

### Possible Flags and Arguments 

NOTE: 
- -s {search term} or --search {search term} MUST be provided.
- Some arguments have no effect depending on other arguments (i.e --skiptags won't do anything for .wav files since those files don't support metadata tagging to being with)

Below are the supported/planned flags and arguments (all are optional except the search term one) that can be set before program is run. They have been split into multiple categories depending on which part of the pipeline they affect


### Common Args

| Argument                 | Options | Behaviour                                                                                            | Default Behaviour if not used                           | Implemented                  |
| ------------------------ | ------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------- | ---------------------------- |
| -y --skipuser            |         | Will skip user confirmation after presenting found songs to user (and any other user input).         | require user confirmations                              | <ul><li>- [x]</li><br> </ul> |
| --output {"folder_path"} |         | Changes output directory of downloaded files. NOTE, if -m diff is used, this must always be provided | built in output folder used by application ("./output") |                              |

### Search Args
| Argument     | Options           | Behaviour                                                                                   | Default Behaviour if not used                                                   | Implemented                                                        |
| ------------ | ----------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| -s --search  |                   | The Search Term                                                                             | no default, MUST BE PROVIDED (Literally the only Mandatory Argument in program) | <ul><li>- [x]</li><br> </ul>                                       |
| --noexact    |                   | If flag is enabled, will search using the provided search term as a **substring**           | will search and match songs ONLY if exact match                                 | <ul><li>- [x]</li><br> </ul>                                       |
| -m {options} | single/ album/all | Searches AND downloads either using Album name/cID or Song name/cID, or downloads all songs | Search and Downloads by single song                                             | <br> <ul><li>- [x] single </li><br> <li>- [x] album</li><br> </ul> |
| -d --diff    |                   | From found songs, only download those that don't exist in output directory.                 |                                                                                 |                                                                    |

### Download Args
| Argument   | Options | Behaviour                                                               | Default Behaviour if not used                  | Implemented                  |
| ---------- | ------- | ----------------------------------------------------------------------- | ---------------------------------------------- | ---------------------------- |
| --nolyrics |         | Will skip downloading any .lrc files if a song has it                   | Downloads .lrc files                           | <ul><li>- [x]</li><br> </ul> |
| -a         |         | Will download songs into separate album folders in the output directory | Downloads all songs ungrouped output directory |                              |

### Conversion Args

| Argument              | Options         | Behaviour                                                                                                                                   | Default Behaviour if not used | Implemented                  |
| --------------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- | ---------------------------- |
| --filter {options}    | normalize/strip | all done using FFmpeg filters:<br>- normalize: normalize audio<br>- strip: remove beginning and end portions of silence if song has any<br> | No Filters applied            |                              |
| -f --format {options} | mp3/flac/ogg    | Will convert downloaded music files to the following format                                                                                 | no conversions                | <ul><li>- [x]</li><br> </ul> |

### Metadata Args

| Argument             | Options Avaliable | Behaviour                                                                                                                  | Default Behaviour if not used                                | Implemented                  |
| -------------------- | ----------------- | -------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ | ---------------------------- |
| --metadata {options} | none,basic,full   | none: does not add metadata<br>basic: adds metadata provided from the Hypergryph API only<br>full: IDK about this one ngl  | adds metadata tags to converted song files with "basic" mode |                              |
| --musicbrainz        |                   | Will use the MusicBrainz API to add any missing metadata to songs                                                          | no musicbrainz metadata used                                 |                              |
| -v                   | --waveform        | create a .png showing waveform of song                                                                                     | No visualization                                             |                              |
| -a                   | --ass             | using audio source separation, create multiple audio files containing distinct audio elements (i.e guitars, vocals, etc..) | None                                                         |                              |
| -w --watermark       |                   | Watermark in song metadata comments field with this github link                                                            | Defaults to no watermark                                     | <ul><li>- [x]</li><br> </ul> |


### Examples:

# Built With

- Note: any built in python libraries not shown here
- We note that Github Workflow scripts will be/are used to build the binaries and perform automated testing 
### Python Stack (External Libraries)
* [![Tech Stack Badge](https://img.shields.io/badge/Pyinstaller-blue?style=for-the-badge&logo=python&logoColor=61DAFB)](https://pyinstaller.org/en/stable/) - Python Standalone Binary Builder
*  [![Tech Stack Badge](https://img.shields.io/badge/mutagen-red?style=for-the-badge&logo=python&logoColor=61DAFB)](https://mutagen.readthedocs.io/en/latest/user/gettingstarted.html) - Audio File Metadata Library
*  [![Tech Stack Badge](https://img.shields.io/badge/Requests-red?style=for-the-badge&logo=python&logoColor=61DAFB)](https://requests.readthedocs.io/en/latest/) - HTTP Library
-  [![Tech Stack Badge](https://img.shields.io/badge/tqdm-red?style=for-the-badge&logo=python&logoColor=61DAFB)](https://tqdm.github.io/) - Console Progress Bar Library

### Languages
* [![Tech Stack Badge](https://img.shields.io/badge/Python-green?style=for-the-badge&logo=python&logoColor=61DAFB)](https://www.python.org/) - Self Explanatory

### External Binaries
-  [![Tech Stack Badge](https://img.shields.io/badge/ffmpeg-red?style=for-the-badge&logo=ffmpeg&logoColor=61DAFB)](https://www.ffmpeg.org/) - Video/Audio Processing Library/Executable 

- Note: I've tried to use as little external libraries and tools as possible. The ones that are included are because implementing their functionality would take an too long or are vastly out of scope for this project.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

# Getting Started (Development)

### Overview
Project uses a pipelined workflow as seen below:
![program_flow_diagram](_Documentation/Images/program_flow_diagram.png)
*General Program Execution Flow.*

Arguments are passed in from user via CLI arguments, these are parsed using the built in ArgParse python library and then mapped to multiple data classes contained in a master data class. 5 steps are then taken:

1. *Validation of any folder directories*
	- Also checks if FFmpeg is installed in /deps/ or can be accessed in ENV
2. *Search songs using provided search arguments*
3. If user accepts the search (or auto user confirmation is enabled)
	1. *Download found songs*
	2. If Allowed to convert songs
		1. *Convert songs via FFmpeg*
		2. If allowed to add metadata
			1. *Add metadata*


### Project Structure
Current project folder organization. I am aware i should probably put the actual program script files in its own separate folder as well as separating any  
![program_flow_diagram](_Documentation/Images/project_file_structure.png)
*Descriptions and current project structure*

### Data Flow
I don't know why i made these ngl (I don't even know if these are correct, forgot most of COE691)
![program_flow_diagram](_Documentation/Images/L0_context_diagram.png)
*Level 0 Context Diagram*

![program_flow_diagram](_Documentation/Images/L1_dfd.png)
*Level 1 Data Flow Diagram*

### Testing
I have some unit tests done but Im lazy asf.

### Contributions
Just fork the git repo and pip install requirements.txt or smth idk. Not much else to work on for this thing anyways as it should fit most of my personal requirements. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>


# Documentation

This project uses [Obsidian](https://obsidian.md) for Markdown file editing. Most documentation for this project is included with the "\_Documentation" folder. Documentation is either in Markdown for text or Draw.io files for diagrams (can be downloaded and imported into Draw.io to read or directly opened in VSCode using extensions). Note that documentation may not always be up to date. All documentation can be found in the \_Documentation folder in this repo.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

# License



<p align="right">(<a href="#readme-top">back to top</a>)</p>

# Disclaimer and Acknowledgements

### Acknowledgements
- Thanks to Hypergryph for actually providing said API as well the means to download high quality audio files direct from source instead of being forced to stream the music from Spotify or other means

### Disclaimer
Songs retrieved from this software is obviously owned by Hypergryph Co. Ltd., as a content retrieval API is publicly exposed and other GitHub hosted downloading scripts exists i am assuming that retrieving and downloading these songs are allowed as longs as its not done commercially.

