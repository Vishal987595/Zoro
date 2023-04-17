from dataTypeDeclaration import *
from lexer import *
# from exceptions import *
from env import *
import copy

# envglobal = dict()


def evalAST(program: AST, envlocal: Environment = None) -> Value:

    if envlocal is None:
        envlocal = Environment()

    def evalAST_(program):
        return evalAST(program, envlocal)
    
    def varevalAST_(program):
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
            # print("left", type(left))
            # print("leftvalue", left.value)
            # print("right", type(right))
            # print("rightvalue", evalAST_(right))
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
            # if type(left) == Variable:
            #     left = evalAST_(left)
            # if type(right) == Variable:
            #     right = evalAST_(right)
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
            if(type(right) != Int and type(right) != Float and type(right) != Frac and type(right) != Bool and type(right) != String and type(right) != Null and type(right) != List_):
                # print("TTTTTTTTTTTTT", right)
                right = evalAST_(right)
                # print("YYYYYYYYYYYYY", right)
                # print("YYYYYYYYYYYYY", type(right))
                if(isinstance(right, int)):
                    right = Int(value=right)
                elif(isinstance(right, float)):
                    right = Float(value=right)
                elif(isinstance(right, bool)):
                    right = Bool(value=right)
                elif(isinstance(right, str)):
                    right = String(value=right)   
            envlocal.add(left.name, right)
            return envlocal.get(left.name)
        case AssignOp("->",left, right):
            if(type(right) != Int and type(right) != Float and type(right) != Frac and type(right) != Bool and type(right) != String and type(right) != Null and type(right) != List_):
                right = evalAST_(right)
                if(isinstance(right, int)):
                    right = Int(value=right)
                elif(isinstance(right, float)):
                    right = Float(value=right)
                elif(isinstance(right, bool)):
                    right = Bool(value=right)
                elif(isinstance(right, str)):
                    right = String(value=right)   
            envlocal.add(right.name, right)
            return envlocal.get(right.name)
        case UpdateOp("<-",left, right):
            if(type(right) != Int and type(right) != Float and type(right) != Frac and type(right) != Bool and type(right) != String and type(right) != Null and type(right) != List_):
                right = evalAST_(right)
                if(isinstance(right, int)):
                    right = Int(value=right)
                elif(isinstance(right, float)):
                    right = Float(value=right)
                elif(isinstance(right, bool)):
                    right = Bool(value=right)
                elif(isinstance(right, str)):
                    right = String(value=right)   
            if left.name[0] != '_':
                envlocal.update(left.name, right)
                return envlocal.get(left.name)
            else:
                #Raise error here
                # print(f"Patthar ki lakeer hai \"{left.name}\", Janaab, badlegi nahi")
                print(f"\"{left.name[1:]}\" sunke mutable samjhe the kya? Immutable hai apun, badlega nai saala")
                # return envlocal.get(left.name)
        case UpdateOp("->",left, right):
            if(type(left) != Int and type(left) != Float and type(left) != Frac and type(left) != Bool and type(left) != String and type(left) != Null and type(left) != List_):
                left = evalAST_(left)
                if(isinstance(left, int)):
                    left = Int(value=left)
                elif(isinstance(left, float)):
                    left = Float(value=left)
                elif(isinstance(left, bool)):
                    left = Bool(value=left)
                elif(isinstance(left, str)):
                    left = String(value=left)
            if right.name[0] != '_':
                envlocal.update(right.name, left)
                return envlocal.get(right.name)
            else:
                # raise error here
                print(f"\"{right.name[1:]}\" sunke mutable samjhe the kya? Immutable hai apun, badlega nai saala")
                # return envlocal.get(right.name)
        


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
            return evalAST_(envlocal.get(name))
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
                if(type(val) == Returns):
                    break
            return val
        
        case Returns(value):
            if(type(value) != Int and type(value) != Float and type(value) != Frac and type(value) != Bool and type(value) != String and type(value) != Null and type(value) != List_):
                value = evalAST_(value)
                if(isinstance(value, int)):
                    value = Int(value=value)
                elif(isinstance(value, float)):
                    value = Float(value=value)
                elif(isinstance(value, bool)):
                    value = Bool(value=value)
                elif(isinstance(value, str)):
                    value = String(value=value)    
            return program
        
        #######################################################################################################################################

        case List_(items):
            # for i in range(len(items)):
            #     items[i] = evalAST_(items[i])
            return items
        case ListOp(list, "len"):
            a = list
            if type(list) == Variable:
                a = evalAST_(a)
                a = List_(items=a)
            return a.items.__len__()
        
        case ListOp(list, "push", item):
            a = list
            if type(list) == Variable:
                a = evalAST_(a)
                a = List_(items=a)
            if type(item) == Int:
                a.items.append(Int(evalAST_(item)))
            elif type(item) == Float:
                a.items.append(Float(evalAST_(item)))
            elif type(item) == Frac:
                a.items.append(Frac(evalAST_(item)))
            elif type(item) == Bool:
                a.items.append(Bool(evalAST_(item)))
            elif type(item) == String:
                a.items.append(String(evalAST_(item)))
            elif type(item) == Variable:
                x = evalAST_(item)
                if type(x) == int:
                    a.items.append(Int(evalAST_(item)))
                # Add other cases
            envlocal.update(list.name, a)
            return evalAST_(a)
        case ListOp(list, "pop", item, index):
            a = list
            if type(list) == Variable:
                a = evalAST_(a)
                a = List_(items=a)

            v = evalAST_(a.items[evalAST_(index)])
            a.items.pop(evalAST_(index))

            envlocal.update(list.name, a)
            return v
        case ListOp(list, "insert", item, index):
            a = list
            if type(list) == Variable:
                a = evalAST_(a)
                a = List_(items=a)

            a.items.insert(evalAST_(index), item)
            envlocal.update(list.name, a)
            return evalAST_(item)
        case ListOp(list, "index", item):
            a = list
            if type(list) == Variable:
                a = evalAST_(a)
                a = List_(items=a)
            return a.items.index(item)
        case ListOp(list, "at", item, index):
            a = list
            if type(list) == Variable:
                a = evalAST_(a)
                a = List_(items=a)
            return evalAST_(a.items[evalAST_(index)])

        case ListOp(list, "count", item):
            a = list
            if type(list) == Variable:
                a = evalAST_(a)
                a = List_(items=a)
            return a.items.count(item)
        
        case ListOp(list, "update", item, index):
            a = list
            if type(list) == Variable:
                a = evalAST_(a)
                a = List_(items=a)
            a.items[evalAST_(index)] = item
            return evalAST_(item)

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
                    right = args[i]
                    if(type(right) != Int and type(right) != Float and type(right) != Frac and type(right) != Bool and type(right) != String and type(right) != Null and type(right) != List_):
                        right = evalAST_(right)
                        if(isinstance(right, int)):
                            right = Int(value=right)
                        elif(isinstance(right, float)):
                            right = Float(value=right)
                        elif(isinstance(right, bool)):
                            right = Bool(value=right)
                        elif(isinstance(right, str)):
                            right = String(value=right)  
                    # if not envlocal.find(vars[i].name):
                        
                    #     envlocal.add(vars[i].name, right)
                    # else:
                    #     envlocal.update(vars[i].name, right)
                    envlocal.add(vars[i].name, right)
                e = evalAST_(seq)
                r = evalAST_(ret)
                envlocal.exit_scope()
                return r
        # case FuncCall(name, args):
        #     name = evalAST_(name)
        #     if envlocal.find(name):
        #         envlocal.enter_scope()
        #         vars = envlocal.get(name)['params']
        #         seq = envlocal.get(name)['seq']
        #         ret = envlocal.get(name)['ret']
        #         for i in range(len(vars)):
        #             right = args[i]
        #             if(type(right) != Int and type(right) != Float and type(right) != Frac and type(right) != Bool and type(right) != String and type(right) != Null and type(right) != List_):
        #                 right = evalAST_(right)
        #                 if(isinstance(right, int)):
        #                     right = Int(value=right)
        #                 elif(isinstance(right, float)):
        #                     right = Float(value=right)
        #                 elif(isinstance(right, bool)):
        #                     right = Bool(value=right)
        #                 elif(isinstance(right, str)):
        #                     right = String(value=right)  
        #             # if not envlocal.find(vars[i].name):
                        
        #             #     envlocal.add(vars[i].name, right)
        #             # else:
        #             #     envlocal.update(vars[i].name, right)
        #             envlocal.add(vars[i].name, right)
        #         e = evalAST_(seq)
        #         r = None
        #         if type(e) == Returns:
        #             r = evalAST_(e.value)
        #         # r = evalAST_(ret)
        #         envlocal.exit_scope()
        #         return r
        
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
                if flag and (len(seq) != len(con)):
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
            if(not envlocal.find(var.name)):
                envlocal.add(var.name, iter)
            else:
                envlocal.update(var.name, iter)
            result = None
            if type(iter) == Range:
                iter = evalAST_(iter)
            for item in iter.items:
                if(type(item) != Int and type(item) != Float and type(item) != Frac and type(item) != Bool and type(item) != String and type(item) != Null and type(item) != List_):
                    item = evalAST_(item)
                    if(isinstance(item, int)):
                        item = Int(value=item)
                    elif(isinstance(item, float)):
                        item = Float(value=item)
                    elif(isinstance(item, bool)):
                        item = Bool(value=item)
                    elif(isinstance(item, str)):
                        item = String(value=item)  
                envlocal.update(var.name, item)
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
                # if(type(c)==Variable):
                #     c = evalAST_(c)
                c = copy.copy(evalAST_(c))
                # print("TYPEEEEEEE",type(c))
                if(isinstance(c, type([]))):
                    for i in range(len(c)):
                        c[i] = evalAST_(c[i])
                print(c, end=" ")
            print()

        case other:
            print("writing AST is out of your scope!")




# FuncCall : fib of n-1 #you should also allow fib of (n-1)
# FuncCall: fib of n-1 + fib of n-2 # you should also allow fib of (n-1) + fib of (n-2)
# add Returns
# Optional Pass
# Comments (single line and multi line)
