cd reactivexcomponent

echo Creating virtual environment...
virtualenv venv
call venv\Scripts\activate.bat

echo Installing dependencies...
set LANG=en_US.UTF-8
pip install -r ..\requirements.txt
IF ERRORLEVEL 1 EXIT /B 1

echo Running lint...
pylint reactivexcomponent -f parseable > pylint.out
IF ERRORLEVEL 1 (
	echo Lint failed!
	type pylint.out
	EXIT /B 1
)

echo Running tests...
<<<<<<< HEAD
cd tests/unit
python -m unittest discover
cd ../../
::nosetests tests/unit --with-xunit --with-cov --cov reactivexcomponent
=======
nosetests tests/unit --with-xunit --with-cov --cov reactivexcomponent 
>>>>>>> b31eddd530c8e7c09a3dbda0ab6d7eee21461058
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
