import inspect

def get_internal(name):
    stack = inspect.stack()

    try:
        for frame in stack:
            frame = frame[0].f_locals

            if name in frame:
                return frame[name]

        return None
    except:
        pass