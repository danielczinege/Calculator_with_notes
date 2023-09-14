from typing import List, Optional
from my_eval import tokenize_expr, Token, correct_tokenized_expression

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

print("Testing correct_tokenized_expression:")
for expr in ["- 1", "1+ 2 - ( 3 + 4*5 * 6^(6+6)) - sin cos 565,4123 + ln (5,2 / 66,3)", "(3) + 4*(sin cos (e^((3)- 5 mod 6) + 3 log_base (pi)))", "sin (pi + cos e)",
             "-sin (-6 - 3-(-4^2)) - cos (-5)"]:
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
