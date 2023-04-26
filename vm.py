from lexer import *
from dataTypeDeclaration import *
from Zoro_parser import *
from bytecode_parser import *

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
                case LOAD(name):
                    self.data.append(self.currentFrame.find(name))
                    self.ip += 1
                case STORE(name, True):
                    val = self.data.pop()
                    self.currentFrame.add(name, val)
                    self.ip += 1
                case STORE(name, False):
                    val = self.data.pop()
                    self.currentFrame.update(name, val)
                    self.ip += 1
                case STOREFUN(name, addr):
                    self.currentFrame.add(name, addr)
                    self.ip += 1
                case CALLFUN(name):
                    ip = self.currentFrame.find(name)
                    self.currentFrame = Frame(self.ip+1, self.currentFrame)
                    self.ip = ip
                case RETURN():
                    ip = self.currentFrame.retaddr
                    self.currentFrame = self.currentFrame.dynLink
                    self.ip = ip
                case PRINT():
                    val = self.data.pop()
                    print(val)
                    self.ip += 1
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
                        case 'u-':
                            right = self.data.pop()
                            self.data.append(-right)
                            self.ip += 1
                        case 'u~':
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

                        case 'push':
                            item = self.data.pop()
                            lst = self.data.pop()
                            lst.append(item)
                            self.data.append(lst)
                            self.ip += 1
                        case 'at':
                            index = self.data.pop()
                            lst = self.data.pop()
                            self.data.append(lst[index])
                            self.ip += 1
                        case 'pop':
                            lst = self.data.pop()
                            x = lst.pop()
                            self.data.append(x)
                            self.ip += 1
                        case 'popvar':
                            lst = self.data.pop()
                            x = lst.pop()
                            self.data.append(x)
                            self.data.append(lst)
                            self.ip += 1
                        case 'len':
                            lst = self.data.pop()
                            self.data.append(len(lst))
                            self.ip += 1
                        case 'insert':
                            idx = self.data.pop()
                            itm = self.data.pop()
                            lst = self.data.pop()
                            lst.insert(idx, itm)
                            self.data.append(lst)
                            self.ip += 1
                        case 'index':
                            itm = self.data.pop()
                            lst = self.data.pop()
                            self.data.append(lst.index(itm))
                            self.ip += 1
                        case 'count':
                            itm = self.data.pop()
                            lst = self.data.pop()
                            self.data.append(lst.count(itm))
                            self.ip += 1
                        case 'update':
                            idx = self.data.pop()
                            itm = self.data.pop()
                            lst = self.data.pop()
                            lst[idx] = itm
                            self.data.append(lst)
                            self.ip += 1

                        case 'strlen':
                            string = self.data.pop()
                            self.data.append(len(string))
                            self.ip += 1
                        case 'concat':
                            right = self.data.pop()
                            left = self.data.pop()
                            self.data.append(left+right)
                            self.ip += 1
                        case 'slice':
                            end = self.data.pop()
                            start = self.data.pop()
                            string = self.data.pop()
                            self.data.append(string[start:end+1])
                            self.ip += 1
                            
                case HALT():
                    if len(self.data) > 0:
                        return self.data.pop()
                    return "EMPTY STACK"

# ast = ZoroParser("var a <- fib of 7;; print a;").Parsed_AST
# bytecode = parseAST(Sequence(seq=[FuncDec(name=Function(name='fib'), params=[Variable(name='n')], body=Sequence(seq=[AssignOp(operator='<-', left=Variable(name='f'), right=Int(value=0)), If(con=[LogOp(operator='or', left=CndOp(operator='==', left=Variable(name='n'), right=Int(value=0)), right=CndOp(operator='==', left=Variable(name='n'), right=Int(value=1)))], seq=[Sequence(seq=[UpdateOp(operator='<-', left=Variable(name='f'), right=Int(value=1))], inloop=False), Sequence(seq=[UpdateOp(operator='<-', left=Variable(name='f'), right=MathOp(operator='+', left=FuncCall(name=Function(name='fib'), args=[MathOp(operator='-', left=Variable(name='n'), right=Int(value=1))]), right=FuncCall(name=Function(name='fib'), args=[MathOp(operator='-', left=Variable(name='n'), right=Int(value=2))])))], inloop=False)])], inloop=False), returns=Variable(name='f')), AssignOp(operator='<-', left=Variable(name='a'), right=FuncCall(name=Function(name='fib'), args=[Int(value=7)])), Print(contents=[Variable(name='a')])], inloop=False))
# print('-------------------------------------------')
# myVM = VM()
# myVM.load(bytecode)
# pprint(bytecode.instructions)
# print('-------------------------------------------')
# print(myVM.run())
# print(myVM.data)
# print(myVM.currentFrame.locals)
