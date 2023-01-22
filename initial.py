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
class Variable:
    name: str


AST = NumLiteral | BinOp | Variable

Value = Fraction | bool | None

class InvalidProgram(Exception): pass


def eval(program: AST, environment: Mapping[str, Value] = None) -> Value:
    if environment is None:
        environment = {}
    match program:
        case NumLiteral(value):
            return value
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

    
test_comp_eval()
