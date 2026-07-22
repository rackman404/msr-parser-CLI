Last Modified 07-21

# OS_Check

## Referenced Python Module and Test Module
- os_check.py
- test_os_check.py

## General Overview
Creates/Validates that folders exist.
Also checks if binary dependencies can be found in a ENV variable or in deps folder

NOTE: we only test dependencies checking functionality, folder detection and creation is assumed to always work

### Test Development Specification

Folder Checking:
- Predefined Folders (i.e cache, deps, etc..) not created ER: Create them and return folder paths
- Predefined Folders created ER: return their valid folder paths
- User defined output folder path passed in (not exist) - ER: return nothing
	- Reasoning: we can technically just return the predefined output folder path but user would not be aware their own custom output directory is not valid
- User defined output folder path passed in (exists) - ER: return valid folder paths 

Dependencies Checking:
- Dependencies exist somewhere detectable (ENV or deps folder) ER: return either ENV or dep path to dependency
- Dependencies don't exist ER: return nothing

## Test Cases
Test Steps for multi step processes (not needed when just testing singular functions)

| Test Title                       | Preconditions                                                                      | Test Description                                                                | Expected Result                                                      | Comments                                                | Test Steps |
| -------------------------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------- | ---------- |
| no files at all                  | Mock no valid env and rel path                                                     | Test if no envs are passed in to check for validity/creation                    | Returns nothing                                                      |                                                         | N/A        |
| dep exists in ENV and rel        | Mock valid ENV and rel path                                                        | test if binary dependencies exist in both ENV var and relative folder directory | Return paths specified in env                                        | Returns ENV instead of relative folder because priority | N/A        |
| dep exists in rel                | Mock valid path in /deps/ folder                                                   | test if binary dependencies exist in both ENV var and relative folder directory | Return paths in /deps/ folder                                        |                                                         | N/A        |
| dep exists in ENV                | Mock valid path in a ENV variable with dep name                                    | test if binary dependencies exist in both ENV var and relative folder directory | Return paths in ENV variables                                        |                                                         | N/A        |
| ---                              |                                                                                    |                                                                                 |                                                                      |                                                         |            |
| folders no exist                 | - Mock os.exists to return false<br>- Mock folder paths                            |                                                                                 | Create them and return folder paths                                  |                                                         | N/A        |
| folders exist                    | - Mock os.exists to return true<br>- Mock folder paths                             |                                                                                 | return folder paths                                                  |                                                         | N/A        |
| user def output folder exists    | - Mock os.exists to return true<br>- Mock folder paths<br>- Mock user folder path  |                                                                                 | return folder paths with replaced output folder with user def folder |                                                         | N/A        |
| user def output folder no exists | - Mock os.exists to return false<br>- Mock folder paths<br>- Mock user folder path |                                                                                 | return nothing                                                       |                                                         | N/A        |

