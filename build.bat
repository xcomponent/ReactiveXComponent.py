call dev_up.bat

cd reactivexcomponent

echo Running lint...
pylint reactivexcomponent -f parseable > pylint.out
IF ERRORLEVEL 1 (
	echo Lint failed!
	type pylint.out
	EXIT /B 1
)

echo Running tests...
nosetests tests/unit --with-xunit --with-cov --cov reactivexcomponent
IF ERRORLEVEL 1 EXIT /B 1

echo Checking setup.py...
python setup.py check
IF ERRORLEVEL 1 EXIT /B 1

echo Creating source distribution package...
python setup.py sdist
IF ERRORLEVEL 1 EXIT /B 1

cd ..
call dev_down.bat
