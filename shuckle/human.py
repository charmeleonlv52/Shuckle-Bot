# from discord import Member

from tokenizer import Tokenizer
# from util import get_id

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

def is_has(s):
    return s.lower() in ['has']

def is_mentions(s):
    return s.lower() in ['mentions']

def is_not(s):
    return s.lower() in ['not']

def is_op(s):
    op_list = [is_and, is_or, is_equal, is_contains, is_in, is_has, is_mentions]
    return any(x(s) for x in op_list)

class Human(object):
    def __init__(self, s):
        self.tokens = Tokenizer(s)
        self.queue = []
        self.wildcards = []

        self.parse()

    def create_eval(self):
        eval_stack = []
        working_queue = []
        index = 0

        for token in self.queue:
            if is_op(token):
                # Check for unary operator
                if is_not(token):
                    x = eval_stack.pop()

                    def closure(x):
                        def func_not():
                            return not x()
                        return func_not

                    eval_stack.append(closure(x))
                elif is_has(token):
                    x = working_stack.pop()

                    if x == 'attachment':
                        def closure(i):
                            def func_has():
                                return self.wildcards[i].attachments

                            return func_has

                        eval_stack.append(closure(index))

                        index += 1
                elif is_mentions(token):
                    x = working_stack.pop()
                    x = int(get_id(x))

                    def closure(i):
                        def func_mentions():
                            return any(m.id == x for m in self.wildcards[i].id)

                        return func_mentions

                    eval_stack.append(closure(index))

                    index += 1
                # Check for binary operators
                elif is_and(token):
                    x = eval_stack.pop()
                    y = eval_stack.pop()

                    def closure(x, y):
                        def func_and():
                            return x() and y()
                        return func_and

                    eval_stack.append(closure(x, y))
                elif is_or(token):
                    x = eval_stack.pop()
                    y = eval_stack.pop()

                    def closure(x, y):
                        def func_or():
                            return x() or y()
                        return func_or

                    eval_stack.append(closure(x, y))
                elif is_equal(token):
                    x = eval_stack.pop()
                    y = eval_stack.pop()

                    def closure(x, y):
                        def func_equal():
                            return x() == y()
                        return func_equal

                    eval_stack.append(closure(x, y))
                elif is_contains(token):
                    x = eval_stack.pop()
                    y = eval_stack.pop()

                    def closure(x, y):
                        def func_contains():
                            return x() in y()
                        return func_contains

                    eval_stack.append(closure(x, y))
                elif is_in(token):
                    x = eval_stack.pop()
                    y = eval_stack.pop()

                    def closure(x, y):
                        def func_in():
                            return y() in x()
                        return func_in

                    eval_stack.append(closure(x, y))
            # Wildcards that will change on a per-message basis
            elif token in ['author', 'message', 'attachment']:
                self.wildcards.append(token)

                def closure(i):
                    def func_wc():
                        return self.wildcards[i]
                    return func_wc

                eval_stack.append(closure(index))

                index += 1
            else:
                def closure(x):
                    def literal():
                        return x
                    return literal

                eval_stack.append(closure(token))

        func = eval_stack.pop()

        def compound(wc):
            self.wildcards = wc
            return func()

        return self.wildcards, compound

    def parse(self):
        stack = []
        queue = []

        for token in self.tokens.tokens:
            if is_and(token):
                while len(stack) and not is_or(stack[-1]):
                    queue.append(stack.pop())
                stack.append(token)
            elif is_or(token):
                while len(stack) and not is_or(stack[-1]):
                    queue.append(stack.pop())
                stack.append(token)
            elif is_op(token):
                while len(stack) and not is_and(stack[-1]) and not is_or(stack[-1]):
                    queue.append(stack.pop())
                stack.append(token)
            else:
                queue.append(token)

        queue.extend(stack[::-1])

        self.queue = queue

if __name__ == '__main__':
    test = Human('author is <@1312313141341133> or car in racecar')
    print test.queue
    # print test.create_eval()
    args, func = test.create_eval()
    print func(['<@1312313141341133>'])
