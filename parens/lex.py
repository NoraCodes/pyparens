# lex.py
# Python Lisp LEXer

from string import whitespace

def lex(characters):
    "Convert a string of characters into a list of tokens."
    tokens = []
    current_token = ""
    pos = 0
    while pos < len(characters):  # returns immediately if there are 0 tokens
        # By default, just add the current character to current_token
        # Finding any other single-char token, like whitespace or a (,
        #   commits the contents of current_token to a token and
        #   begins anew.
        # This is most of the state in the lexer, along with position.

        # Whitespace - discard, but commit current_token
        if characters[pos] in whitespace:
            # Discard all whitespace
            if len(current_token) > 0:
                tokens.append(current_token)
                current_token = ""

        # Open paren token - commit current_token and commit a (
        elif characters[pos] == "(":
            # Open paren
            if len(current_token) > 0:
                tokens.append(current_token)
                current_token = ""
            tokens.append("(")

        # Close paren token - commit current_token and commit a )
        elif characters[pos] == ")":
            # Close paren
            if len(current_token) > 0:
                tokens.append(current_token)
                current_token = ""
            tokens.append(")")

        # Strings: doubles quotes make string literals
        elif characters[pos] == '"':
            # Commit current_token
            if len(current_token) > 0:
                tokens.append(current_token)
                current_token = ""

            # Do a string literal
            initial_pos = pos
            # +1 here so that the token gets the quote
            closing_pos = characters.find('"', pos+1) + 1
            if closing_pos > pos:
                # A complete string was found. It is a single token.
                tokens.append(characters[pos:closing_pos])
                pos = closing_pos - 1
            else:
                # No complete string was found.
                raise SyntaxError("Quote mismatch in string literal.")
        else:
            # Something else
            current_token += characters[pos]

        pos += 1

    return tokens
