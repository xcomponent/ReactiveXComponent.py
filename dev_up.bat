cd reactivexcomponent

echo Creating virtual environment...
virtualenv venv
call venv\Scripts\activate.bat

echo Installing dependencies...
set LANG=en_US.UTF-8
pip install -r ..\requirements.txt
IF ERRORLEVEL 1 EXIT /B 1

cd ..
