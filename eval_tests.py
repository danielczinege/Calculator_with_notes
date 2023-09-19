from typing import List, Optional, Dict
from my_eval import tokenize_expr, Token, correct_tokenized_expression, build_ast, Prec, Ast_node, evaluation

def print_tokens(tokens: Optional[List[Token]]) -> None:
    if tokens is None:
        print("Incorrect expression")
        return

    for token in tokens:
        print(token.value, end=' ')

    print()

tokens = tokenize_expr("1+ 2 - ( 3 + 4*5 * 6^(6+6)) - sin cos 565,4123 + ln (5,2 / 66,3)")
print_tokens(tokens)
print(correct_tokenized_expression(tokens))
print()

print_tokens(tokenize_expr("sin (cos 5) + cos 6"))

print_tokens(tokenize_expr("sin (cos 5) + cis 6"))

print_tokens(tokenize_expr("1,"))

print_tokens(tokenize_expr("1+ 2 - ( 3 + 4*5 * 6^(6+6)) - sin cos 565,4123 + ln (5,2 / 66,3)"))

print_tokens(tokenize_expr("1,0 /pi + 0,121/           (e)+     6"))

print_tokens(tokenize_expr("- (1 + 2) ^ 2 ^ (sin cos tan 4 * 5)"))

print("Testing correct_tokenized_expression:")
for expr in ["- 1", "1+ 2 - ( 3 + 4*5 * 6^(6+6)) - sin cos 565,4123 + ln (5,2 / 66,3)", "(3) + 4*(sin cos (e^((3)- 5 mod 6) + 3 log_base (pi)))", "sin (pi + cos e)",
             "-sin (-6 - 3-(-4^2)) - cos (-5)", "3 log_base sin 5"]:
    tokenized = tokenize_expr(expr)
    if tokenized is not None and correct_tokenized_expression(tokenized):
        print("OK")
    else:
        print("NOK")

print()

for expr in ["arcsin", "sin cos + ()", "sin cos + 5", "sin (5 + cos)", "6 mod (sin 6 cos 8)", "(3) + 4(sin cos (e^((3)- 5 mod 6) + 3 log_base (pi)))",
             "-(-5) - sin"]:
    tokenized = tokenize_expr(expr)
    if tokenized is not None and correct_tokenized_expression(tokenized):
        print("NOK")
    else:
        print("OK")

tokenized = tokenize_expr("3 log_base sin 5")
if tokenized is not None and correct_tokenized_expression(tokenized):
    print("OK")
else:
    print("NOK")

def ast_to_string(ast_root: Ast_node, begin: str, result: List[str]) -> None:
    result.append(begin)
    result.append(ast_root.token.value)
    result.append("\n")

    begin = begin + "        "
    for child in ast_root.children:
        ast_to_string(child, begin, result)

expr1 = "( 75,2 - sroot ( pi - e * 0 ) ) ^ 3 ^ 2 - 3 log_base 5 * 9 yth_root 6 + ( 8 * arcsin 5 - ( 5 / tan ( pi / 2 ) ) )"
expr2 = "3 + 4 * 2 * 5 ^ 6 ^ (6 + 1) * 8 * 9 + 10"
expr3 = "4* sin (5) ^ 6^8*7"
expr4 = "3 + 4 ^ 2 / (1 + 2 * sin (2 * 5^2^3 * 4 + 3 mod 2 mod 9 * 5 + 3) ^ (-2 - 1) * 3) * 5 ^ 3 - 1"
expr5 = "sin 7 log_base (5 + 5 yth_root 6) yth_root 5"
expr6 = "- (1 + 2,3) ^ 2,02 ^ (sin cos tan 456,45896 * 5,326)"
expr7 = "(-sin pi - e) * tan (-e + pi / 2) ^ ((-pi + 1) / 3)"
expr8 = "5 + cos (sin (9 / (3 * (2 - sin arcsin 5 / (42 + 3)) - 2) ^ 4) + 6)"

correct_solutions: Dict[str, str] = {expr1 : 
"""+
        -
                ^
                        -
                                75,2
                                sroot
                                        -
                                                pi
                                                *
                                                        e
                                                        0
                        ^
                                3
                                2
                *
                        log_base
                                3
                                5
                        yth_root
                                9
                                6
        -
                *
                        8
                        arcsin
                                5
                /
                        5
                        tan
                                /
                                        pi
                                        2
""", expr2 :
"""+
        +
                3
                *
                        *
                                *
                                        *
                                                4
                                                2
                                        ^
                                                5
                                                ^
                                                        6
                                                        +
                                                                6
                                                                1
                                8
                        9
        10
""", expr3 :
"""*
        *
                4
                ^
                        sin
                                5
                        ^
                                6
                                8
        7
""", expr4 :
"""-
        +
                3
                *
                        /
                                ^
                                        4
                                        2
                                +
                                        1
                                        *
                                                *
                                                        2
                                                        ^
                                                                sin
                                                                        +
                                                                                +
                                                                                        *
                                                                                                *
                                                                                                        2
                                                                                                        ^
                                                                                                                5
                                                                                                                ^
                                                                                                                        2
                                                                                                                        3
                                                                                                4
                                                                                        *
                                                                                                mod
                                                                                                        mod
                                                                                                                3
                                                                                                                2
                                                                                                        9
                                                                                                5
                                                                                3
                                                                -
                                                                        -
                                                                                0
                                                                                2
                                                                        1
                                                3
                        ^
                                5
                                3
        1
""", expr5 :
"""yth_root
        log_base
                sin
                        7
                +
                        5
                        yth_root
                                5
                                6
        5
""", expr6 :
"""-
        0
        ^
                +
                        1
                        2,3
                ^
                        2,02
                        *
                                sin
                                        cos
                                                tan
                                                        456,45896
                                5,326
""", expr7 :
"""*
        -
                -
                        0
                        sin
                                pi
                e
        ^
                tan
                        +
                                -
                                        0
                                        e
                                /
                                        pi
                                        2
                /
                        +
                                -
                                        0
                                        pi
                                1
                        3
""", expr8 :
"""+
        5
        cos
                +
                        sin
                                /
                                        9
                                        ^
                                                -
                                                        *
                                                                3
                                                                -
                                                                        2
                                                                        /
                                                                                sin
                                                                                        arcsin
                                                                                                5
                                                                                +
                                                                                        42
                                                                                        3
                                                        2
                                                4
                        6
"""
}

#with open("result.txt", "w") as file:
#    result: List[str] = []
#    ast_to_string(build_ast(tokenize_expr(expr5), 0, Prec.MIN)[0], "", result)
#    res = "".join(result)
#    file.write(res)

print()
print("#########################")
print("Testing building the AST:")

for expr in correct_solutions.keys():
    result: List[str] = []
    ast_to_string(build_ast(tokenize_expr(expr), 0, Prec.MIN)[0], "", result)
    res = "".join(result)

    if res == correct_solutions[expr]:
        print("OK")
    else:
        print("NOK")

print("\n###############################\n")

EXPRESSIONS_ANSWERS = {"1 - (2 + 3)" : "-4",
                       "sin (pi / 2) + (5 log_base 25 + 3 mod 2)" : "2,5",
                       "arcsin (-2,5)" : "asin value out of [-1, 1]"}

print("Testing evaluation:")

for expr in EXPRESSIONS_ANSWERS.keys():
    if evaluation(expr) == EXPRESSIONS_ANSWERS[expr]:
        print("OK")
    else:
        print("NOK")
