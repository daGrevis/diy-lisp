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


def evaluate_flat(args, env):
    return [evaluate(arg, env) for arg
            in args]


def atom(ast, env):
    args = ast[1:]
    x = evaluate(args[0], env)

    return not is_list(x)


def eq(ast, env):
    args = ast[1:]
    x, y = evaluate_flat(args, env)

    if not is_atom(x):
        return False

    return x == y


def add(ast, env):
    args = ast[1:]
    x, y = evaluate_flat(args, env)

    if not is_integer(x) or not is_integer(y):
        raise LispError()

    return x + y


def sub(ast, env):
    args = ast[1:]
    x, y = evaluate_flat(args, env)

    if not is_integer(x) or not is_integer(y):
        raise LispError()

    return x - y


def mul(ast, env):
    args = ast[1:]
    x, y = evaluate_flat(args, env)

    if not is_integer(x) or not is_integer(y):
        raise LispError()

    return x * y


def div(ast, env):
    args = ast[1:]
    x, y = evaluate_flat(args, env)

    if not is_integer(x) or not is_integer(y):
        raise LispError()

    return x / y


def mod(ast, env):
    args = ast[1:]
    x, y = evaluate_flat(args, env)

    if not is_integer(x) or not is_integer(y):
        raise LispError()

    return x % y


def gt(ast, env):
    args = ast[1:]
    x, y = evaluate_flat(args, env)

    if not is_integer(x) or not is_integer(y):
        raise LispError()

    return x > y


def lt(ast, env):
    args = ast[1:]
    x, y = evaluate_flat(args, env)

    if not is_integer(x) or not is_integer(y):
        raise LispError()

    return x < y


def cons(ast, env):
    args = ast[1:]
    x, y = evaluate_flat(args, env)

    return [x] + y


def head(ast, env):
    args = ast[1:]
    x = evaluate(args[0], env)

    if not x:
        raise LispError()

    return x[0]


def tail(ast, env):
    args = ast[1:]
    x = evaluate(args[0], env)

    return x[1:]


def empty(ast, env):
    args = ast[1:]
    x = evaluate(args[0], env)

    return (not x)


def quote(ast, env):
    args = ast[1:]
    return args[0]


def if_expr(ast, env):
    args = ast[1:]
    x, y, z = args

    if evaluate(x, env):
        return evaluate(y, env)
    return evaluate(z, env)


def define(ast, env):
    args = ast[1:]

    if len(args) != 2:
        raise LispError("Wrong number of arguments")

    x = args[0]

    if not is_symbol(x):
        raise LispError("non-symbol")

    y = evaluate(args[1], env)

    env.set(x, y)


def lambda_expr(ast, env):
    args = ast[1:]

    if len(args) != 2:
        raise LispError("number of arguments")

    params = args[0]
    body = args[1]

    if not is_list(params):
        raise LispError()

    return Closure(env, params, body)


def closure(ast, env):
    closure = ast[0]
    args = evaluate_flat(ast[1:], env)

    len_of_closure_params = len(closure.params)
    len_of_args = len(args)

    if len_of_closure_params != len_of_args:
        message = ("wrong number of arguments, expected {} got {}"
                    .format(len_of_closure_params, len_of_args))
        raise LispError(message)

    variables = dict(zip(closure.params, args))
    env = (closure.env).extend(variables)

    return evaluate(closure.body, env)


builtin_functions = {
    "atom": atom,
    "eq": eq,
    "+": add,
    "-": sub,
    "*": mul,
    "/": div,
    "mod": mod,
    ">": gt,
    "<": lt,
    "cons": cons,
    "head": head,
    "tail": tail,
    "empty": empty,
    "quote": quote,
    "if": if_expr,
    "define": define,
    "lambda": lambda_expr,
    "closure": closure,
}


def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""

    if is_list(ast):
        operation = ast[0]
        args = ast[1:]

        if is_list(operation):
            closure = evaluate(operation, env)

            return evaluate([closure] + args, env)

        if operation in builtin_functions:
            return builtin_functions[operation](ast, env)

        if not is_symbol(operation):
            raise LispError("not a function")

        closure = env.variables[operation]

        return evaluate([closure] + args, env)

    if is_symbol(ast):
        return env.lookup(ast)

    return ast
