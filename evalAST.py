from dataTypeDeclaration import *
from lexer import *
# from exceptions import *
from env import *

# envglobal = dict()


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
        case Null(value):
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
        

        ################## FOLLOWING BLOCK TO BE "CHECKED AND VERIFIED" BY "PRAKRAM AND JUHIL"  ##################

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
        
        ####################################################################################################### 


        case AssignOp("<-",left, right):
            envlocal.add(left.name, right)
            return envlocal.get(left.name)
        case AssignOp("->",left, right):
            envlocal.add(right.name, right)
            return envlocal.get(right.name)
        case UpdateOp("<-",left, right):
            envlocal.update(left.name, right)
            return envlocal.get(left.name)
        case UpdateOp("->",left, right):
            envlocal.update(right.name, left)
            return envlocal.get(right.name)
        


        case StringOp("concat", [left, right]):
            return evalAST_(left) + evalAST_(right)
        case StringOp("slice", [string, start, end]):
            return evalAST_(string)[evalAST_(start): evalAST_(end)+1]
        case StringOp("len", string):
            return len(evalAST_(string))
        

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
        
        #######################################################################################################################################

        case List_(items):
            for i in range(len(items)):
                items[i] = evalAST_(items[i])
            return items
        case ListOp(list, "len"):
            a = list
            if type(list) == Variable:
                a = evalAST_(a)
            return a.items.__len__()
        
        case ListOp(list, "push", item):
            a = list
            if type(list) == Variable:
                a = evalAST_(a)

            a.items.append(item)
            envlocal.update(list.name, a)
            return evalAST_(item)
        case ListOp(list, "pop", item, index):
            a = list
            if type(list) == Variable:
                a = evalAST_(a)

            v = evalAST_(a.items[evalAST_(index)])
            a.items.pop(evalAST_(index))

            envlocal.update(list.name, a)
            return v
        case ListOp(list, "insert", item, index):
            a = list
            if type(list) == Variable:
                a = evalAST_(a)

            a.items.insert(evalAST_(index), item)
            envlocal.update(list.name, a)
            return evalAST_(item)
        case ListOp(list, "index", item):
            a = list
            if type(list) == Variable:
                a = evalAST_(a)

            return a.items.index(item)
        case ListOp(list, "count", item):
            a = list
            if type(list) == Variable:
                a = evalAST_(a)
            return a.items.count(item)


        ###################################################### Keywords Constructs ######################################################

        case FuncDec(name, params, seq, ret):
            name = evalAST_(name)
            if not envlocal.find(name):
                envlocal.add(name, {'params': params, 'seq': seq, 'ret': ret})
            else:
                envlocal.update(name, {'params': params, 'seq': seq, 'ret': ret})
            return envlocal.get(name)

        case FuncCall(name, args):
            name = evalAST_(name)
            if envlocal.find(name):
                envlocal.enter_scope()
                vars = envlocal.get(name)['params']
                seq = envlocal.get(name)['seq']
                ret = envlocal.get(name)['ret']
                for i in range(len(vars)):
                    if not envlocal.find(vars[i].name):
                        envlocal.add(vars[i].name, evalAST_(args[i]))
                    else:
                        envlocal.update(vars[i].name, evalAST_(args[i]))
                e = evalAST_(seq)
                r = evalAST_(ret)
                envlocal.exit_scope()
                return r
        
        case Function(name):
            return name

        case If(con, seq):
            envlocal.enter_scope()
            r = None
            if(len(seq)==1):
                    if evalAST_(con[0]):
                        r = evalAST_(seq[0])
                        envlocal.exit_scope()
                        return r
            else:
                flag = 1
                for i in range(len(seq)-1):
                    if evalAST_(con[i]):
                        flag = 0
                        r = evalAST_(seq[i])
                        envlocal.exit_scope()
                        return r
                if flag:
                    r = evalAST_(seq[-1])
                    envlocal.exit_scope()
                    return r
            
        case While(cnd, seq):
            envlocal.enter_scope()
            val = None
            while(evalAST_(cnd)):
                val = evalAST_(seq)
            envlocal.exit_scope()
            return val
        
        case For(var, iter, seq):
            envlocal.enter_scope()
            # iter = evalAST_(iter)
            # if(not envlocal.find(var.name)):
            #     envlocal.add(var.name, evalAST_(iter[0]))
            # else:
            #     envlocal.update(var.name, evalAST_(iter[0]))
            if(not envlocal.find(var.name)):
                envlocal.add(var.name, iter)
            else:
                envlocal.update(var.name, iter)
            result = None
            if type(iter) == Range:
                iter = evalAST_(iter)
            for item in iter.items:
                envlocal.update(var.name, evalAST_(item))
                result = evalAST_(seq)
            envlocal.exit_scope()
            return result
        
        case Range(num1, num2, jmp):
            num1 = evalAST_(num1)
            num2 = evalAST_(num2)
            jmp = evalAST_(jmp)
            if jmp == None:
                jmp = 1
            ret = List_
            list: List[Int] = []
            if num1 < num2:
                while num1 < num2:
                    list.append(Int(num1))
                    num1 = num1 + jmp
            else:
                while num1 > num2:
                    list.append(Int(num1))
                    num1 = num1 - jmp
            ret.items = list
            return ret
        
        ########################################################## Statements ##########################################################

        case Print(contents):
            for c in contents:
                if(type(c)==Variable):
                    c = evalAST_(c)
                print(evalAST_(c), end=" ")
            print()

        case other:
            print("writing AST is out of your scope!")
        
