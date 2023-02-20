from dataTypeDeclaration import *
from exceptions import *
import math
from typing import Mapping
from env import *

envglobal = dict()

def evalAST(program: AST, envlocal: Environment = None) -> Value:
    if envlocal is None:
        envlocal = Environment()

    def evalAST_(program):
        return evalAST(program, envlocal)
    
    match program:
        case Frac(value):
            return value
        case Int(value):
            return value
        case Float(value):
            return value
        case Bool(value):
            return value
        case String(value):
            return value
        case MathOp("+", left, right):
            return evalAST_(left) + evalAST_(right)
        case MathOp("-", left, right):
            return evalAST_(left) - evalAST_(right)
        case MathOp("*", left, right):
            return evalAST_(left) * evalAST_(right)
        case MathOp("%", left, right):
            return evalAST_(left) % evalAST_(right)
        case MathOp("//", left, right):
            return evalAST_(left) // evalAST_(right)
        case MathOp("**", left, right):
            return evalAST_(left) ** evalAST_(right)
        case MathOp("/", left, right):
            return evalAST_(left) / evalAST_(right)
        case CndOp(">", left, right):
            return evalAST_(left) > evalAST_(right)
        case CndOp("<", left, right):
            return evalAST_(left) < evalAST_(right)
        case CndOp("==", left, right):
            return evalAST_(left) == evalAST_(right)
        case CndOp("!=", left, right):
            return evalAST_(left) != evalAST_(right)
        case CndOp(">=", left, right):
            return evalAST_(left) >= evalAST_(right)
        case CndOp("<=", left, right):
            return evalAST_(left) <= evalAST_(right)
        case UnOp("-", right):
            return -1 * evalAST_(right)
        case UnOp("!", right):
            return not evalAST_(right)
        case UnOp("~", right):
            return ~evalAST_(right)
        case BitOp("&", left, right):
            return evalAST_(left) & evalAST_(right)
        case BitOp("|", left, right):
            return evalAST_(left) | evalAST_(right)
        case BitOp("^", left, right):
            return evalAST_(left) ^ evalAST_(right)
        case BitOp(">>", left, right):
            return evalAST_(left) >> evalAST_(right)
        case BitOp("<<", left, right):
            return evalAST_(left) << evalAST_(right)
        case BinOp("and", left, right):
            return evalAST_(left) and evalAST_(right)
        case BinOp("or", left, right):
            return evalAST_(left) or evalAST_(right)
        case Print(contents):
            for c in contents:
                print(evalAST_(c), end=" ")
            print()
        case StringOp("concat", [left, right]):
            return evalAST_(left) + evalAST_(right)
        case StringOp("slice", [string, start, end]):
            return evalAST_(string)[evalAST_(start): evalAST_(end)+1
        case If(con, seq):
            if(len(seq)==1):
                    if evalAST_(con[0]):
                        return evalAST_(seq[0])
            flag = 1
            for i in range(len(seq)-1):
                if evalAST_(con[i]):
                    flag = 0
                    return evalAST_(seq[i])
            if flag:
                return evalAST_(seq[-1])
        case AssignOp("<-",left, right):
            if(not envlocal.find(left.name)):
                envlocal.add(left.name, evalAST_(right))
            else:
                envlocal.update(left.name, evalAST_(right))
            return envlocal.get(left.name)
        case AssignOp("->",left, right):
            if(not envlocal.find(right.name)):
                envlocal.add(right.name, evalAST_(left))
            else:
                envlocal.update(right.name, evalAST_(left))
            return envlocal.get(right.name)
        case Put(Variable(name), e):
            envlocal.add(name, evalAST_(e))
            return envlocal.get(name)
        case Get(Variable(name)):
            return envlocal.get(name)
        case Variable(name):
            return envlocal.get(name)
        case Let(Variable(name), e1, e2):
            v1 = evalAST_(e1)
            envlocal.enter_scope()
            envlocal.add(name, v1)
            v2 = evalAST_(e2)
            envlocal.exit_scope()
            return v2
        case For(var, iter, seq):
            if(not envlocal.find(var.name)):
                envlocal.add(var.name, evalAST_(iter[0]))
            else:
                envlocal.update(var.name, evalAST_(iter[0]))
            for item in iter:
                envlocal.update(var.name, evalAST_(item))
                result = None
                for stmt in seq.seq:
                    result = evalAST_(stmt)
                if result is not None:
                    return result
        case While(cnd, seq):
            val = None
            while(evalAST_(cnd)):
                val = evalAST_(seq)
            return val
        case Sequence(seq):
            val = None
            for i in seq:
                val = evalAST_(i)
            return val
        case Funcdec(name, args, seq, ret):
            if not envlocal.find(name):
                envlocal.add(name, {'args': args, 'seq': seq, 'ret': ret})
            else:
                envlocal.update(name, {'args': args, 'seq': seq, 'ret': ret})
            return envlocal[name]
        case FuncCall(name, args):
            if envlocal.find(name):
                vars = envlocal[name]['args']
                seq = envlocal[name]['seq']
                ret = envlocal[name]['ret']
                for i in range(len(vars)):
                    if not envlocal.find(vars[i].name):
                        envlocal.add(vars[i].name, evalAST_(args[i]))
                    else:
                        envlocal.update(vars[i].name, evalAST_(args[i]))
                e = evalAST_(seq)
                return evalAST_(ret)
                                    
