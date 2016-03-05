#!/usr/bin/python3.5

from discord import Client
import os
import sys

from config import config
from secrets import secrets

if '--debug' in sys.argv:
    __DEBUG__ = True
elif '-d' in sys.argv:
    __DEBUG__ = True
else:
    __DEBUG__ = False

__BASE__ = os.path.abspath(os.path.dirname(__file__))
__MAIN__ = os.path.abspath(__file__)
__DATA__ = os.path.join(__BASE__, 'data')
__SHUCKLE__ = os.path.join(__BASE__, 'shuckle')
__BOTS__ = os.path.join(__BASE__, config.bots_folder)

sys.path.append(__SHUCKLE__)

from shuckle.core import Toolbox

client = Toolbox(
    base=__BASE__,
    main=__MAIN__,
    data=__DATA__,
    bots=__BOTS__,
    prefix=config.prefix,
    debug=__DEBUG__
)

if __name__ == '__main__':
    print('Starting up...')
    print('Debug status: {}'.format(__DEBUG__))
    print('Using user: ' + secrets.email)

    client.run(secrets.email, secrets.password)
