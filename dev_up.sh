#!/bin/bash
cd reactivexcomponent

echo Creating virtual environment...
virtualenv -p python3 venv
source $PWD/venv/bin/activate

echo Installing dependencies...
export LANG=en_US.UTF-8
pip3 install -r ../requirements.txt
rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi

cd ..
