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


AST = NumLiteral | BinOp | Variable | If | UnOp

Value = Fraction | bool | None

class InvalidProgram(Exception): pass


def eval(program: AST, environment: Mapping[str, Value] = None) -> Value:
    if environment is None:
        environment = {}
    match program:
        case NumLiteral(value):
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
        case BinOp("<-", left, right):
            v = eval(right, environment)
            left.value = v
            environment[left.value] = v
            return None
    raise InvalidProgram()

def test_comp_eval():
    a = NumLiteral(1)
    b = NumLiteral(2)
    c = NumLiteral(3)
    d = NumLiteral(4)

    assert eval( BinOp (">=", c, c) )
    assert eval( BinOp ("<", a, d) )

    eval(BinOp ("<-", d, NumLiteral(0)))
    assert (d.value == 0)
    
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
    
test_comp_eval()
test_unop_if()
