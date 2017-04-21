from distutils.core import setup
import os

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

setup(
    name='reactivexcomponent',
    packages=['reactivexcomponent', 'reactivexcomponent.communication', 'reactivexcomponent.configuration'],
    version='1.0.0',
    description='Python API for XComponent Platform',
    author='INVIVOO SOFTWARE',
    author_email='dev@xcomponent.com',
    url='https://github.com/xcomponent/ReactiveXComponent.py',
    classifiers=["Programming Language :: Python 3.5"]
    )
