[![](http://slack.xcomponent.com/badge.svg)](http://slack.xcomponent.com/)
[![Build Status](https://travis-ci.org/xcomponent/ReactiveXComponent.py.svg?branch=master)](https://travis-ci.org/xcomponent/ReactiveXComponent.py)

# Reactive XComponent API for Python 

Reactive XComponent is a Python client API that allows you to interact with microservices generated with XComponent software.

## Build from source (on a Windows environment)
Use the *build* script to build the API from sources.
```
build.bat
```
A ``reactivexcomponent-X.Y.Z.tar.gz`` pip package is build on the *dist\reactivexcomponent* folder.

## Build from source (on a Linux/OSX environment)
Use the *build* script to build the API from sources.
```
./build.sh
```
A ``reactivexcomponent-X.Y.Z.tar.gz`` pip package is build on the *dist\reactivexcomponent* folder.


## Development

### Dependencies 

- Python 3
- Pip
- Virtualenv
- python3-nose
- Pylint

### Starting up environment

Use the scripts *dev_up* and *dev_down* to activate and deactivate a virtualenv containing the reactivexcomponent API.

Windows example:
```
> dev_up.bat
(venv) > python3
> python
Python 3.6.1 (v3.6.1:69c0db5, Mar 21 2017, 18:41:36) [MSC v.1900 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import reactivexcomponent
>>> exit()

(venv) > dev_down.bat
> 
```

Linux/OSX example:
```
> source dev_up.sh
(venv) > python3
> python3
Python 3.6.1 (v3.6.1:69c0db5, Mar 21 2017, 18:41:36) [MSC v.1900 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import reactivexcomponent
>>> exit()

(venv) > deactivate
> 
```

## Sample code

Create a file called `test.py`.

```python
from reactivexcomponent.xcomponent_api import XcomponentAPI

def callback(error, session):
    if error is not None:
        print('Error connecting to WebSocket bridge')
	print(error)
    if session is not None:
	publisher = session.create_publisher()
	publisher.send_message('COMPONENT NAME', 'STATEMACHINE NAME', 'MESSAGE TYPE', { 'JSON': 'MESSAGE' })

xc_api_file = "PATH TO A XCAPI FILE GENERATED BY XCStudio"
server_url = "wss://WEB_SOCKET_BRIDGE_SERVER:443"
api = XcomponentAPI()
api.create_session(xc_api_file, server_url, callback)
```

Run the Web socket bridge from a XComponent project and then run the test file as `python test.py`.

## Running unit tests

Use the *nose* runner to run unit tests.
```
dev_up.bat (or source dev_up.sh) 
cd reactivexcomponent
nosetests3 tests/unit reactivexcomponent --exe
```

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request
## License

Apache License V2

