from dataTypeDeclaration import *
from exceptions import *
from env import *

envglobal = dict()


def evalAST(program: AST, envlocal: Environment = None) -> Value:

    if envlocal is None:
        envlocal = Environment()

    def evalAST_(program):
        return evalAST(program, envlocal)
    
    match program:
        

        ########################################################## DataTypes ##########################################################


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
        

        ########################################################## Operators ##########################################################


        case MathOp("+", left, right):
            return evalAST_(left) + evalAST_(right)
        case MathOp("-", left, right):
            return evalAST_(left) - evalAST_(right)
        case MathOp("*", left, right):
            return evalAST_(left) * evalAST_(right)
        case MathOp("/", left, right):
            return evalAST_(left) / evalAST_(right)
        case MathOp("//", left, right):
            return evalAST_(left) // evalAST_(right)
        case MathOp("%", left, right):
            return evalAST_(left) % evalAST_(right)
        case MathOp("**", left, right):
            return evalAST_(left) ** evalAST_(right)
        
        case CndOp(">", left, right):
            return evalAST_(left) > evalAST_(right)
        case CndOp("<", left, right):
            return evalAST_(left) < evalAST_(right)
        case CndOp(">=", left, right):
            return evalAST_(left) >= evalAST_(right)
        case CndOp("<=", left, right):
            return evalAST_(left) <= evalAST_(right)
        case CndOp("==", left, right):
            return evalAST_(left) == evalAST_(right)
        case CndOp("!=", left, right):
            return evalAST_(left) != evalAST_(right)
        
        case UnOp("-", right):
            return (-1) * evalAST_(right)
        case UnOp("~", right):
            return ~( evalAST_(right) )
        
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
        

        ''' ################## FOLLOWING BLOCK TO BE "CHECKED AND VERIFIED" BY "PRAKRAM AND JUHIL"  ################### '''

        case LogOp("not", right):
            return not evalAST_(right)
        case LogOp("and", left, right):
            return evalAST_(left) and evalAST_(right)
        case LogOp("or", left, right):
            return evalAST_(left) or evalAST_(right)
        case LogOp("xor", left, right):
            if(left==right):
                return 0    
            else:
                return evalAST_(left) or evalAST_(right)
        
        case LogOp("nand", left, right):
            return not ( evalAST_(left) and evalAST_(right) )
        case LogOp("nor", left, right):
            return not ( evalAST_(left) or evalAST_(right) )
        case LogOp("xnor", left, right):
            if(left==right):
                return not (0)
            else:
                return not ( evalAST_(left) or evalAST_(right) )
        
        ''' ####################################################################################################### '''


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

        case StringOp("concat", [left, right]):
            return evalAST_(left) + evalAST_(right)
        case StringOp("slice", [string, start, end]):
            return evalAST_(string)[evalAST_(start): evalAST_(end)+1]
        

        ###################################################### Identifier Constructs ######################################################


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
        
        case Sequence(seq):
            val = None
            for i in seq:
                val = evalAST_(i)
            return val
        
        case List_(items):
            for i in range(len(items)):
                print(items[i])
                items[i] = evalAST_(items[i])
            return items
        case ListOp("len", list):
            return list.__len__()
        case ListOp("push", list, item):
            a = evalAST_(list)
            a.append(evalAST_(item))
            envlocal.update(list.name, a)
            return evalAST_(item)
        case ListOp("pop", list, item, index):
            a = evalAST_(list)
            v = evalAST_(a[evalAST_(index)])
            a.pop(evalAST_(index))
            envlocal.update(list.name, a)
            return v
        case ListOp("insert", list, item, index):
            a = evalAST_(list)
            a.insert(evalAST_(index), evalAST_(item))
            envlocal.update(list.name, a)
            return evalAST_(item)
        case ListOp("index", list, item):
            a = evalAST_(list)
            return a.index(evalAST_(item))
        case ListOp("count", list, item):
            a = evalAST_(list)
            return a.count(evalAST_(item))


        ###################################################### Keywords Constructs ######################################################


        # case Func_call(name, args):
        #   pass
        #   # TO BE COMPLETED

        # case Func_dec(name, params, seq, ret):
        #     if not envlocal.find(name):
        #         envlocal.add(name, {'params': params, 'seq': seq, 'ret': ret})
        #     else:
        #         envlocal.update(name, {'params': params, 'seq': seq, 'ret': ret})
        #     return envlocal[name]

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
        
        case While(cnd, seq):
            val = None
            while(evalAST_(cnd)):
                val = evalAST_(seq)
            return val
        
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
        
        ########################################################## Statements ##########################################################

        case Print(contents):
            for c in contents:
                print(evalAST_(c), end=" ")
            print()
        
