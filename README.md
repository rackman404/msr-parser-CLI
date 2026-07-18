# msr-parser-CLI

<a id="readme-top"></a>

<div align="center">
  <h1 align="center">MSR Parser Python CLI and GUI</h3>
   <h3 align="center">Version: Pre-V1.0</h3>

  <p align="center">
    Python based CLI tool (Later with simple GUI as well maybe) for downloading and auto tagging song content from  <a href="(https://monster-siren.hypergryph.com)">Hypergryph's Official Music Website</a>.
    <br />
    <a href="https://github.com/TBA/TBA/tree/main/_Documentation"><strong>See User Manual »</strong></a>
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

![preview](_Documentation/Images/preview_v0_1_0.png)
<sub>Preview Pre V1.0 of CLI </sub>

TBD GIF
<sub>Preview Pre V1.0 of CLI </sub>

TBD SCREENSHOT
<sub>Preview Pre V1.0 of GUI </sub>


Python CLI for downloading songs from Arknights Soundtrack. Extremely overkill but I kind of wanted to write unit tests in Python and make an actual CLI tool for fun. 


# Requirements

### If running straight from the .py file
- Install required python deps from the requirements.txt
- Add FFmpeg.exe to deps folder

### If running from .exe (compiled from PyInstaller)
- Add FFmpeg.exe to deps folder

# Usage

Run the thing from command line from a terminal. Supply with Arguments (google if you don't know how idk)

### Possible Flags and Arguments 

Show a Simplified Diagram from left to right Search -> Download -> Conversion -> Metadata Tagging
<sub> Process Diagram </sub>

NOTE: 
- A string value MUST be provided as the very first argument, this is the search term. This is only optional if "-m all" or "-m diff" are used, since search term is not required for these terms. 
- Some arguments have no effect depending on other arguments (i.e --skiptags won't do anything for .wav files since those files don't support metadata tagging to being with)

Below are the supported/planned flags and arguments (both optional and mandatory) that can be set before program is run:


### Common Args


### Search Args


### Download Args


### Conversion Args


### Metadata Args

| Argument                 | Options Avaliable | Behaviour                                                                                                                                   | Default Behaviour if not used                                | Implemented                                                 |
| ------------------------ | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ | ----------------------------------------------------------- |
| -m {options}             | single/ album/all | Searches AND downloads either using Album name/cID or Song name/cID, or downloads all songs                                                 | Search and Downloads by single song                          | <br> <ul><li>- [x] </li><br> <li>- [x] album</li><br> </ul> |
| --noexact                |                   | If flag is enabled, will search using the provided search term as a **substring**                                                           | will search and match songs ONLY if exact match              |                                                             |
| -y --skipuser            |                   | Will skip user confirmation after presenting found songs to user (and any other user input).                                                | require user confirmations                                   |                                                             |
| --output {"folder_path"} |                   | Changes output directory of downloaded files. NOTE, if -m diff is used, this must always be provided                                        | built in output folder used by application ("./output")      |                                                             |
| --metadata {options}     | none,basic,full   | none: does not add metadata<br>basic: adds metadata provided from the Hypergryph API only<br>full: IDK about this one ngl                   | adds metadata tags to converted song files with "basic" mode |                                                             |
| -f --format {options}    | mp3/flac/ogg      | Will convert downloaded music files to the following format                                                                                 | no conversions                                               |                                                             |
| --musicbrainz            |                   | Will use the MusicBrainz API to add any missing metadata to songs                                                                           | no musicbrainz metadata used                                 |                                                             |
| --nolyrics               |                   | Will skip downloading any .lrc files if a song has it                                                                                       | Downloads .lrc files                                         |                                                             |
| -a                       |                   | Will download songs into separate album folders in the output directory                                                                     | Downloads all songs ungrouped output directory               |                                                             |
| --filter {options}       | normalize/strip   | all done using FFmpeg filters:<br>- normalize: normalize audio<br>- strip: remove beginning and end portions of silence if song has any<br> | No Filters applied                                           |                                                             |
| -v                       |                   | create a .png showing waveform of song                                                                                                      | No visualization                                             |                                                             |
| -a                       | --ass             | using audio source separation, create multiple audio files containing distinct audio elements (i.e guitars, vocals, etc..)                  | None                                                         |                                                             |
| -d --diff                |                   | From found songs, only download those that don't exist in output directory.                                                                 | Noded                                                        |                                                             |
| -s --search              |                   | The Search Term                                                                                                                             | no default, MUST BE PROVIDED                                 |                                                             |
| -w --watermark           |                   | Watermark in song metadata comments field with this github link                                                                             | Defaults to no watermark                                     |                                                             |


### Examples:

# Built With

- Note: any built in python libraries not shown here
- We note that Github Workflow scripts were also used to build the binaries and perform automated testing 
### Python Stack (External Libraries)
* [![Tech Stack Badge](https://img.shields.io/badge/Pyinstaller-blue?style=for-the-badge&logo=python&logoColor=61DAFB)](https://www.electronjs.org) - Python Standalone Binary Builder
*  [![Tech Stack Badge](https://img.shields.io/badge/mutagen-red?style=for-the-badge&logo=python&logoColor=61DAFB)](https://mui.com) - Audio File Metadata Library
*  [![Tech Stack Badge](https://img.shields.io/badge/Requests-red?style=for-the-badge&logo=python&logoColor=61DAFB)](https://mui.com) - HTTP Library
-  [![Tech Stack Badge](https://img.shields.io/badge/tqdm-red?style=for-the-badge&logo=python&logoColor=61DAFB)](https://mui.com) - Console Progress Bar Library
- TBD - Python GUI Library
### Languages
* [![Tech Stack Badge](https://img.shields.io/badge/Python-green?style=for-the-badge&logo=python&logoColor=61DAFB)]([https://rust-lang.org/](https://rust-lang.org/)) 

### External Binaries
-  [![Tech Stack Badge](https://img.shields.io/badge/ffmpeg-red?style=for-the-badge&logo=ffmpeg&logoColor=61DAFB)](https://mui.com) - Console Progress Bar Library

- Note: I've tried to use as little external libraries and tools as possible. The ones that are included are because implementing their functionality would take an insane amount of time or are vastly out of scope for this project, may use typer or click in the future to make the CLI look better however.  
<p align="right">(<a href="#readme-top">back to top</a>)</p>


# Getting Started (Development)

Just fork the git repo and pip install requirements.txt or smth idk. Not much else to work on for this thing anyways as it should fit most of my personal requirements. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

# Documentation
(TBD)

This project uses [Obsidian](https://obsidian.md) for Markdown file editing. Most documentation for this project is included with the "\_Documentation" folder. Documentation is either in Markdown for text or Draw.io files for diagrams (can be downloaded and imported into Draw.io to read or directly opened in VSCode using extensions). Note that documentation may not always be up to date. All documentation can be found in the \_Documentation folder in this repo.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

# License



<p align="right">(<a href="#readme-top">back to top</a>)</p>

# Attributions And Acknowledgements

### Acknowledgements
- Thanks to Hypergryph for actually providing said API as well the means to download high quality audio files direct from source instead of being forced to stream the music from Spotify or other means
	- Note: Thee songs retrieved from this software is obviously the property of Hypergryph Co. Ltd., Since the API is publicly exposed and other GitHub hosted downloading scripts exist i am assuming that retrieving and downloading these songs are allowed as longs as its not done commercially

### Attributions
- N/A
### Images
- N/A
