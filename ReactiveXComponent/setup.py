from distutils.core import setup
import os

# Conditionally include additional modules for docs
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
requirements = list()
if on_rtd:
    requirements.append('websocket')
    requirements.append('lxml')
    #requirements.append('pyev')

setup(
    name = 'ReactiveXComponent',
    packages = ['ReactiveXComponent','ReactiveXComponent.communication','ReactiveXComponent.configuration'],
    version = '1.0.0',
    description = 'Python API for XComponent Platform',
    author = 'INVIVOO SOFTWARE',
    author_email = 'dev@xcomponent.com',
    url = 'https://github.com/xcomponent/ReactiveXComponent.py',
    classifiers = ["Programming Language :: Python 3.5"]
    )
