from typing import *

SExpr: TypeAlias = "str | list[SExpr]"

def todo(*args: object, **kwargs: dict) -> Never:
    assert False, "not implemented"

def plus(args: list[SExpr]) -> str:
    # TODO: proper error handling
    sum_ = 0
    for arg in args:
        assert isinstance(arg, str), "`+` does not expect list arguments"
        sum_ += int(arg)
    return str(sum_)

def mul(args: list[SExpr]) -> str:
    # TODO: proper error handling
    prod = 1
    for arg in args:
        assert isinstance(arg, str), "`*` does not expect list arguments"
        prod *= int(arg)
    return str(prod)

def minus(args: list[SExpr]) -> str:
    assert len(args) == 2, "`-` expects exactly 2 args"
    assert isinstance(args[0], str), "`-` does not expect list arguments"
    assert isinstance(args[1], str), "`-` does not expect list arguments"
    arg1, arg2 = int(args[0]), int(args[1])
    return str(arg1 - arg2)

def div(args: list[SExpr]) -> str:
    assert len(args) == 2, "`/` expects exactly 2 args"
    assert isinstance(args[0], str), "`/` does not expect list arguments"
    assert isinstance(args[1], str), "`/` does not expect list arguments"
    arg1, arg2 = int(args[0]), int(args[1])
    return str(arg1 // arg2)

def quote(args: list[SExpr]) -> SExpr:
    return args

def quit_(_: list[SExpr]) -> Never:
    quit()

def println(args: list[SExpr]) -> SExpr:
    assert len(args) == 1, "`println` expects exactly 1 arg"
    arg = args[0]
    assert isinstance(arg, list), "`println` expects a string"
    for ch in arg:
        assert isinstance(ch, str) and len(ch) == 1, "`println` expects a string"
    
    print("".join(map(str, arg)))
    return []

Builtin: TypeAlias = Callable[[list[SExpr]], SExpr]
BUILTINS: dict[str, Builtin] = {
    "+": plus,
    "-": minus,
    "*": mul,
    "/": div,
    "quote": quote,
    "quit": quit_,
    "println": println,
}