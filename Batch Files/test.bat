REM for manual testing
cd ..

cd ./.venv/Scripts
call activate.bat
cd ../..

coverage run -m unittest discover -v --buffer
REM python -m unittest discover -v --buffer
coverage report -m

pause