from enum import Enum
from typing import Dict, List, Optional

class Type(Enum):
    NUMBER = 0
    PLUS = 1
    MINUS = 2
    MULTIPLY = 3
    DIVIDE = 4
    EXPONENT = 5
    OPEN_PAR = 6
    CLOSE_PAR = 7
    FUNCTION = 8

class Prec(Enum):
    MIN = 0
    TERM = 1    # +, -
    FACTOR = 2  # *, /
    POWER = 3   # ^
    FUNC = 4    # sin, cos, mod, log, ...
    PARS = 5    # (, ) - should be the maximum precedence

ONE_CHARACTER_TYPES: Dict[str, Type] = {'+' : Type.PLUS, '-' : Type.MINUS, '*' : Type.MULTIPLY, '/' : Type.DIVIDE,
                                        '^' : Type.EXPONENT, '(' : Type.OPEN_PAR, ')' : Type.CLOSE_PAR}

PRECEDENCE: Dict[int, int] = {Type.NUMBER : Prec.MIN,
                              Type.PLUS : Prec.TERM,
                              Type.MINUS : Prec.TERM,
                              Type.MULTIPLY : Prec.FACTOR,
                              Type.DIVIDE : Prec.FACTOR,
                              Type.EXPONENT : Prec.POWER,
                              Type.OPEN_PAR : Prec.PARS,
                              Type.CLOSE_PAR : Prec.MIN,
                              Type.FUNCTION : Prec.FUNC}

class Token():
    def __init__(self, value: str, type: Type) -> None:
        self.type = type
        self.value = value

def tokenize_expr(expression: str) -> Optional[List[Token]]:
    tokens: List[Token] = []

    token_type: Optional[Type] = None
    token_begin = 0
    i = 0

    while i < len(expression):
        char = expression[i]

        if token_type is None:
            if char == ' ':
                i += 1
                continue

            if char.isdigit():
                token_type = Type.NUMBER
                token_begin = i
                decimal_point = False
                i += 1
                continue

            if char in ONE_CHARACTER_TYPES:
                new_token = Token(char, ONE_CHARACTER_TYPES[char])
                tokens.append(new_token)
                i += 1
                continue

            token_type = Type.FUNCTION
            token_begin = i
            i += 1
            continue

        if token_type == Type.NUMBER:
            if char.isdigit() or (char == ',' and not decimal_point):
                decimal_point = decimal_point or char == ','
                i += 1
                continue

            if (char in ONE_CHARACTER_TYPES or char == ' ') and not expression[i - 1] == ',':
                new_token = Token(expression[token_begin : i], Type.NUMBER)
                tokens.append(new_token)
                token_type = None
                continue

            return None

        if char == ' ' or char == '(':
            new_token = Token(expression[token_begin : i])
            tokens.append(new_token)
            token_type = None
            continue
        i += 1

    if token_type == Type.NUMBER


def evaluation(expression: str) -> str:
    pass
