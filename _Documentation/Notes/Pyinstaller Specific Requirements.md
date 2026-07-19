Last Modified 07-19
# Overview
Specific shit done to account for the use of PyInstaller.

# Pathing (Working Directory)
- After packaging into binary, assuming that --onefile is used, then launching the executable will cause it to have a relative temp directory somewhere random in the C: drive (or elsewhere).
- To fix:
``` python
#https://stackoverflow.com/questions/404744/determining-application-path-in-a-python-exe-generated-by-pyinstaller
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    cwd = os.path.dirname(sys.executable)
    print('running in a PyInstaller bundle')
else:
    cwd = os.path.dirname(__file__)
    print('running in a normal Python process')
```
where cwd should be used in place of the standard "os.path.dirname(__file__)".

# Custom Output Folder
- By default PyInstaller will place a /build/ and a /dist/ folder in the root project directory
- This clutters the project a bit
- To fix, two args can be passed, --distpath {path} and --workpath {path}: 
``` shell
pyinstaller --distpath ./_PYINSTALLER/dist --workpath ./_PYINSTALLER/build ...(rest of line)
```
