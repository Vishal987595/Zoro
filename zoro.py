from lexer import *
from evalAST import *
from Zoro_parser import *
from static_typecheck import *
import sys

if len(sys.argv) != 2:
    print("Usage: python zoro.py <file_location>")
    sys.exit(1)

file_path = sys.argv[1]
with open(file_path, 'r') as file:
    file_contents = file.read()

ans_to_parser = print_tokens(file_contents)
print(ans_to_parser)
ans_to_eval = ZoroParser(file_contents).Parsed_AST
print(ans_to_eval)
ans = evalAST(ans_to_eval)
print(ans)

