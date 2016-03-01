def command(prefix, cmd):
    def dec(func):
        func._shuckle_command = (prefix, cmd)
        return func
    return dec