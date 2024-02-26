from typing import *
import sys

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

    assert is_lisp_str(arg), "`println` expects a string"
    print("".join(map(str, arg)))
    return []

def load(args: list[SExpr]) -> SExpr:
    assert len(args) == 1, "`load` expects exactly 1 arg"
    arg = args[0]

    assert is_lisp_str(arg), "`load` expects a string"
    file_path = "".join(map(str, arg))

    with open(file_path, "r") as f:
        code = f.read()
    # HACK: we need the functions from `main.py` so we use
    # sys.modules to get them
    sexpr = sys.modules["__main__"].parse(code)
    ret = sys.modules["__main__"].run_sexpr(sexpr)

    return ret

def module(stuff: list[SExpr]) -> SExpr:
    assert len(stuff) >= 1, "missing module name"
    name = stuff[0]
    assert isinstance(name, str), "module name must be a symbol"

    return ["module", name]

def eq(args: list[SExpr]) -> str:
    assert len(args) == 2, "`=` expects exactly 2 args"
    arg1, arg2 = args[0], args[1]
    return str(arg1 == arg2).lower()

def lt(args: list[SExpr]) -> str:
    assert len(args) == 2, "`<` expects exactly 2 args"
    assert isinstance(args[0], str), "`<` does not expect list arguments"
    assert isinstance(args[1], str), "`<` does not expect list arguments"
    arg1, arg2 = int(args[0]), int(args[1])
    return str(arg1 < arg2).lower()

def gt(args: list[SExpr]) -> str:
    assert len(args) == 2, "`>` expects exactly 2 args"
    assert isinstance(args[0], str), "`>` does not expect list arguments"
    assert isinstance(args[1], str), "`>` does not expect list arguments"
    arg1, arg2 = int(args[0]), int(args[1])
    return str(arg1 > arg2).lower()

Builtin: TypeAlias = Callable[[list[SExpr]], SExpr]
BUILTINS: dict[str, Builtin] = {
    "+": plus,
    "-": minus,
    "*": mul,
    "/": div,
    "quote": quote,
    "quit": quit_,
    "println": println,
    "load": load,
    "module": module,
    "=": eq,
    "<": lt,
    ">": gt,
}

def iff(args: list[SExpr]) -> SExpr:
    match args:
        case [cond, then, elze]:
            # HACK: we need the functions from `main.py` so we use
            # sys.modules to get them
            res = sys.modules["__main__"].run_sexpr(cond)
            if res == "true":
                return then
            elif res == "false":
                return elze
            else:
                assert False, "the condition of the `if` macro must return `true` or `false`"
        case _:
            assert False, "`if` macro takes exactly 3 args"

BUILTIN_MACROS: dict[str, Builtin] = {
    "if": iff,
}

def is_lisp_str(sexpr: SExpr) -> bool:
    if not isinstance(sexpr, list): return False
    for ch in sexpr:
        if not isinstance(ch, str): return False
        if len(ch) != 1: return False
    return True