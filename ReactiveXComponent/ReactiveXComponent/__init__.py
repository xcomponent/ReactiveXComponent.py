__version__ = '1.0.0'

import logging
try:
    # not available in python 2.6
    from logging import NullHandler
except ImportError:

    class NullHandler(logging.Handler):

        def emit(self, record):
            pass

# Add NullHandler to prevent logging warnings
logging.getLogger(__name__).addHandler(NullHandler())

from ReactiveXComponent.xcomponentAPI import xcomponentAPI

from ReactiveXComponent.communication import publisher
from ReactiveXComponent.communication import xcConnection
from ReactiveXComponent.communication import xcSession
from ReactiveXComponent.configuration import serializer

##from pika.adapters import BaseConnection
##from pika.adapters import BlockingConnection
##from pika.adapters import SelectConnection
##from pika.adapters import TornadoConnection
##from pika.adapters import TwistedConnection
##from pika.adapters import LibevConnection
