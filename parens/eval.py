# eval.py
# Python Lisp EVALuation function

import importlib

from .common import Symbol, List
from .env import global_env


def get_var(x, env):
    " Look up a variable in the env. If it's not there, look it up globally. "
    try:
        val = env[x]
    except KeyError:
        try:
            val = globals()[x]
        except:
            raise NameError("No variable named {}".format(x))
    return val


def dot_extraction(x, env):
    'Dot notation extraction: e.g. (. obj attr) will give obj.attr'
    if len(x) == 3:
        (_, parent, child) = x
        return getattr(eval(parent, env), child)
    else:
        raise SyntaxError("Dot extraction requires " +
                          "exactly two arguments.")


def wants_env(f):
    from inspect import signature
    try:
        sig = signature(f)
    except ValueError:
        return False
    for param in sig.parameters.values():
        if (param.kind == param.KEYWORD_ONLY and
            param.name == 'env'):
            return True
    return False

def eval(x, env=global_env):
    """
    Evaluate an expression x in an env
    """
    if isinstance(x, Symbol):
        if x[0] == '"':
            # x is a string literal
            # Cut off the quotes and return it as such
            return x[1:-1]

        # OK, it's a variable.
        return get_var(x, env)

    # Maybe x isn't a list but some kind of literal
    elif not isinstance(x, List):
        # const. literal
        return x

    # OK, x is a list, but is it empty?
    elif len(x) == 0:
        return []

    # It isn't empty... maybe it's a special form.
    # Dot extraction special form
    elif x[0] == '.':
        return dot_extraction(x, env)

    # Conditional special form
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

    # Variable definition special form
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

    # Import special form
    elif x[0] == 'import':
        try:
            (_, exp) = x
        except ValueError as e:
            raise SyntaxError(
                "import requires exactly 1 argument " +
                "(the name of the module). {}".format(e))
        return importlib.import_module(exp)

    else:
        # This is the default case:
        # (f arg1 arg2 .. argn)
        # or perhaps
        # (item1 item2 ... itemn)

        # Evaluate the first item, to see if it gives us back a callable
        proc = eval(x[0], env)

        # Handle the case of (item1 item2 ... itemn)
        if not callable(proc):
            # If input is of the form (item), put item in a list and we're done
            if len(x) == 1:
                return [proc]
            else:
                # If there are more elements, eval them and put them in a list
                L = [proc]
                for item in x[1:]:
                    L.append(eval(item))
                return L

        # OK, input is of the form (f arg1 arg2 ... argn)
        args = [eval(arg, env) for arg in x[1:]]
        try:
            if wants_env(proc):
                return proc(*args, env=env)
            else:
                return proc(*args)
        except TypeError as e:
            if callable(proc):
                # Callable, but wrong number of args or something
                raise NameError(e)
            raise NameError("Tried to call a non-callable Python object {} " +
                            "(its type is {})".format(x[0], type(proc)))
