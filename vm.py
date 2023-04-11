from bytecode_parser import *
from dataTypeDeclaration import *

class VM:
    bytecode: ByteCode
    ip: int
    data: List[Value]
    currentFrame: Frame

    def load(self, code):
        self.bytecode=code
        self.restart()

    def restart(self):
        self.ip = 0
        self.data = []
        self.currentFrame = Frame()

    def run(self):
        while True:
            assert self.ip < len(self.bytecode.instructions)
            match self.bytecode.instructions[self.ip]:
                case PUSH(val):
                    self.data.append(val)
                    self.ip += 1
                case POP():
                    self.data.pop()
                    self.ip += 1
                case DUP():
                    val = self.data.pop()
                    self.data.append(val)
                    self.data.append(val)
                    self.ip += 1
                case JMP_IF_FALSE(to):
                    val = self.data.pop()
                    if not val:
                        self.ip = to.label
                    else:
                         self.ip += 1
                case JMP_IF_TRUE(to):
                    val = self.data.pop()
                    if val:
                        self.ip = to.label
                    else:
                         self.ip += 1
                case JMP(to):
                    self.ip = to.label
                case Operator(op):
                    match op:
                        case '+':
                            right = self.data.pop()
                            left = self.data.pop()
                            self.data.append(left+right)
                            self.ip += 1
                        case '-':
                            right = self.data.pop()
                            left = self.data.pop()
                            self.data.append(left-right)
                            self.ip += 1
                        case '*':
                            right = self.data.pop()
                            left = self.data.pop()
                            self.data.append(left*right)
                            self.ip += 1
                        case '/':
                            right = self.data.pop()
                            left = self.data.pop()
                            self.data.append(left/right)
                            self.ip += 1
                        case '//':
                            right = self.data.pop()
                            left = self.data.pop()
                            self.data.append(left//right)
                            self.ip += 1
                        case '**':
                            right = self.data.pop()
                            left = self.data.pop()
                            self.data.append(left**right)
                            self.ip += 1
                        case '%':
                            right = self.data.pop()
                            left = self.data.pop()
                            self.data.append(left%right)
                            self.ip += 1
                        
                        case '>':
                            right = self.data.pop()
                            left = self.data.pop()
                            self.data.append(left>right)
                            self.ip += 1
                        case '<':
                            right = self.data.pop()
                            left = self.data.pop()
                            self.data.append(left<right)
                            self.ip += 1
                        case '>=':
                            right = self.data.pop()
                            left = self.data.pop()
                            self.data.append(left>=right)
                            self.ip += 1
                        case '<=':
                            right = self.data.pop()
                            left = self.data.pop()
                            self.data.append(left<=right)
                            self.ip += 1
                        case '==':
                            right = self.data.pop()
                            left = self.data.pop()
                            self.data.append(left==right)
                            self.ip += 1
                        case '!=':
                            right = self.data.pop()
                            left = self.data.pop()
                            self.data.append(left!=right)
                            self.ip += 1
                        
                        case 'not':
                            right = self.data.pop()
                            self.data.append(not right)
                            self.ip += 1
                        case '-':
                            right = self.data.pop()
                            self.data.append(-right)
                            self.ip += 1
                        case '~':
                            right = self.data.pop()
                            self.data.append(~right)
                            self.ip += 1
                        
                        case '&':
                            right = self.data.pop()
                            left = self.data.pop()
                            self.data.append(left&right)
                            self.ip += 1
                        case '|':
                            right = self.data.pop()
                            left = self.data.pop()
                            self.data.append(left|right)
                            self.ip += 1
                        case '^':
                            right = self.data.pop()
                            left = self.data.pop()
                            self.data.append(left^right)
                            self.ip += 1
                        case '<<':
                            right = self.data.pop()
                            left = self.data.pop()
                            self.data.append(left<<right)
                            self.ip += 1
                        case '>>':
                            right = self.data.pop()
                            left = self.data.pop()
                            self.data.append(left>>right)
                            self.ip += 1
            

                case HALT():
                    if len(self.data) > 0:
                        return self.data.pop()
                    return self.data.pop()
                  
# ast = ZoroParser("<ZORO CODE HERE>").Parsed_AST
# bytecode = parseAST(<AST HERE>)
# print('-------------------------------------------')
# myVM = VM()
# myVM.load(bytecode)
# pprint(bytecode.instructions)
# print('-------------------------------------------')
# print(myVM.run()) #Will print the popped top of the stack
# print(myVM.data)  #Will print the rest of the elements (if any) in the stack