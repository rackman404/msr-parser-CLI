
REM echo %cd%
REM cd ..

cd ./../.venv/Scripts
call activate.bat
cd ../..

REM https://stackoverflow.com/questions/37319911/python-how-to-specify-output-folders-in-pyinstaller-spec-file
pyinstaller --distpath ./_PYINSTALLER/dist --workpath ./_PYINSTALLER/build --onefile -n msr_downloader_CLI ./msr_parser_main.py

cd ./.venv/Scripts
call deactivate.bat
cd ../..

pause