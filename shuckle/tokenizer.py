from shlex import shlex

class Tokenizer(object):
    def __init__(self, s):
        self.tokens = shlex(s, posix=True)
        self.tokens.whitespace_split = True

        token = self.tokens.get_token()
        tokens = []

        while token is not None:
            tokens.append(token)
            token = self.tokens.get_token()

        self.tokens = tokens

    def has_next(self):
        return len(self.tokens) > 0

    def peek(self):
        if not self.has_next():
            return None
        return self.tokens[0]

    def next(self):
        if not self.has_next():
            return None
        return self.tokens.pop(0)

    def swallow(self):
        if not self.has_next():
            return None
        return [x for x in self]

    def __iter__(self):
        return self

    def __next__(self):
        if not self.has_next():
            raise StopIteration
        else:
            return self.next()
