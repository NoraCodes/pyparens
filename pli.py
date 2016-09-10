#!/usr/bin/env python3
# pli.py
# A command interpreter frontend for PyParens, the Python Lisp

from parens import plexec, parse, lex
from cmd import Cmd

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
