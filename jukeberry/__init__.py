'''
jukeberry is a jukebox application written in python.
It is meant to be run on a raspberry pi, but can run on
any computer with python installed.

'''
from __future__ import print_function, absolute_import

__version__ = '2.1.1'
__author__ = 'Mike Biacaniello'
__maintainer__ = 'Mike Biacaniello'
__email__ = 'chepazzo@gmail.com'
__url__ = 'https://github.com/chepazzo/jukeberry'
__shortdesc__ = 'Jukebox application optimized for raspberry pi.'

## Configure logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
log.addHandler(ch)
log.debug('loading {}'.format(__name__))

## Configure settings
from .conf import settings

DEFAULT_SETTINGS = """
[GLOBAL]
DEBUG=True
THREADED=True
SSL=False
AUTOLOAD=False
PLAYER=omxplayer
#PLAYER=mpg123
LIB=/var/media/music/

[WEB]
# Put all web API config here
HOST=0.0.0.0
PORT=5000
"""

settings.bool_fields = ['DEBUG', 'AUTOLOAD', 'SSL', 'THREADED']
settings.int_fields = ['PORT']
settings.float_fields = []
settings.cust_fields = {}
settings.load(confstr=DEFAULT_SETTINGS)
