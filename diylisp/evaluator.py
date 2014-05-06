# -*- coding: utf-8 -*-

from types import Environment, LispError, Closure
from ast import is_boolean, is_atom, is_symbol, is_list, is_closure, is_integer
from asserts import assert_exp_length, assert_valid_definition, assert_boolean
from parser import unparse

"""
This is the Evaluator module. The `evaluate` function below is the heart
of your language, and the focus for most of parts 2 through 6.

A score of useful functions is provided for you, as per the above imports,
making your work a bit easier. (We're supposed to get through this thing
in a day, after all.)
"""


def add(x, y):
    if not is_integer(x) or not is_integer(y):
        raise LispError()

    return x + y


def sub(x, y):
    if not is_integer(x) or not is_integer(y):
        raise LispError()

    return x - y


def mul(x, y):
    if not is_integer(x) or not is_integer(y):
        raise LispError()

    return x * y


def div(x, y):
    if not is_integer(x) or not is_integer(y):
        raise LispError()

    return x / y


def mod(x, y):
    if not is_integer(x) or not is_integer(y):
        raise LispError()

    return x % y


def gt(x, y):
    if not is_integer(x) or not is_integer(y):
        raise LispError()

    return x > y


def lt(x, y):
    if not is_integer(x) or not is_integer(y):
        raise LispError()

    return x < y


functions = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": div,
    "mod": mod,
    ">": gt,
    "<": lt,
}


def quote_special(x):
    return evaluate_wo_env(x)


def atom_special(x):
    x = evaluate_wo_env(x)
    return not is_list(x)


def eq_special(x, y):
    x = evaluate_wo_env(x)
    y = evaluate_wo_env(y)

    if not is_atom(x):
        return False

    return x == y


def if_special(x, y, z):
    if evaluate_wo_env(x):
        return evaluate_wo_env(y)
    return evaluate_wo_env(z)


specials = {
    "quote": quote_special,
    "atom": atom_special,
    "eq": eq_special,
    "if": if_special,
}


def evaluate_wo_env(ast):

    if is_list(ast):
        operation = ast[0]
        args = ast[1:]

        if operation in specials:
            return specials[operation](*args)

        if operation in functions:
            args = map(evaluate_wo_env, args)

            return functions[operation](*args)

    return ast


def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""

    return evaluate_wo_env(ast)
