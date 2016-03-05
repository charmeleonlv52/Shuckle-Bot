from humanfriendly import parse_timespan

from .types import Timespan

def transform_bool(s):
    s = s.lower()
    if any(s == x for x in ['yes', 'y', 'true', 't', '1']):
        return True
    elif any(s == x for x in ['no', 'n', 'false', 'f', '0']):
        return False

def transform_timespan(s):
    return Timespan(parse_timespan(s))
