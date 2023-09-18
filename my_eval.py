from enum import Enum
from typing import Dict, List, Optional, Set, Tuple
from math import sin, cos, tan, asin, acos, atan, log, pow, pi, e

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

INFIX_FUNCTIONS: Set[str] = {"mod", "log_base", "yth_root"}

PRECEDENCE: Dict[int, int] = {Type.NUMBER : Prec.MIN,
                              Type.PLUS : Prec.TERM,
                              Type.MINUS : Prec.TERM,
                              Type.MULTIPLY : Prec.FACTOR,
                              Type.DIVIDE : Prec.FACTOR,
                              Type.EXPONENT : Prec.POWER,
                              Type.OPEN_PAR : Prec.PARS,
                              Type.CLOSE_PAR : Prec.MIN,
                              Type.FUNCTION : Prec.FUNC}

ALL_FUNCTIONS = {"sin", "cos", "tan", "arcsin", "arccos", "arctan", "mod", "sroot", "yth_root", "ln", "log_base", "abs"}

class Token():
    def __init__(self, value: str, type: Type) -> None:
        self.type = type
        self.value = value


def tokenize_expr(expression: str) -> Optional[List[Token]]:
    """
    Makes list of tokens that represents given expression.
    Also checks if the tokens are correct numbers, functions, operators or constants (like pi and e).
    
    Returns the list if no error was found or returns None otherwise.
    """
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

            if char == ',':
                return None

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

        value = expression[token_begin : i]

        if (value == 'pi' or value == 'e'):
            if char == '(':
                return None

            if char in ONE_CHARACTER_TYPES or char == ' ':
                new_token = Token(value, Type.FUNCTION)
                tokens.append(new_token)
                token_type = None
                continue

        if char == ' ' or char == '(':
            if value not in ALL_FUNCTIONS:
                return None

            new_token = Token(value, Type.FUNCTION)
            tokens.append(new_token)
            token_type = None
            continue

        if char.isdigit() or char in ONE_CHARACTER_TYPES or char == ',':
            return None
        i += 1

    value = expression[token_begin : i]

    if token_type == Type.NUMBER:
        if expression[i - 1].isdigit():
            new_token = Token(value, Type.NUMBER)
            tokens.append(new_token)
            return tokens

        return None

    if token_type == Type.FUNCTION:
        if value != 'pi' and value != 'e' and value not in ALL_FUNCTIONS:
            return None

        new_token = Token(value, Type.FUNCTION)
        tokens.append(new_token)

    return tokens

def correct_number_neighbors(tokens: List[Token], i: int) -> bool:
    return (i - 1 < 0 or (tokens[i - 1].value != 'pi' and tokens[i - 1].value != 'e'
                          and tokens[i - 1].type != Type.NUMBER and tokens[i - 1].type != Type.CLOSE_PAR)) and \
           (i + 1 >= len(tokens) or (tokens[i + 1].value != 'pi' and tokens[i + 1].value != 'e'
                          and tokens[i + 1].type != Type.NUMBER and tokens[i + 1].type != Type.OPEN_PAR))

def correct_infix_neighbors(tokens: List[Token], i: int) -> bool:
    return (i - 1 >= 0 and (tokens[i - 1].value == 'pi' or tokens[i - 1].value == 'e'
                          or tokens[i - 1].type == Type.NUMBER or tokens[i - 1].type == Type.CLOSE_PAR)) and \
           (i + 1 < len(tokens) and (tokens[i + 1].type == Type.FUNCTION and tokens[i + 1].value not in INFIX_FUNCTIONS
                          or tokens[i + 1].type == Type.NUMBER or tokens[i + 1].type == Type.OPEN_PAR))

def correct_minus(tokens: List[Token], i: int) -> bool:
    return (i - 1 < 0 or (tokens[i - 1].value == 'pi' or tokens[i - 1].value == 'e' or tokens[i - 1].type == Type.OPEN_PAR
                          or tokens[i - 1].type == Type.NUMBER or tokens[i - 1].type == Type.CLOSE_PAR)) and \
           (i + 1 < len(tokens) and (tokens[i + 1].type == Type.FUNCTION and tokens[i + 1].value not in INFIX_FUNCTIONS
                          or tokens[i + 1].type == Type.NUMBER or tokens[i + 1].type == Type.OPEN_PAR))

def correct_function_neighbors(tokens: List[Token], i: int) -> bool:
    return (i - 1 < 0 or (tokens[i - 1].value != 'pi' and tokens[i - 1].value != 'e'
                          and tokens[i - 1].type != Type.NUMBER and tokens[i - 1].type != Type.CLOSE_PAR)) and \
           (i + 1 < len(tokens) and (tokens[i + 1].type == Type.FUNCTION and tokens[i + 1].value not in INFIX_FUNCTIONS
                          or tokens[i + 1].type == Type.NUMBER or tokens[i + 1].type == Type.OPEN_PAR))

def correct_tokenized_expression(tokens: List[Token]) -> bool:
    """
    Returns true if tokenized expression, created in tokenize_expr function, is a valid expression\n
    (but does not check division by zero and things like this - this will be checked while calculating)
    """
    open_brackets = 0

    for i in range(len(tokens)):
        value = tokens[i].value
        token_type = tokens[i].type

        if token_type == Type.OPEN_PAR:
            open_brackets += 1
            continue

        if token_type == Type.CLOSE_PAR:
            if open_brackets == 0 or tokens[i - 1].type == Type.OPEN_PAR:
                return False

            open_brackets -= 1
            continue

        if token_type == Type.MINUS:
            if not correct_minus(tokens, i):
                return False
            continue

        if token_type == Type.NUMBER or value == 'pi' or value == 'e':
            if not correct_number_neighbors(tokens, i):
                return False
            continue

        if value in ONE_CHARACTER_TYPES or value in INFIX_FUNCTIONS:
            if not correct_infix_neighbors(tokens, i):
                return False
            continue

        if not correct_function_neighbors(tokens, i):
            return False

    return open_brackets == 0

def get_num_value(value: str) -> Tuple[Optional[int], Optional[float]]:
    if value == 'pi':
        return None, pi

    if value == 'e':
        return None, e

    if value.find(',') == -1:
        return int(value), None

    return None, float(value.replace(',', '.'))


class Ast_node():
    def __init__(self, token: Token) -> None:
        self.token = token
        self.number: Optional[int] = None
        self.decimal_number: Optional[float] = None

        if token.type == Type.NUMBER or token.value == 'pi' or token.value == 'e':
            self.number, self.decimal_number = get_num_value(token.value)

        self.children: List['Ast_node'] = []


def build_ast(tokens: List[Token], begin: int, start_prec: int) -> Tuple[Optional[Ast_node], int]:
    root: Optional[Ast_node] = None
    i = begin

    while i < len(tokens):
        if tokens[i].type == Type.OPEN_PAR:
            root, i = build_ast(tokens, i + 1, Prec.PARS)
            i += 1

            if start_prec == PRECEDENCE[Type.FUNCTION] or i == len(tokens)\
                    or start_prec != Prec.PARS and (PRECEDENCE[tokens[i].type].value < start_prec.value
                    or (start_prec != Prec.POWER and PRECEDENCE[tokens[i].type].value == start_prec.value)):
                return root, i

            continue

        if tokens[i].type == Type.CLOSE_PAR:
            return root, i

        if tokens[i].type == Type.NUMBER or tokens[i].value == 'pi' or tokens[i].value == 'e':
            if i == 0 or tokens[i - 1].type == Type.OPEN_PAR:
                root = Ast_node(tokens[i])
                i += 1
                continue

            if tokens[i - 1].type == Type.FUNCTION or i + 1 == len(tokens) or tokens[i + 1].type == Type.CLOSE_PAR \
                    or PRECEDENCE[tokens[i + 1].type].value < start_prec.value \
                    or (start_prec != Prec.POWER and PRECEDENCE[tokens[i + 1].type].value == start_prec.value):
                return  Ast_node(tokens[i]), i + 1

            root = Ast_node(tokens[i])
            i += 1
            continue

        if tokens[i].type == Type.FUNCTION and tokens[i].value not in INFIX_FUNCTIONS:
            root = Ast_node(tokens[i])
            argument, i = build_ast(tokens, i + 1, Prec.FUNC)
            root.children.append(argument)
            if start_prec == Prec.FUNC or (start_prec != Prec.PARS and i < len(tokens) and start_prec.value >= PRECEDENCE[tokens[i].type].value):
                return root, i
            continue

        # Now are infix functions and operators +, -, *, /, ^ left

        token_prec = PRECEDENCE[tokens[i].type]
        operator = Ast_node(tokens[i])

        if tokens[i].type == Type.MINUS and (i == 0 or tokens[i - 1].type == Type.OPEN_PAR):
            operator.children.append(Ast_node(Token('0', Type.NUMBER)))
        else:
            operator.children.append(root)

        right, i = build_ast(tokens, i + 1, token_prec)
        operator.children.append(right)

        if start_prec == token_prec or start_prec != Prec.MIN and start_prec != Prec.PARS \
                and (i >= len(tokens) or start_prec.value >= PRECEDENCE[tokens[i].type].value):
            return operator, i

        root = operator

    return root, i

def evaluation(expression: str) -> str:
    pass
