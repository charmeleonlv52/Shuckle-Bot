from humanfriendly import parse_timespan

def transform_bool(s):
    s = s.lower()
    if any(s == x for x in ['yes', 'y', 'true', 't', '1', 'on']):
        return True
    elif any(s == x for x in ['no', 'n', 'false', 'f', '0', 'off']):
        return False

def transform_timespan(s):
    return parse_timespan(s)
