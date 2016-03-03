#!/usr/bin/python3.5

from config import BOTS_FOLDER, PREFIX
from discord import Client
import os
from secrets import secrets
import sys

if '--debug' in sys.argv:
    __DEBUG__ = True
elif '-d' in sys.argv:
    __DEBUG__ = True
else:
    __DEBUG__ = False

__BASE__ = os.path.abspath(os.path.dirname(__file__))
__MAIN__ = os.path.abspath(__file__)
__SHUCKLE__ = os.path.join(__BASE__, 'shuckle')
__BOTS__ = os.path.join(__BASE__, BOTS_FOLDER)

sys.path.append(__SHUCKLE__)

from shuckle.core import Toolbox

client = Toolbox(base=__BASE__, main=__MAIN__, bots=__BOTS__, prefix=PREFIX, debug=__DEBUG__)

if __name__ == '__main__':
    print('Starting up...')
    print('Debug status: {}'.format(__DEBUG__))
    print('Using user: ' + secrets.email)

    client.run(secrets.email, secrets.password)
