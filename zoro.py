from Zoro_parser import *
from dataTypeDeclaration import *
from evalAST import *
# from static_typecheck import *
import sys

if len(sys.argv) != 2:
    print("Usage: python3 zoro.py <file_location>")
    sys.exit(1)

file_path = sys.argv[1]
with open(file_path, 'r') as file:
    file_contents = file.read().replace('\n', ' ')

ans_to_parser = print_tokens(file_contents)

ans_to_eval = ZoroParser(file_contents).Parsed_AST

evalAST(ans_to_eval)


