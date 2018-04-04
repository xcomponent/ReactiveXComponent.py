cd reactivexcomponent

echo Running flake8...
flake8 reactivexcomponent > flake8.out

echo Running tests...
nosetests tests/unit --with-xunit --with-cov --cov reactivexcomponent --exe
IF ERRORLEVEL 1 EXIT /B 1

echo Checking setup.py...
python setup.py check
IF ERRORLEVEL 1 EXIT /B 1

echo Creating source distribution package...
python setup.py sdist
IF ERRORLEVEL 1 EXIT /B 1

cd ..
