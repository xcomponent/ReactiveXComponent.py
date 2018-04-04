#!/bin/bash
cd reactivexcomponent

echo Running lint...
flake8 reactivexcomponent > flake8.out

rc=$?; if [[ $rc != 0 ]]; then 
    echo Flake8 failed!
    cat flake8.out
    exit $rc; 
fi

echo Running tests...
nosetests tests/unit --with-xunit --with-cov --cov reactivexcomponent --exe
rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi

echo Checking setup.py...
python3 setup.py check
rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi

echo Creating source distribution package...
python3 setup.py sdist
rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi

cd ..
