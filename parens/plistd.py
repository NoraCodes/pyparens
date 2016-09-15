# plistd.py
# Python LIsp STanDard library


def makelist(*args):
    " Create a list from arguments. "
    return list(args)


def quote(*args):
    return ['"{}"'.format(a) if isinstance(a, str) else a for a in args]


def cond(test, then, else_=False, *, env):
    from .eval import eval
    return eval(then if test else else_, env)
