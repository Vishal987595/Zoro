from dataclasses import dataclass
from fractions import Fraction
from typing import List, Mapping

@dataclass
class NumLiteral:
    value: Fraction
    def __init__(self, *args):
        self.value = Fraction(*args)

@dataclass
class BinOp:
    operator: str
    left: 'AST'
    right: 'AST'

@dataclass
class Let:
    var: 'AST'
    e1: 'AST'
    e2: 'AST'
        
@dataclass
class If:
    e1: 'AST'
    c: 'AST'
    e2: 'AST'
        
@dataclass
class UnOp:
    op: str
    right: 'AST'

@dataclass
class Variable:
    name: str

@dataclass
class Mut:
    name: str
    value: 'AST'



AST = NumLiteral | BinOp | Variable | Let | If | UnOp | Mut

Value = Fraction | bool | None

class InvalidProgram(Exception): pass

def eval(program: AST, environment: Mapping[str, Value] = None) -> Value:
    if environment is None:
        environment = {}
    match program:
        case NumLiteral(value):
            return value
        case Variable(name):
            if name in environment:
                return environment[name]
            raise InvalidProgram()
        case Let(Variable(name), e1, e2):
            v1 = eval(e1, environment)
            return eval(e2, environment | { name: v1 })
        case Mut(name, value):
            environment[name] = value
            return value
        case If(e1, c, e2):
            if eval(c, environment):
                return eval(e1, environment)
            else:
                return eval(e2, environment)
        case UnOp("-", right):
            return -1 * eval(right, environment)
        case UnOp("!", right):
            return not eval(right, environment)
        case UnOp("b!", right):
            return ~eval(right, environment)
        case BinOp(">", left, right):
            return eval(left, environment) > eval(right, environment)
        case BinOp("<", left, right):
            return eval(left, environment) < eval(right, environment)
        case BinOp("==", left, right):
            return eval(left, environment) == eval(right, environment)
        case BinOp("!=", left, right):
            return eval(left, environment) != eval(right, environment)
        case BinOp(">=", left, right):
            return eval(left, environment) >= eval(right, environment)
        case BinOp("<=", left, right):
            return eval(left, environment) <= eval(right, environment)
        case BinOp("+", left, right):
            return eval(left, environment) + eval(right, environment)
        case BinOp("-", left, right):
            return eval(left, environment) - eval(right, environment)
        case BinOp("*", left, right):
            return eval(left, environment) * eval(right, environment)
        case BinOp("/", left, right):
            if eval(right,environment) == 0:
                print("Division by Zero")
                raise InvalidProgram()
            return eval(left, environment) / eval(right, environment)
        case BinOp("exp", left, right):
            return eval(left, environment) ** eval(right, environment)
        case BinOp("%", left, right):
            if eval(right,environment) == 0:
                print("Division by Zero")
                raise InvalidProgram()
            return eval(left, environment) % eval(right, environment)
        case BinOp("i/", left, right):
            if eval(right,environment) == 0:
                print("Division by Zero")
                raise InvalidProgram()
            return eval(left, environment) // eval(right, environment)
        case BinOp("<-", left, right):
            v = eval(right, environment)
            left.value = v
            environment[left.name] = v
            return None
        case BinOp("|", left, right):
            return eval(left, environment) or eval(right, environment)
        case BinOp("&", left, right):
            return eval(left, environment) and eval(right, environment)
    raise InvalidProgram()

def test_comp_eval():
    a = NumLiteral(1)
    b = NumLiteral(2)
    c = NumLiteral(3)
    d = NumLiteral(4)

    assert eval( BinOp (">=", c, c) )
    assert eval( BinOp ("<", a, d) )

def test_let_eval():
    a  = Variable("a")
    e1 = NumLiteral(5)
    e2 = BinOp("+", a, a)
    e  = Let(a, e1, e2)
    assert eval(e) == 10
    e  = Let(a, e1, Let(a, e2, e2))
    assert eval(e) == 20
    e  = Let(a, e1, BinOp("+", a, Let(a, e2, e2)))
    assert eval(e) == 25
    e  = Let(a, e1, BinOp("+", Let(a, e2, e2), a))
    assert eval(e) == 25
    e3 = NumLiteral(6)
    e  = BinOp("+", Let(a, e1, e2), Let(a, e3, e2))
    assert eval(e) == 22

def test_unop_if():
    b = NumLiteral(5)
    e1 = NumLiteral(6)
    e2 = NumLiteral(4)
    c = BinOp(">", b, NumLiteral(7))
    e = If(e1, c, e2)
    assert eval(e) == 4
    g = BinOp("<=", b, NumLiteral(3))
    d = UnOp("!", g)
    f = If(e1, d, e2)
    assert eval(f) == 6
    
    g = NumLiteral(2)
    e3 = UnOp("-", g)
    assert eval(e3) == -2

def test_arithop_mut():
    a = NumLiteral(1)
    b = NumLiteral(2)
    c = NumLiteral(3)
    d = NumLiteral(4)
    e1 = BinOp("+", a, b)
    e2 = BinOp("*", c, d)
    e3 = BinOp("i/", e2, e1)
    assert eval(e3) == 4
    i = NumLiteral(1)
    j = NumLiteral(0)
    try:
        e4 = BinOp("/", i, j)
        x = eval(e4)
        print("hii")
    except InvalidProgram:
        print("An error was raised")

    k = Mut('k', 0)
    y = eval(BinOp('<-', k, NumLiteral(2)))
    assert k.value == 2

    
test_comp_eval()
test_let_eval()
test_unop_if()
test_arithop_mut()