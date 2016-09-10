# env.py
# Python Lisp ENVironment

from .common import Env


def standard_env():
    """
    An environment with some useful stuff
    """
    env = Env()

    # Add mathematical symbols
    import math
    env.update(vars(math))

    # Add fundamental operations
    import operator as op
    env.update({
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv,
        '%': op.mod, '^': op.pow,
        '=': op.eq, 'eq': op.eq,
    })

    # Add basic I/O
    env.update({
        'print': print
    })

    # Add standard library tools
    from . import plistd
    env.update(vars(plistd))
    # Alias a few of them to make them easier to use
    env.update({
        'list': plistd.makelist,
    })

    return env

global_env = standard_env()
