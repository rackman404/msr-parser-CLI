
cd ..

cd ./.venv/Scripts
call activate.bat
cd ../..

pylint --fail-under=8 msr_parser_main msr_parser_code
if ERRORLEVEL 1 echo Failed Lint (Score under below 8 out of 10)

pause