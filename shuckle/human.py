from discord import User
import humanfriendly

from util import get_id

'''
Attempts to turn a human readable condition
string into a series of compound functions.
'''

def get_compound(s):
    and_compound = ['and', '&&', '&']
    or_compound = ['or', '||', '|']

    if s.lower() in and_compound:
        return lambda x, y: x and y
    elif s.lower() in or_compound:
        return lambda x, y: x or y

    return None

def is_member(id):
    def check_member(test):
        if not isinstance(test, User):
            return False
        return test.id == id
    return check_member

def parse_helper(tokens, start, end):
    condition = []
    index = 0

    while index < end:
        token = tokens[x]

        # Is this a mention?
        # Assume that if the first token in the list
        # represents a member mention then we want the
        # user check to be the ONLY condition.
        if get_id(token):
            if index == 0 and end > 1 and not get_compound(tokens[1]):
                return is_member(token)
            condition.append(is_member(token))
        if get_compound(s):
            left = tokens[:index]
            right =

        index += 1

def parse_condition(tokens):
    return parse_helper(tokens, 0, len(tokens))
