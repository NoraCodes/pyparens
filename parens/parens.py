#!/usr/bin/env python3

# A Python Lispish called Parens
from .lex import lex
from .parse import parse
from .eval import eval


def plexec(line):
    """
    Brings together the lexer, parser, and evaluator,
    and does some error handling
    """
    return_value = False
    try:
        return_value = eval(parse(lex(line)))
    except SyntaxError as e:
        print(e)
    except NameError as e:
        print(e)
    except AttributeError as e:
        print(e)
    except KeyboardInterrupt:
        print("Aborted with keyboard.")
    except SystemExit:
        print("Aborted with system exit.")

    if return_value:
        print("R: {}".format(return_value))
    else:
        print("NR~")

    return return_value
