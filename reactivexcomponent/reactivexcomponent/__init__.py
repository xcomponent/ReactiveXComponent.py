__version__ = '1.0.0'

import logging
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):

        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())

from reactivexcomponent.xcomponentAPI import XcomponentAPI

from reactivexcomponent.communication import publisher
from reactivexcomponent.communication import xcConnection
from reactivexcomponent.communication import xcSession
from reactivexcomponent.configuration import serializer
