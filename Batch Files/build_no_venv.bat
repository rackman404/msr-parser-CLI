REM https://stackoverflow.com/questions/37319911/python-how-to-specify-output-folders-in-pyinstaller-spec-file
cd ..
pyinstaller --distpath ./_PYINSTALLER/dist --workpath ./_PYINSTALLER/build --onefile -n msr_downloader_CLI ./msr_parser_main.py