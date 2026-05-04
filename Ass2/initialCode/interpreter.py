from __future__ import annotations

from dataclasses import dataclass

from ifp_ast import TBinOp, TBool, TIf, TInt, TLam, TString, TUnOp, TVar, Term
from printer import encode_string, to_base94
from parser import convertToBase94, decodeString

MAX_STEPS = 10_000_000


class InterpreterError(Exception):
    pass


class BetaReductionLimit(InterpreterError):
    pass


class ScopeError(InterpreterError):
    pass


class TypeError_(InterpreterError):
    pass


class ArithmeticError_(InterpreterError):
    pass


class UnknownUnOp(InterpreterError):
    def __init__(self, op: str):
        super().__init__(f"Unknown unary operator: {op}")
        self.op = op


class UnknownBinOp(InterpreterError):
    def __init__(self, op: str):
        super().__init__(f"Unknown binary operator: {op}")
        self.op = op


@dataclass
class VInt:
    value: int


@dataclass
class VBool:
    value: bool


@dataclass
class VString:
    value: str


@dataclass
class VClosure:
    var: int
    body: Term
    env: dict[int, "Thunk"]


Value = VInt | VBool | VString | VClosure


@dataclass
class Thunk:
    kind: str
    value: Value | None = None
    steps: int = 0
    term: Term | None = None
    env: dict[int, "Thunk"] | None = None


def _to_term(v: Value) -> Term:
    if isinstance(v, VInt):
        return TInt(v.value)
    if isinstance(v, VBool):
        return TBool(v.value)
    if isinstance(v, VString):
        return TString(v.value)
    if isinstance(v, VClosure):
        return TLam(v.var, v.body)
    raise TypeError(f"Unknown value type: {type(v).__name__}")


def interpret(check_max: bool, term: Term) -> tuple[Term, int]:
    steps = 0
    
    def eval_term(t: Term, env: dict[int, Thunk]) -> Value:
        # TODO
        nonlocal steps

        if isinstance(t, TInt):
            return VInt(t.value)
        elif isinstance(t, TBool):
            return VBool(t.value)
        elif isinstance(t, TString):
            return VString(t.value)
        elif isinstance(t, TVar):
            if t.value not in env:
                raise ScopeError()
            thunk = env[t.value]
            return eval_term(thunk.term, thunk.env)
        elif isinstance(t, TLam):
            return VClosure(t.var, t.body, env.copy())
        elif isinstance(t, TUnOp):
            val = eval_term(t.term, env)
            if t.op == '-':
                if not isinstance(val, VInt):
                    raise TypeError_()
                return VInt(-val.value)
            elif t.op == '!':
                if not isinstance(val, VBool):
                    raise TypeError_()
                return VBool(not val.value)
            elif t.op == '#':
                if not isinstance(val, VString):
                    raise TypeError_()
                return VInt(convertToBase94(encode_string(val.value)))
            elif t.op == '$':
                if not isinstance(val, VInt):
                    raise TypeError_()
                return VString(decodeString(to_base94(val.value)))
            else:
                raise UnknownUnOp(t.op)
        elif isinstance(t, TIf):
            cond_val = eval_term(t.cond, env)
            if not isinstance(cond_val, VBool):
                raise TypeError_()
            
            if cond_val.value == True:
                return eval_term(t.true_branch, env)
            else:
                return eval_term(t.false_branch, env)
        elif isinstance(t, TBinOp):
            if t.op == '$':
                func_val = eval_term(t.left, env)
                if not isinstance(func_val, VClosure):
                    raise TypeError_()
                arg_thunk = Thunk(kind="thunk", term=t.right, env=env.copy())

                steps += 1
                if (check_max == True and steps > MAX_STEPS):
                    raise BetaReductionLimit()
                
                new_env = func_val.env.copy()
                new_env[func_val.var] = arg_thunk
                return eval_term(func_val.body, new_env)
            else:
                left_val = eval_term(t.left, env)
                right_val = eval_term(t.right, env)
                if t.op in ['+', '-', '*', '/', '%', '<', '>']:
                    if not isinstance(left_val, VInt) or not isinstance(right_val, VInt):
                        raise TypeError_()
                    l = left_val.value
                    r = right_val.value
                    if t.op == '+':
                        return VInt(l + r)
                    elif t.op == '-':
                        return VInt(l - r)  
                    elif t.op == '*':
                        return VInt(l * r)
                    elif t.op == '/':
                        if r == 0:
                            raise ArithmeticError_()
                        return VInt(int(l / r))
                    elif t.op == '%':
                        if r == 0:
                            raise ArithmeticError_()
                        q = int(l / r)
                        r = l - (q * r)
                        return VInt(r)
                    elif t.op == '<':
                        return VBool(l < r)
                    elif t.op == '>':
                        return VBool(l > r)
                elif t.op == '=':
                    if type(left_val) != type(right_val):
                        raise TypeError_()
                    return VBool(left_val.value == right_val.value)
                elif t.op in ['|', '&']:
                    if not isinstance(left_val, VBool) or not isinstance(right_val, VBool):
                        raise TypeError_()
                    l = left_val.value
                    r = right_val.value
                    if t.op == '|':
                        return VBool(l or r)
                    elif t.op == '&':
                        return VBool(l and r)
                elif t.op == '.':
                    if not isinstance(left_val, VString) or not isinstance(right_val, VString):
                        raise TypeError_()
                    return VString(left_val.value + right_val.value)
                elif t.op in ['T', 'D']:
                    if not isinstance(left_val, VInt) or not isinstance(right_val, VString):
                        raise TypeError_()
                    x = left_val.value
                    s = right_val.value
                    if t.op == 'T':
                        return VString(s[:x])
                    elif t.op == 'D':
                        return VString(s[x:])
                else:
                    raise UnknownBinOp(t.op)
        else:
            raise TypeError(f"Unknown term type: {type(t).__name__}")

    result = eval_term(term, {})
    return _to_term(result), steps

