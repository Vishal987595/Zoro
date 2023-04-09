from bytecode_parser import *
from dataTypeDeclaration import *

class VM:
    bytecode: ByteCode
    ip: int
    data: List[Value]
    currentFrame: Frame
    

    def run(self):
        while True:
            assert self.ip < len(self.bytecode.instructions)
            match self.bytecode.instructions[self.ip]:

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
                        
