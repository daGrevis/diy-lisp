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


def is_atom(ast):
    return not is_list(ast)


def add(x, y):
    return x + y


def sub(x, y):
    return x - y


def mul(x, y):
    return x * y


def div(x, y):
    return x / y


def mod(x, y):
    return x % y


def gt(x, y):
    return x > y


def lt(x, y):
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


def if_special(x, y, z):
    if evaluate_wo_env(x):
        return evaluate_wo_env(y)
    return evaluate_wo_env(z)


specials = {
    "if": if_special,
}


def evaluate_wo_env(ast):

    # Handle quote.
    if is_list(ast) and ast[0] == "quote":
        return evaluate_wo_env(ast[1])

    # Handle atom.
    if is_list(ast) and ast[0] == "atom":
        ast = evaluate_wo_env(ast[1])
        return not is_list(ast)

    # Handle eq.
    if is_list(ast) and ast[0] == "eq":
        x = evaluate_wo_env(ast[1])
        y = evaluate_wo_env(ast[2])
        if not is_atom(x):
            return False
        return x == y

    # Handle functions.
    if is_list(ast) and ast[0] in functions:
        operation = ast[0]
        x = evaluate_wo_env(ast[1])
        y = evaluate_wo_env(ast[2])

        if not is_integer(x) or not is_integer(y):
            raise LispError()

        return functions[operation](x, y)

    # Handle specials.
    if is_list(ast) and ast[0] in specials:
        operation = ast[0]
        args = ast[1:]

        return specials[operation](*args)

    return ast


def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""

    return evaluate_wo_env(ast)
