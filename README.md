# msr-parser-CLI

<a id="readme-top"></a>

<div align="center">
  <h1 align="center">MSR Parser Python CLI and GUI</h3>
   <h3 align="center">Version: Pre-V1.0</h3>

  <p align="center">
     Simple Python based CLI tool (with simple GUI .exe if you don't like CLI) for downloading and auto tagging song content from  <a href="(https://monster-siren.hypergryph.com)">Hypergryph's Official Music Website</a>.
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
![[preview_v0_1_0.png.png]]
<sub>Preview Pre V1.0 of CLI </sub>


TBD Screenshot
<sub>Preview Pre V1.0 of GUI </sub>



Simple CLI and GUI for downloading songs from Arknights. 


# Usage

### CLI

If using the CLI, you must run it by opening the folder in terminal, then running the included .exe using command line arguments (see the following link if you're not familiar with the concept): [Command Line Arguments in Python](https://www.geeksforgeeks.org/python/command-line-arguments-in-python/_)

### Possible Flags and Arguments 

Below are the supportted flags and arguments (both optional and mandatory) that should be set to use this CLI correctly:


| Argument | Is Flag | Mandatory/Optional | Description | Default Behaviour if Optional |
| -------- | ------- | ------------------ | ----------- | ----------------------------- |
|          |         |                    |             |                               |



# Built With

- We note that the built in Unittest python lib was used for Unit and End to End Testing
- We note that Github Workflow scripts were used to build the binaries 
### Python Stack (External Libraries)
* [![Tech Stack Badge](https://img.shields.io/badge/Pyinstaller-blue?style=for-the-badge&logo=python&logoColor=61DAFB)](https://www.electronjs.org) - Python Standalone Binary Builder
	*  [![Tech Stack Badge](https://img.shields.io/badge/mutagen-red?style=for-the-badge&logo=python&logoColor=61DAFB)](https://mui.com) - Audio File Metadata Library
	*  [![Tech Stack Badge](https://img.shields.io/badge/Requests-red?style=for-the-badge&logo=python&logoColor=61DAFB)](https://mui.com) - HTTP Library
	-  [![Tech Stack Badge](https://img.shields.io/badge/tqdm-red?style=for-the-badge&logo=python&logoColor=61DAFB)](https://mui.com) - Console Progress Bar Library
	- TBD - Python GUI Library
### Languages
* [![Tech Stack Badge](https://img.shields.io/badge/Python-green?style=for-the-badge&logo=python&logoColor=61DAFB)]([https://rust-lang.org/](https://rust-lang.org/)) 

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

(NOTE TO SELF: include license that requires crediting developer)


<p align="right">(<a href="#readme-top">back to top</a>)</p>

# Attributions And Acknowledgements

### Acknowledgements
- Code snippets and general programming assistance was obtained from Stack Overflow and other websites, links to relevant forum posts have been included in the source code where relevant
- Thanks to Hypergryph for actually providing said API as well the means to download high quality audio files direct from source instead of being forced to stream the music from Spotify or other means
	- Note: Thee songs retrieved from this software is obviously the property of Hypergryph Co. Ltd., Since the API is publicly exposed and other GitHub hosted downloading scripts exist i am assuming that retrieving and downloading these songs are allowed as longs as its not done commercially

### Attributions
- N/A
### Images
- N/A
