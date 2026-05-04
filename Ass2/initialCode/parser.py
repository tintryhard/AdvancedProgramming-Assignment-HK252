from __future__ import annotations

from dataclasses import dataclass

from ifp_ast import (
    CHARS,
    CHARS_DECODED,
    TBinOp,
    TBool,
    TIf,
    TInt,
    TLam,
    TString,
    TUnOp,
    TVar,
    Term,
)


@dataclass(frozen=True)
class ParseError(Exception):
    kind: str
    index: int | None = None
    ch: str | None = None

    def __str__(self) -> str:
        if self.kind == "UnexpectedChar":
            return f"UnexpectedChar({self.ch!r}, {self.index})"
        if self.kind == "UnusedInput":
            return f"UnusedInput({self.index})"
        return "UnexpectedEOF"


def convertToBase94(chars: str) -> int:
    value = 0
    for char in chars:
        value = value * 94 + (ord(char) - 33)
    return value

def decodeString(chars: str) -> str:
    return "".join(CHARS_DECODED[ord(char)-33] for char in chars)

def p_term(inp: str) -> Term:
    # TODO
    tokens = inp.split()
    index = 0

    def parse_node() -> Term:
        nonlocal index
        if index > len(tokens) - 1:
            raise ParseError(kind="UnexpectedEOF")
        token = tokens[index]
        index += 1
        indicator = token[0]
        body = token[1:]
        if indicator == 'T':
            if body != "":
                raise ParseError(kind="UnexpectedChar", index=index, ch=body[0])
            return TBool(True)
        elif indicator == 'F':
            if body != "":
                raise ParseError(kind="UnexpectedChar", index=index, ch=body[0])
            return TBool(False)
        elif indicator == 'I':
            if body == "":
                raise ParseError(kind="UnexpectedChar", index=index)
            return TInt(convertToBase94(body))
        elif indicator == 'S':
            return TString(decodeString(body))
        elif indicator == 'U':
            if len(body) != 1:
                raise ParseError(kind="UnexpectedChar", index=index, ch=body[0])
            return TUnOp(body, parse_node())
        elif indicator == 'B':
            if len(body) != 1:
                raise ParseError(kind="UnexpectedChar", index=index, ch=body[0])
            return TBinOp(parse_node(), body, parse_node())
        elif indicator == '?':
            return TIf(parse_node(), parse_node(), parse_node())
        elif indicator =='L':
            return TLam(convertToBase94(body), parse_node())
        elif indicator == 'v':
            return TVar(convertToBase94(body))
        else:
            raise ParseError(kind="UnexpectedChar", index=index, ch=indicator)
    
    root = parse_node()
    if (index < len(tokens)):
        raise ParseError(kind="UnusedInput", index=index)
    return root
