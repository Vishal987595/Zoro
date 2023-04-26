import time
from lexer import *
from dataTypeDeclaration import *
from Zoro_parser import *
from bytecode_parser import *
from vm import VM
# from static_typecheck import *
import sys
# print("Bytecode interpreter")
if len(sys.argv) != 2:
    print("Usage: python3 zoro2.py <file_location>")
    sys.exit(1)

file_path = sys.argv[1]
with open(file_path, 'r') as file:
    file_contents = file.read().replace('\n', ' ')


ast = ZoroParser(file_contents).Parsed_AST

# print('----------AST-------------------------------------------------------------------------')
# print(ast)
# print()

# print('----------BYTECODE--------------------------------------------------------------------')
bytecode = parseAST(ast)
# pprint(bytecode.instructions)
# print()

# print('----------VM OUTPUT AND OTHER RESULTS-------------------------------------------------')
myvm = VM()
myvm.restart()
myvm.load(bytecode)
# t1 = time.time()
stacktop = myvm.run()
# t2 = time.time()
# print("Top of the stack after running :", stacktop)
# print("Stack :", myvm.data)
# print("Frame :", myvm.currentFrame.locals)
# print("Runtime :", t2-t1)
# print()