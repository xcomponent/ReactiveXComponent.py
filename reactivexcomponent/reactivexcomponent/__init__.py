import logging

from reactivexcomponent.xcomponentAPI import XcomponentAPI
from reactivexcomponent.communication import publisher
from reactivexcomponent.communication import xcConnection
from reactivexcomponent.communication import xcSession
from reactivexcomponent.configuration import serializer

__version__ = '1.0.0'

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
