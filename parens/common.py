# common.py
# Python Lisp COMMON definitions

from collections import namedtuple

Symbol = str
List = list
Number = (int, float)
Env = dict
Expr = namedtuple("Expr", ["fn", "args"])
