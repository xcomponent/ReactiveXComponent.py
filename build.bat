cd ReactiveXComponent

echo Creating virtual environment...
virtualenv venv
call venv\Scripts\activate.bat

echo Installing dependencies...
set LANG=en_US.UTF-8
pip install -r ..\requirements.txt
IF ERRORLEVEL 1 EXIT /B 1

echo Running lint...
pylint reactivexcomponent -f parseable
IF ERRORLEVEL 1 EXIT /B 1

echo Running tests...
nosetests tests --with-xunit --with-coverage
IF ERRORLEVEL 1 EXIT /B 1

echo Checking setup.py...
python setup.py check
IF ERRORLEVEL 1 EXIT /B 1

echo Creating source distribution package...
python setup.py sdist
IF ERRORLEVEL 1 EXIT /B 1

echo Leaving virtual environment...
call venv\Scripts\deactivate.bat
IF ERRORLEVEL 1 EXIT /B 1

cd ..
