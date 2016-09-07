#!/usr/bin/env python3

# A Python Lispish called Parens

from collections import namedtuple
from cmd import Cmd
from string import whitespace
import math  # For the standard environment
import operator as op
import importlib  # To allow importing

import plistd

Expr = namedtuple("Expr", ["fn", "args"])

Symbol = str
List = list
Number = (int, float)
Env = dict


def standard_env():
    """
    An environment with some useful stuff
    """
    env = Env()
    env.update(vars(math))
    env.update({
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv,
        '%': op.mod, '^': op.pow,
        '=': op.eq, 'eq': op.eq,
        'print': print,
        'list': plistd.makelist
        })
    return env

global_env = standard_env()


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
    except KeyboardInterrupt:
        print("Aborted with keyboard.")
    except SystemExit:
        print("Aborted with system exit.")

    if return_value:
        print("R: {}".format(return_value))
    else:
        print("NR~")


class LispCmd(Cmd):
    """
    The command line for PyParens
    """
    intro = "Welcome to PyParens, a Python Lisp-ish"
    prompt = "pl> "
    file = None

    # We actually don't mostly use commands, so everything is
    #   handled by default()
    def default(self, line):
        plexec(line)

    # ... except EOF, which allows pressing ctrl + D to exit
    def do_EOF(self, line):
        """
        Exit the interpreter (press Ctrl+D)
        """
        print("")
        exit(0)

    # ... and _EXEC which is an alias for the default, for the help menu
    def do__EXEC(self, arg):
        """
        Executes some PyLisp. This is the default, so simply:

        pl> (+ 1 2)

        will execute that line of code.
        """

    # ... and _LOAD which loads and evals a file.
    def do__LOAD(self, arg):
        """
        Load and execute a script from a file.
        """
        try:
            with open(arg) as f:
                text = f.read()
        except FileNotFoundError as e:
            print("_LOAD FAIL: {}".format(e))
            return
        plexec(text)

    # ... and _LEX which just lexes a line.
    def do__LEX(self, arg):
        """
        Just lex a string, resulting in a list of tokens
        """
        print(lex(arg))

    # ... and _PARSE which lexes and parses a line
    def do__PARSE(self, arg):
        """
        Lex and parse an input string, resulting in a bunch of Python lists.
        """
        print(parse(lex(arg)))


def repl():
    commandLine = LispCmd()
    commandLine.cmdloop()

if __name__ == "__main__":
    repl()
