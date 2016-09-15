# parse.py
# Python Lisp PARSEr

from .atom import atom


def preparse(tokens):
    """
    Break up a tokenized source into lists; this allows input like
    pl> (a, b) (c, d)
    to work as expected.
    """
    count_open = 0
    lists = []
    current_list = []

    if len(tokens) == 0:
        raise SyntaxError("Unexpected EOF while preparsing.")

    for token in tokens:
        if token == '(':
            count_open += 1
            current_list.append('(')
        elif token == '\'(':
            count_open += 1
            current_list.append('\'(')
        elif token == ')':
            if count_open == 0:
                # Too many closing parens
                raise SyntaxError(" Unexpected ) while preparsing!")
            count_open -= 1
            current_list.append(')')
            if count_open == 0:
                # This list is done; split it off and start a new one
                lists.append(current_list)
                current_list = []
        else:
            # Any other token
            current_list.append(token)
            continue

        # Once the loop is done, there can't be any remaining open
        #   parentheses, or the source is unbalanced
    if count_open != 0:
        raise SyntaxError("Missing a closing parenthesis while" +
                          "preparsing ({}).".format(count_open))

    return lists


def parse_single(tokens):
    """
    Take lexed tokens and turn them into a list of lists, numbers, and symbols
    """
    if len(tokens) == 0:
        raise SyntaxError("Unexpected EOF while parsing.")
    token = tokens.pop(0)
    # We need to have a paren to start a list, otherwise we'll just eval one
    # TODO
    if token in ('\'(', '('):
        L = []
        if token == '\'(':
            L.append('quote')
        try:
            while tokens[0] != ')':
                # Until we get to the end of this paren enclosure, recurse
                L.append(parse_single(tokens))
            tokens.pop(0)
        except IndexError:
            raise SyntaxError("Missing a closing parenthesis.")
        return L
    elif token == ')':
        # Too many closing parens
        raise SyntaxError(" Unexpected ) while parsing!")
    else:
        return atom(token)


def parse(tokens):
    """
    Take lexed tokens and turn them into a list of lists
    """
    token_lists = preparse(tokens)
    lists = []
    for token_list in token_lists:
        lists.append(parse_single(token_list))

    return lists
