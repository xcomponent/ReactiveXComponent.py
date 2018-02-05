#!/bin/bash

source ./dev_up.sh

cd reactivexcomponent

echo Running lint...
pylint3 reactivexcomponent --extension-pkg-whitelist=lxml -f parseable > pylint.out

rc=$?; if [[ $rc != 0 ]]; then 
    echo Lint failed!
    cat pylint.out
    exit $rc; 
fi

echo Running tests...
nosetests3 tests/unit --with-xunit --with-cov --cov reactivexcomponent --exe
rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi

echo Checking setup.py...
python3 setup.py check
rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi

echo Creating source distribution package...
python3 setup.py sdist
rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi

cd ..

deactivate
