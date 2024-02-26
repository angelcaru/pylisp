#!/usr/bin/env python3
from typing import *

from pylisp_builtins import BUILTINS, BUILTIN_MACROS, FUNCTIONS, bind

Predicate = Callable[[str], bool]
def find_by_pred(s: str, i: int, p: Predicate) -> int:
    while i < len(s) and not p(s[i]):
        i += 1
    return i

SExpr: TypeAlias = "str | list[SExpr]"

def parse(code: str) -> SExpr:
    def parse_impl(code: str, *, start: int = 0) -> tuple[SExpr, int]:
        if start + 1 < len(code) and code[start:start+2] == "//":
            start = find_by_pred(code, start, lambda x: x == "\n") + 1
        
        if start >= len(code): return [], start
        if code[start] != "(" and code[start] != '"':
            word_end = find_by_pred(code, start, lambda x: x.isspace() or x == ")")
            return code[start:word_end], word_end
        elif code[start] == '"':
            str_end = find_by_pred(code, start + 1, lambda x: x == '"')
            quote: list[SExpr] = ["'"]
            return quote + list(code[start+1:str_end]), str_end + 1
        
        sexpr: list[SExpr] = []
        i = start + 1
        while i < len(code) and code[i] != ")":
            inner, i = parse_impl(code, start=i)
            sexpr.append(inner)

            i = find_by_pred(code, i, lambda s: not s.isspace())
        return sexpr, i + 1
    
    sexpr, i = parse_impl(code, start=0)
    if i < len(code):
        assert False, f"Extra characters at end of line: {code[i:]}"
    return sexpr

def run_sexpr(sexpr: SExpr) -> SExpr:
    if isinstance(sexpr, str): return sexpr

    # assert isinstance(sexpr, list)
    if len(sexpr) == 0: return []
    fun_name, *raw_args = sexpr
    
    if fun_name in BUILTIN_MACROS:
        assert isinstance(fun_name, str)
        processed_sexpr = BUILTIN_MACROS[fun_name](raw_args)
        return run_sexpr(processed_sexpr)

    args = []
    for arg in raw_args:
        args.append(run_sexpr(arg))
    
    assert isinstance(fun_name, str)

    if fun_name in BUILTINS:
        return BUILTINS[fun_name](args)
    elif fun_name in FUNCTIONS:
        params, body = FUNCTIONS[fun_name]
        bound_body = body
        for param, arg in zip(params, args):
            if isinstance(arg, list):
                arg = ["'"] + arg # type: ignore
            bound_body = bind(param, arg, bound_body)
        return run_sexpr(bound_body)
    else:
        assert False, f"unknown function or macro: {fun_name} {render_as_sexpr(sexpr)}"

def render_as_sexpr(sexpr: SExpr) -> str:
    if isinstance(sexpr, str): return sexpr
    
    elts: list[str] = []
    for x in sexpr:
        elts.append(render_as_sexpr(x))
    return f"({' '.join(elts)})"


def repl():
    code = input("> ")
    sexpr = parse(code)
    res = run_sexpr(sexpr)
    print(" => {}".format(render_as_sexpr(res)))


def report_err(e):
    for i, arg in enumerate(e.args):
        if i == 0:
            print(f"ERROR: {arg}")
        else:
            print(f"  {arg}")

while __name__ == "__main__":
    try:
        repl()
    except Exception as error:
        if isinstance(error, EOFError):
            quit()
        else:
            report_err(error)