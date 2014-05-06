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


def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""

    # Handle quote.
    if is_list(ast) and ast[0] == "quote":
        return evaluate(ast[1], env)

    # Handle atom.
    if is_list(ast) and ast[0] == "atom":
        ast = evaluate(ast[1], env)
        return not is_list(ast)

    # Handle eq.
    if is_list(ast) and ast[0] == "eq":
        x = evaluate(ast[1], env)
        y = evaluate(ast[2], env)
        if not is_atom(x):
            return False
        return x == y

    # Handle math.
    math_operations = ("+", "-", "*", "/", "mod", ">", "<")
    if is_list(ast) and ast[0] in math_operations:
        operation = ast[0]
        x = evaluate(ast[1], env)
        y = evaluate(ast[2], env)

        if not is_integer(x) or not is_integer(y):
            raise LispError()

        if operation == "+":
            return x + y
        if operation == "-":
            return x - y
        if operation == "*":
            return x * y
        if operation == "/":
            return x / y
        if operation == "mod":
            return x % y
        if operation == ">":
            return x > y
        if operation == "<":
            return x < y

    special_forms = ("if", )
    if is_list(ast) and ast[0] in special_forms:
        operation = ast[0]

        if operation == "if":
            x = evaluate(ast[1], env)
            if x:
                return evaluate(ast[2], env)
            else:
                return evaluate(ast[3], env)

    return ast
