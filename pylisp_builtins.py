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

def ret(args: list[SExpr]) -> SExpr:
    assert len(args) == 1, "`return` expects exactly 1 arg"
    return ["magic: return", args[0]]

def head(args: list[SExpr]) -> SExpr:
    assert isinstance(args[0], list), "`head` expects only list arguments"
    return args[0][0]

def tail(args: list[SExpr]) -> SExpr:
    assert isinstance(args[0], list), "`tail` expects only list arguments"
    return args[0][1:]

def is_empty(args: list[SExpr]) -> SExpr:
    assert isinstance(args[0], list), "`is-empty` expects only list arguments"
    return str(len(args[0]) == 0).lower()

def range_(args: list[SExpr]) -> SExpr:
    assert len(args) == 2, "`range` expects exactly 2 args"
    assert isinstance(args[0], str), "`range` does not expect list arguments"
    assert isinstance(args[1], str), "`range` does not expect list arguments"
    start, stop = int(args[0]), int(args[1])
    return list(map(str, range(start, stop)))

Builtin: TypeAlias = Callable[[list[SExpr]], SExpr]
BUILTINS: dict[str, Builtin] = {
    "+": plus,
    "-": minus,
    "*": mul,
    "/": div,
    "'": quote,
    "quit": quit_,
    "println": println,
    "load": load,
    "module": module,
    "=": eq,
    "<": lt,
    ">": gt,
    "return": ret,
    "head": head,
    "tail": tail,
    "is-empty": is_empty,
    "range": range_,
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

def foreach(args: list[SExpr]) -> SExpr:
    match args:
        case [elts, sym, body]:
            # HACK: we need the functions from `main.py` so we use
            # sys.modules to get them
            lst = sys.modules["__main__"].run_sexpr(elts)
            assert isinstance(lst, list), "the first argument of the `foreach` macro must be a list"
            assert isinstance(sym, str), "the second argument of the `foreach` macro must be a symbol"
            outs: list[SExpr] = ["'"]
            for elt in lst:
                outs.append(bind(sym, elt, body))
            return outs
        case _:
            assert False, "the `foreach` macro takes exactly 3 args"

def block(args: list[SExpr]) -> SExpr:
    for arg in args:
        res = sys.modules["__main__"].run_sexpr(arg)
        if len(res) == 2 and res[0] == "magic: return":
            return (["'"] if isinstance(res[1], list) else "") + res[1]
    return []

Function: TypeAlias = tuple[list[str], SExpr]
FUNCTIONS: dict[str, Function] = {}

def fun(args: list[SExpr]) -> SExpr:
    match args:
        case [str(name), [*args], [*body]]:
            for arg in args:
                assert isinstance(arg, str), "function parameters must be symbols"
            params = list(map(str, args))

            FUNCTIONS[name] = params, body
            return []
        case _:
            assert False, "invalid `fun` definition"

def literal(sexpr: SExpr) -> SExpr:
    return sexpr if isinstance(sexpr, str) else (["'"] + sexpr) # type: ignore

def reduce(args: list[SExpr]) -> SExpr:
    match args:
        case [elts, [str(iter_name), str(acc_name)], body, first_acc]:
            # HACK: we need the functions from `main.py` so we use
            # sys.modules to get them
            lst = sys.modules["__main__"].run_sexpr(elts)
            assert isinstance(lst, list), "the first argument of the `reduce` macro must be a list"
            acc = sys.modules["__main__"].run_sexpr(first_acc)
            for elt in lst:
                acc = sys.modules["__main__"].run_sexpr(
                    bind(iter_name, elt,
                         bind(acc_name, literal(acc), body)))
            return literal(acc)
        case _:
            assert False, "the `reduce` macro takes exactly 4 args and the second one must be a 2-symbol list"

BUILTIN_MACROS: dict[str, Builtin] = {
    "if": iff,
    "foreach": foreach,
    "block": block,
    "fun": fun,
    "reduce": reduce,
}

def is_lisp_str(sexpr: SExpr) -> bool:
    if not isinstance(sexpr, list): return False
    for ch in sexpr:
        if not isinstance(ch, str): return False
        if len(ch) != 1: return False
    return True

def bind(sym: str, expr: SExpr, block: SExpr) -> SExpr:
    if block == sym:
        return expr
    elif isinstance(block, str):
        return block
    else:
        new_sexpr: list[SExpr] = []
        for child in block:
            new_sexpr.append(bind(sym, expr, child))
        return new_sexpr
