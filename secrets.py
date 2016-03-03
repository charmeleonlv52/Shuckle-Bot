from config import config
import json
import os
from object import Object

secrets = Object()

with open(config.secrets_path) as f:
    lines = ''.join(f.readlines())

    s = json.loads(lines)

    secrets.update(s)
