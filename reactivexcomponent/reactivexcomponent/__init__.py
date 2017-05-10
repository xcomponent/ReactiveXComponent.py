import logging

from reactivexcomponent.xcomponent_api import XcomponentAPI

__version__ = '1.0.0'

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
