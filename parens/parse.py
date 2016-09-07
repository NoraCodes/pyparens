# parse.py
# Python Lisp PARSEr

from .atom import atom

def parse(tokens):
    """
    Take lexed tokens and turn them into lists of numbers and symbols
    """
    if len(tokens) == 0:
        raise SyntaxError("Unexpected EOF while parsing.")
    token = tokens.pop(0)
    # We need to have a paren to start a list, otherwise we'll just eval one
    # TODO
    if token == '(':
        L = []
        try:
            while tokens[0] != ')':
                # Until we get to the end of this paren enclosure, recurse
                L.append(parse(tokens))
            tokens.pop(0)
        except IndexError:
            raise SyntaxError("Missing a closing parenthesis.")
        return L
    elif token == ')':
        # Too many closing parens
        raise SyntaxError(" Unexpected ) while parsing!")
    else:
        return atom(token)
