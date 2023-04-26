from typing import Dict
from lexer import *
from dataTypeDeclaration import *


class VariableNotFoundError(Exception):
    def __init__(self, name):
        super().__init__(f"\'{name}\' is there, but only in your imagination.")

# If a new instruction is defined, add a dataclass, class name should be in all caps
@dataclass
class PUSH:
    val: Value

@dataclass
class POP:
    pass

@dataclass
class DUP:
    pass

@dataclass
class LABEL:
    label: int = -1

@dataclass
class JMP_IF_FALSE:
    to: LABEL

@dataclass
class JMP_IF_TRUE:
    to: LABEL

@dataclass
class JMP:
    to: LABEL

@dataclass
class HALT:
    pass

@dataclass
class LOAD:
    localname: str

@dataclass
class STORE:
    localname: str
    newvar: bool = False

@dataclass
class STOREFUN:
    name: str
    addr: int

@dataclass
class CALLFUN:
    name: str

@dataclass
class RETURN:
    pass

@dataclass
class PRINT:
    pass


#If you define a new instruction, add it here
Instructions = PUSH | POP | DUP | JMP_IF_FALSE | JMP_IF_TRUE | JMP | HALT | Operator | LOAD | STORE | RETURN | STOREFUN | CALLFUN | PRINT


class ByteCode:
    instructions: List[Instructions]
    jmp_addr: LABEL = None
    iter_cnt: int = 0

    def __init__(self):
        self.instructions = []

    def label(self):
        return LABEL(-1)
    
    def emit(self, ins):
        self.instructions.append(ins)

    def emit_label(self, label):
        label.label = len(self.instructions)

    def set_break_addr(self, label):
        self.jmp_addr = label

class Frame:
    locals: Dict[str, Value]
    retaddr: int
    dynLink: 'Frame'

    def __init__(self, retaddr=-1, dynlink=None):
        self.locals = {}
        self.retaddr = retaddr
        self.dynLink = dynlink

    def find(self, name):
        if name in self.locals:
            return self.locals[name]
        elif self.dynLink != None:
            return self.dynLink.find(name)
        raise VariableNotFoundError(name)

    def add(self, name, value):
        self.locals[name] = value
    
    def update(self, name, value):
        if name in self.locals:
            self.locals[name] = value
            return
        elif self.dynLink != None:
            self.dynLink.update(name, value)
        raise VariableNotFoundError(name)

l = []
currFrame = Frame()

#in case of binary operations, please remember that left is pushed before right
#thus while popping, the first value you pop will be right, not left.
def parseAST_(ast: AST, code: ByteCode, ) -> None:

    def parse_(ast):
        parseAST_(ast, code)

    match ast:
        case Frac(value):
            code.emit(PUSH(value))
        case Int(value):
            code.emit(PUSH(value))
        case Float(value):
            code.emit(PUSH(value))
        case Bool(value):
            code.emit(PUSH(value))
        case String(value):
            code.emit(PUSH(value))

        case Variable(name):
            code.emit(LOAD(name))

        case AssignOp('<-', left, right):
            parse_(right)
            code.emit(STORE(left.name, True))
        case AssignOp('->', left, right):
            parse_(left)
            code.emit(STORE(right.name, True))

        case UpdateOp('<-', left, right):
            parse_(right)
            code.emit(STORE(left.name, False))
        case UpdateOp('->', left, right):
            parse_(left)
            code.emit(STORE(right.name, False))

        case MathOp("+", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('+'))
        case MathOp("-", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('-'))
        case MathOp("*", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('*'))
        case MathOp("/", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('/'))
        case MathOp("//", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('//'))
        case MathOp("**", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('**'))
        case MathOp("%", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('%'))

        case CndOp(">", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('>'))
        case CndOp("<", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('<'))
        case CndOp(">=", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('>='))
        case CndOp("<=", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('<='))
        case CndOp("==", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('=='))
        case CndOp("!=", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('!='))

        case UnOp("-", right):
            parse_(right)
            code.emit(Operator('u-'))
        case UnOp("~", right):
            parse_(right)
            code.emit(Operator('u~'))
        case UnOp("not", right):
            parse_(right)
            code.emit(Operator('not'))

        case BitOp("&", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('&'))
        case BitOp("|", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('|'))
        case BitOp("^", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('^'))
        case BitOp("<<", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('<<'))
        case BitOp(">>", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('>>'))
        
        case LogOp("and", left, right):
            label = LABEL()
            parse_(left)
            code.emit(DUP())
            code.emit(JMP_IF_FALSE(label))
            code.emit(POP())
            parse_(right)
            code.emit_label(label)
        case LogOp("or", left, right):
            label = LABEL()
            parse_(left)
            code.emit(DUP())
            code.emit(JMP_IF_TRUE(label))
            code.emit(POP())
            parse_(right)
            code.emit_label(label)
        case LogOp("xor", left, right):
            parse_(LogOp('or', LogOp('and', left, UnOp('not', right)), LogOp('and', UnOp('not', left), right)))
        case LogOp("nand", left, right):
            parse_(LogOp("and", left, right))
            code.emit(Operator('not'))
        case LogOp("nor", left, right):
            parse_(LogOp("or", left, right))
            code.emit(Operator('not'))
        case LogOp("xnor", left, right):
            parse_(LogOp("xor", left, right))
            code.emit(Operator('not'))

        case Print(contents):
            for c in contents:
                parse_(c)
                code.emit(PRINT())

        case Sequence(seq):
            for s in seq:
                parse_(s)

        case If(con, seq):
            endlab = LABEL()
            l = len(con)
            for i in range(l):
                falselab=LABEL()
                parse_(con[i])
                code.emit(JMP_IF_FALSE(falselab))
                parse_(seq[i])
                code.emit(JMP(endlab))
                code.emit_label(falselab)
            if len(seq) > l:
                parse_(seq[l])
            code.emit_label(endlab)

        case While(cnd, seq):
            looplab = LABEL()
            endlab = LABEL()
            code.set_break_addr(endlab)
            code.emit_label(looplab)
            parse_(cnd)
            code.emit(JMP_IF_FALSE(endlab))
            parse_(seq)
            code.emit(JMP(looplab))
            code.emit_label(endlab)

        case For(var, iter, body):
            l = Int(len(iter.items))
            i = Variable(str(code.iter_cnt) + "_iter")
            lst = Variable(str(code.iter_cnt) + "_ilst")
            parse_(AssignOp("<-", lst, iter))
            code.iter_cnt += 1
            var_assgn = AssignOp("<-", i, Int(0))
            parse_(var_assgn)
            var_update = AssignOp("<-", var, ListOp(lst, "at", None, i))
            idx_update = AssignOp("<-", i, MathOp("+", i, Int(1)))
            parse_(While(CndOp("<", i, l), Sequence(seq=[var_update] + body.seq + [idx_update])))
            code.iter_cnt -= 1

        case Keyword('break'):
            code.emit(JMP(code.jmp_addr))

        case FuncDec(name, params, body):
            funlab = LABEL()
            beginlab = LABEL()
            code.emit_label(funlab)
            code.emit(STOREFUN(name.name, funlab.label+2))
            code.emit(JMP(beginlab))
            code.emit_label(funlab)
            for p in reversed(params):
                code.emit(STORE(p.name, True))
            parse_(body)
            code.emit(RETURN())
            code.emit_label(beginlab)
        
        case Returns(ast):
            parse_(ast)
            code.emit(RETURN())

        case FuncCall(name, args):
            for a in args:
                parse_(a)
            code.emit(CALLFUN(name.name))

        case List_(items):
            code.emit(PUSH([]))
            for i in items:
                parse_(i)
                code.emit(Operator('push'))

        case ListOp(lst, "push", item):
            if type(lst) == List_:
                parse_(lst)
                parse_(item)
                code.emit(Operator('push'))
            if type(lst) == Variable:
                code.emit(LOAD(lst.name))
                parse_(item)
                code.emit(Operator('push'))
                code.emit(STORE(lst.name))
        case ListOp(lst, "at", item, index):
            if type(lst) == List_:
                parse_(lst)
            if type(lst) == Variable:
                code.emit(LOAD(lst.name))
            parse_(index)
            code.emit(Operator('at'))
        case ListOp(lst, "pop", item, index):
            if type(lst) == List_:
                parse_(lst)
                parse_(item)
                code.emit(Operator('pop'))
            if type(lst) == Variable:
                code.emit(LOAD(lst.name))
                parse_(item)
                code.emit(Operator('popvar'))
                code.emit(STORE(lst.name))
        case ListOp(lst, "len"):
            if type(lst) == List_:
                code.emit(PUSH(len(lst.items)))
            if type(lst) == Variable:
                code.emit(LOAD(lst.name))
                code.emit(Operator('len'))
        case ListOp(lst, "insert", item, index):
            if type(lst) == List_:
                parse_(lst)
                parse_(item)
                parse_(index)
                code.emit(Operator('insert'))
            if type(lst) == Variable:
                code.emit(LOAD(lst.name))
                parse_(item)
                parse_(index)
                code.emit(Operator('insert'))
                code.emit(STORE(lst.name))
        case ListOp(lst, "index", item):
            if type(lst) == List_:
                parse_(lst)
                parse_(item)
                code.emit(Operator('index'))
            if type(lst) == Variable:
                code.emit(LOAD(lst.name))
                parse_(item)
                code.emit(Operator('index'))
        case ListOp(lst, "count", item):
            if type(lst) == List_:
                parse_(lst)
                parse_(item)
                code.emit(Operator('count'))
            if type(lst) == Variable:
                code.emit(LOAD(lst.name))
                parse_(item)
                code.emit(Operator('count'))
        case ListOp(lst, "update", item, index):
            if type(lst) == List_:
                parse_(lst)
                parse_(item)
                parse_(index)
                code.emit(Operator('update'))
            if type(lst) == Variable:
                code.emit(LOAD(lst.name))
                parse_(item)
                parse_(index)
                code.emit(Operator('update'))
                code.emit(STORE(lst.name))
        
        case StringOp("strlen", [string, Null(None)]):
            if type(string) == String:
                code.emit(PUSH(len(string.value)))
            if type(string) == Variable:
                code.emit(LOAD(string.name))
                code.emit(Operator('strlen'))
        case StringOp("concat", [left, right]):
            if type(left) == String:
                parse_(left)
            if type(left) == Variable:
                code.emit(LOAD(left.name))
            if type(right) == String:
                parse_(right)
            if type(right) == Variable:
                code.emit(LOAD(right.name))
            code.emit(Operator('concat'))
        case StringOp("slice", [string, (start, end)]):
            if type(string) == String:
                parse_(string)
            if type(string) == Variable:
                code.emit(LOAD(string.name))
            if type(start) == Int:
                parse_(start)
            if type(start) == Variable:
                code.emit(LOAD(start.name))
            if type(end) == Int:
                parse_(end)
            if type(end) == Variable:
                code.emit(LOAD(end.name))
            code.emit(Operator('slice'))

# Add the prettyprint case for the newly defined instruction here.
def pprint(l):
    c = 0
    for i in l:
        match i:
            case PUSH(val):
                if type(val) == str:
                    print(f"\t{c}\t: PUSH    \t\"{val}\"")
                else:
                    print(f"\t{c}\t: PUSH    \t{val}")
            case Operator(op):
                print(f"\t{c}\t: {op}")
            case DUP():
                print(f"\t{c}\t: DUP")
            case POP():
                print(f"\t{c}\t: POP")
            case JMP(to):
                print(f"\t{c}\t: JMP    \t{to.label}")
            case JMP_IF_FALSE(to):
                print(f"\t{c}\t: JMP_IF_FALSE\t{to.label}")
            case JMP_IF_TRUE(to):
                print(f"\t{c}\t: JMP_IF_TRUE\t{to.label}")
            case LOAD(name):
                print(f"\t{c}\t: LOAD    \t{name}")
            case STORE(name, True):
                print(f"\t{c}\t: STORE    \t{name} \tDEFINED")
            case STORE(name, False):
                print(f"\t{c}\t: STORE    \t{name}")
            case RETURN():
                print(f"\t{c}\t: RETURN")
            case STOREFUN(name, addr):
                print(f"\t{c}\t: STOREFUN    \t{name} \tAT {addr}")
            case CALLFUN(name):
                print(f"\t{c}\t: CALLFUN    \t{name}")
            case PRINT():
                print(f"\t{c}\t: PRINT")
            case HALT():
                print(f"\t{c}\t: HALT")
        c += 1

def parseAST(ast):
    code = ByteCode()
    parseAST_(ast, code)
    code.emit(HALT())
    return code


# ans_to_parser, lines = print_tokens("fun f of a,b,c is var d <- a+b+c; returns d; endfun; var e <- f of 1,2,3;;")
# ast = ZoroParser(ans_to_parser)
# ast = ZoroParser("fun f of a,b,c is var d <- a+b+c; returns d; endfun; var e <- f of 1,2,3;;").Parsed_AST
# ast = ZoroParser("1+2;").Parsed_AST
# print(ast)
# code = parseAST(Sequence(seq=[MathOp(operator='+', left=Int(value=1), right=Int(value=2))], inloop=False))
# code = parseAST(ast)
# print(code.instructions)
# code = parseAST(Sequence(seq=[FuncDec(name=Function(name='f'), params=[Variable(name='a'), Variable(name='b'), Variable(name='c')], body=Sequence(seq=[AssignOp(operator='<-', left=Variable(name='d'), right=MathOp(operator='+', left=MathOp(operator='+', left=Variable(name='a'), right=Variable(name='b')), right=Variable(name='c')))], inloop=False), returns=Variable(name='d')), AssignOp(operator='<-', left=Variable(name='e'), right=FuncCall(name=Function(name='f'), args=[Int(value=1), Int(value=2), Int(value=3)]))], inloop=False))
# pprint(code.instructions)
# code = parseAST(Sequence(seq=[LogOp(operator='xnor', right=Int(value=1), left=Int(value=2))], inloop=False))

# print(code.instructions)