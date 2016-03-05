import json
import os

from config import config
from object import Object

secrets = Object()

with open(config.secrets_path) as f:
    s = json.loads(f.read())
    secrets.update(s)
