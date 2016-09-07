# atom.py
# Python Lisp ATOM definition

from .common import *

def atom(token):
    """
    Numbers -> numbers, everything else -> symbols.
    """
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            # Python strs are Lisp symbols, unless they have " in them,
            #   which is handled AFTER this.
            return Symbol(token)
