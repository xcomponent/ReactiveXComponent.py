# Reactive XComponent API for Python 

Reactive XComponent is a Python client API that allows you to interact with microservices generated with XComponent software.

## Build from source (on a Windows environment)
Use the *build* script to build the API from sources.
```
build.bat
```
A ``reactivexcomponent-X.Y.Z.tar.gz`` pip package is build on the *dist\reactivexcomponent* folder.

## Usage
Use the scripts *dev_up* and *dev_down* to activate and deactivate a virtualenv containing the reactivexcomponent API.

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

## Running unit tests
Use the *nose* runner to run unit tests.
```
dev_up.bat
cd reactivexcomponent
nosetests tests/unit reactivexcomponent
```

## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request

## License
Apache License V2

