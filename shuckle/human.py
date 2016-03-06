from tokenizer import Tokenizer

def is_and(s):
    return s.lower() in ['and', '&', '&&']

def is_or(s):
    return s.lower() in ['or', '|', '||']

def is_equal(s):
    return s.lower() in ['is', '=', '==']

def is_contains(s):
    return s.lower() in ['contains']

def is_in(s):
    return s.lower() in ['in']

def is_op(s):
    op_list = [is_and, is_or, is_equal, is_contains, is_in]
    return any(x(s) for x in op_list)

class Human(object):
    def __init__(self, s):
        self.tokens = Tokenizer(s)
        self.parse()
        self.build_tree()

    def parse(self):
        tokens = self.tokens.tokens
        stack = []
        queue = []

        for token in tokens:
            if is_and(token):
                while len(stack) and not is_or(stack[-1]):
                    queue.append(stack.pop())
                stack.append(token)
            elif is_or(token):
                while len(stack) and not is_or(stack[-1]):
                    queue.append(stack.pop())
                stack.append(token)
            elif is_equal(token) or is_contains(token) or is_in(token):
                while len(stack) and not is_and(stack[-1]) and not is_or(stack[-1]):
                    queue.append(stack.pop())
                stack.append(token)
            else:
                queue.append(token)

        queue.extend(stack[::-1])

        self.queue = queue


if __name__ == '__main__':
    test = Human('{author} is <@24234524342343423> or {message} contains "herp derp" and {attachment}')
    print test.queue
