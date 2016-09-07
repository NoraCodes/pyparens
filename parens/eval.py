# eval.py
# Python Lisp EVALuation function

import importlib

from .common import *
from .env import global_env

def eval(x, env=global_env):
    """
    Evaluate an expression x in an env
    """
    if isinstance(x, Symbol):
        if x[0] == '"':
            # It's a string literal
            # Cut off the quotes and return it as such
            return x[1:-1]

        # Variable lookup
        try:
            val = env[x]
        except KeyError:
            try:
                val = globals()[x]
            except:
                raise NameError("No variable named {}".format(x))
        return val
    elif not isinstance(x, List):
        # const. literal
        return x
    elif x[0] == 'quote':
        # (quote exp)
        try:
            (_, exp) = x
        except ValueError:
            exp = False
        return exp
    elif x[0] == 'if':
        try:
            # With an alt clause
            (_, test, conseq, alt) = x
        except ValueError:
            try:
                # Without an alt clause, defaults to False
                (_, test, conseq) = x
                alt = False
            except ValueError:
                raise SyntaxError(
                    "if requires two or three arguments" +
                    "(test, consqeuence, and optional alternative)")
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif x[0] == 'define':
        try:
            (_, var, exp) = x
        except ValueError:
            raise SyntaxError(
                "define requires exactly two arguments " +
                "(the name of the variable and its value)")
        val = eval(exp, env)
        env[var] = val
        # This is not standard Lisp, but I like it
        return val
    elif x[0] == 'import':
        try:
            (_, exp) = x
        except ValueError as e:
            raise SyntaxError(
                "import requires exactly 1 argument " +
                "(the name of the module). {}".format(e))
        val = eval(exp, env)
        return importlib.import_module(val)
    else:
        # This is the default case:
        # (f arg1 arg2 .. argn)
        proc = eval(x[0], env)
        args = [eval(arg, env) for arg in x[1:]]
        try:
            return proc(*args)
        except TypeError as e:
            if hasattr(proc, '__call__'):
                # Callable, but wrong number of args or something
                raise NameError(e)
            raise NameError("Tried to call a non-callable Python object {} " +
                            "(its type is {})".format(x[0], type(proc)))

