REM for github actions shit
cd ..

coverage run -m unittest discover -v --buffer
coverage report -m
coverage json