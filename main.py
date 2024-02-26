#!/usr/bin/env python3
from typing import *

from pylisp_builtins import BUILTINS

Predicate = Callable[[str], bool]
def find_by_pred(s: str, i: int, p: Predicate) -> int:
    while i < len(s) and not p(s[i]):
        i += 1
    return i

SExpr: TypeAlias = "str | list[SExpr]"

def parse(code: str) -> SExpr:
    def parse_impl(code: str, *, start: int = 0) -> tuple[SExpr, int]:
        if code[start] != "(":
            word_end = find_by_pred(code, start, lambda x: x.isspace() or x == ")")
            return code[start:word_end], word_end
        
        sexpr: list[SExpr] = []
        i = start + 1
        while i < len(code) and code[i] != ")":
            inner, i = parse_impl(code, start=i)
            sexpr.append(inner)

            i = find_by_pred(code, i, lambda s: not s.isspace())
        return sexpr, i + 1
    
    sexpr, i = parse_impl(code, start=0)
    if i < len(code):
        assert False, f"TODO: report errors: {i} < {len(code)}"
    return sexpr

def run_sexpr(sexpr: SExpr) -> SExpr:
    if isinstance(sexpr, str): return sexpr

    # assert isinstance(sexpr, list)
    if len(sexpr) == 0: return []
    fun_name, *raw_args = sexpr
    
    args = []
    for arg in raw_args:
        args.append(run_sexpr(arg))
    
    assert isinstance(fun_name, str)
    return BUILTINS[fun_name](args)

def render_as_sexpr(sexpr: SExpr) -> str:
    if isinstance(sexpr, str): return sexpr
    
    elts: list[str] = []
    for x in sexpr:
        elts.append(render_as_sexpr(x))
    return f"({" ".join(elts)})"


def repl():
    code = input("> ")
    sexpr = parse(code)
    res = run_sexpr(sexpr)
    print(" => {}".format(render_as_sexpr(res)))

while __name__ == "__main__":
    repl()