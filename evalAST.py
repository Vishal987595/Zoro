from dataTypeDeclaration import *
from exceptions import *
import math
from typing import Mapping

envglobal = dict()

def evalAST(program: AST, envlocal: Mapping[str, Value] = None) -> Value:
    if envlocal is None:
        envlocal = {}
    match program:
        case Frac(value):
            return value
        case Int(value):
            return value
        case Float(value):
            return value
        case Bool(value):
            return value
        case MathOp("+", left, right):
            return evalAST(left, envlocal) + evalAST(right, envlocal)
        case MathOp("-", left, right):
            return evalAST(left, envlocal) - evalAST(right, envlocal)
        case MathOp("*", left, right):
            return evalAST(left, envlocal) * evalAST(right, envlocal)
        case MathOp("%", left, right):
            return evalAST(left, envlocal) % evalAST(right, envlocal)
        case MathOp("//", left, right):
            return evalAST(left, envlocal) // evalAST(right, envlocal)
        case MathOp("**", left, right):
            return evalAST(left, envlocal) ** evalAST(right, envlocal)
        case MathOp("/", left, right):
            return evalAST(left, envlocal) / evalAST(right, envlocal)
        case CndOp(">", left, right):
            return evalAST(left, envlocal) > evalAST(right, envlocal)
        case CndOp("<", left, right):
            return evalAST(left, envlocal) < evalAST(right, envlocal)
        case CndOp("==", left, right):
            return evalAST(left, envlocal) == evalAST(right, envlocal)
        case CndOp("!=", left, right):
            return evalAST(left, envlocal) != evalAST(right, envlocal)
        case CndOp(">=", left, right):
            return evalAST(left, envlocal) >= evalAST(right, envlocal)
        case CndOp("<=", left, right):
            return evalAST(left, envlocal) <= evalAST(right, envlocal)
        case UnOp("-", right):
            return -1 * evalAST(right, envlocal)
        case UnOp("!", right):
            return not evalAST(right, envlocal)
        case UnOp("~", right):
            return ~evalAST(right, envlocal)
        case BitOp("&", left, right):
            return evalAST(left, envlocal) & evalAST(right, envlocal)
        case BitOp("|", left, right):
            return evalAST(left, envlocal) | evalAST(right, envlocal)
        case BitOp("^", left, right):
            return evalAST(left, envlocal) ^ evalAST(right, envlocal)
        case BitOp(">>", left, right):
            return evalAST(left, envlocal) >> evalAST(right, envlocal)
        case BitOp("<<", left, right):
            return evalAST(left, envlocal) << evalAST(right, envlocal)
        case BinOp("and", left, right):
            return evalAST(left) and evalAST(right)
        case BinOp("or", left, right):
            return evalAST(left) or evalAST(right)
        case If(con, seq):
            if(len(seq)==1):
                    if evalAST(con[0]):
                        return evalAST(seq[0])
            flag = 1
            for i in range(len(seq)-1):
                if evalAST(con[i]):
                    flag = 0
                    return evalAST(seq[i])
            if flag:
                return evalAST(seq[-1])
        case Assign("<-",left, right):
            value = evalAST(right)
            envglobal[left.name] = value
            return value
        case Assign("->",left, right):
            value = evalAST(left)
            envglobal[right.name] = value
            return value
        case Variable(name):
            if name in envlocal:
                return envlocal[name]
            elif name in envglobal:
                return envglobal[name]
            raise InvalidProgram() 
        case Let(Variable(name), e1, e2):
            v1 = evalAST(e1, envlocal)
            return evalAST(e2, envlocal | { name: v1 })
        case For(Variable(name), iter):
            pass