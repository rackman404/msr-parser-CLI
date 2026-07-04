
Detailed here are just the raw functional and non functional requirements consolidated from several random places (i.e notepad, notion) i noted down, see the SRS document for a more official version. 


# Generic API 
- All API calls must follow any rules given by external APIs (i.e max amount of requests/second)
- All API calls should have a CONTENT HEADER with a appropriate "user-agent" denoting name of application and Github repo URL


### Folder and Executable Dependencies
- Must check if user defined OR hardcoded "data" folders exist/can be created
- Must check if "cache"  folders exist/can be created
- Should not include FFmpeg.exe with application BUT instead check if user has placed a .exe of it in either a "deps" folder OR it is pathed in the ENV variable

### File Conversions/Metadata
- Convert any downloaded .wav files into user defined file format (i.e .flac, .mp3, .ogg) if provided
	- Must use FFmpeg for this
- Add Metadata to any converted audio files
	- Only provide metadata if audio file is not .wav
	- if flag "-nomusicbrainz" enabled, only provide metadata from any metadata included in the MSR APIs
	- if using musicbrainz, must not request from their API more than once a second

### Python CLI GUI
- Provide a rich Console GUI (i.e colors, large textual headers, loading bars)
	- Must cleanly show any major steps the program takes under big headers and minor steps under sub headers
	- Show loading bars when downloading assets (i.e .wav, .lrc, .png) as well as when converting to different audio formats (i.e .wav -> .flac) so that user doesn't get confused if it looks like program has hung
- Possible CLI command arguments provided by user should match the following (IMPORTANT):
	- msr_parser.exe {name/cID NOTE: only if -all is not used} {-album/-single/-all} (-nomusicbrainz) (-o) (-exact) (-folder) (-output "folder_path") (-fileformat ".mp3"/".flac"/".ogg")
	- Note: (arg) is optional {arg} is mandatory 
	- Note: order of args should not matter (except {name/cID}, which should always be the first arg if provided)
	
### MSR API
- Search the MSR API for available songs given a user inputted "name" or "cID"
	- If no songs are available, exit
	- If songs are available, ask user if program can continue
	- If flag "-o" enabled, simply continue without user confirmation
		- Default behaviour is to force user to provide a Y/N input (in upper OR lowercase)
	- If flag "-exact" enabled, 
		- Default behaviour is to search for and return any match cID or name substring 
- Must provide the following means of downloading from MSR API
	- Options
		- if flag "-album" Download by Album (provided cID or Album Name)
		- if flag "-single" Download by Single (provided cID or song Name)
		- if flag "-all" Disregard any names or cID provided (or just ignore if not provided) and literally download every single song from their servers
	- For Both download options:
		- if flag "-folder" enabled, they should download to the designated download folder in their own subfolders (even if "Download by Single" is used)
- Locally cache any downloaded .JSON files (except master lists) from MSR API to avoid making unnecessary API calls to their servers (EXCEPTION: can use cached master list .JSON when developing the CLI tool, to avoid unnecessary API calls)  
	-  Also applies to any data gathered from musicbrainz API

### Github Workflow
- Have a script to run pytest files -> auto pyinstaller packaging -> upload to github releases

# Non Functional Requirements

- Security/Maintainability: 
	- Should use as little EXTERNAL python libraries and other executables/.dlls as much as possible to limit security vulnerabilities and to make maintaining program easier in the future as possible