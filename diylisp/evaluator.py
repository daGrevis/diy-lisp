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


def atom(env, x):
    return not is_list(x)


def eq(env, x, y):
    if not is_atom(x):
        return False

    return x == y


def add(env, x, y):
    if not is_integer(x) or not is_integer(y):
        raise LispError()

    return x + y


def sub(env, x, y):
    if not is_integer(x) or not is_integer(y):
        raise LispError()

    return x - y


def mul(env, x, y):
    if not is_integer(x) or not is_integer(y):
        raise LispError()

    return x * y


def div(env, x, y):
    if not is_integer(x) or not is_integer(y):
        raise LispError()

    return x / y


def mod(env, x, y):
    if not is_integer(x) or not is_integer(y):
        raise LispError()

    return x % y


def gt(env, x, y):
    if not is_integer(x) or not is_integer(y):
        raise LispError()

    return x > y


def lt(env, x, y):
    if not is_integer(x) or not is_integer(y):
        raise LispError()

    return x < y


functions = {
    "atom": atom,
    "eq": eq,
    "+": add,
    "-": sub,
    "*": mul,
    "/": div,
    "mod": mod,
    ">": gt,
    "<": lt,
}


def quote_special(env, x):
    return x


def if_special(env, x, y, z):
    if evaluate(x, env):
        return evaluate(y, env)
    return evaluate(z, env)


def define_special(env, *args):
    if len(args) != 2:
        raise LispError("Wrong number of arguments")

    x = args[0]

    if not is_symbol(x):
        raise LispError("non-symbol")

    y = evaluate(args[1], env)

    env.set(x, y)


def lambda_special(env, *args):
    if len(args) != 2:
        raise LispError("number of arguments")

    params = args[0]
    body = args[1]

    if not is_list(params):
        raise LispError()

    return Closure(env, params, body)


# XXX: The difference between functions and specials is that specials accept unevaluated arguments.
specials = {
    "quote": quote_special,
    "if": if_special,
    "define": define_special,
    "lambda": lambda_special,
}


def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""

    if is_list(ast):
        operation = ast[0]
        args = ast[1:]

        if is_list(operation):

            if operation[0] == "lambda":
                closure = lambda_special(env, *operation[1:])

                return evaluate([closure] + args, env)

            closure = evaluate(operation, env)
            return evaluate([closure] + args, env)

        if operation in specials:
            return specials[operation](env, *args)

        if operation in functions:
            args = [evaluate(arg, env) for arg
                    in args]

            return functions[operation](env, *args)

        if is_closure(operation):
            closure = operation
            args = [evaluate(arg, env) for arg
                    in args]

            len_of_closure_params = len(closure.params)
            len_of_args = len(args)

            if len_of_closure_params != len_of_args:
                message = ("wrong number of arguments, expected {} got {}"
                           .format(len_of_closure_params, len_of_args))
                raise LispError(message)

            variables = dict(zip(closure.params, args))
            env = (closure.env).extend(variables)

            return evaluate(closure.body, env)

        if not is_symbol(operation):
            raise LispError("not a function")

        closure = env.variables[operation]
        return evaluate([closure] + args, env)

    if is_symbol(ast):
        return env.lookup(ast)

    return ast
