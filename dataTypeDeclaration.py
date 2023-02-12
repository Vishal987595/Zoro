from dataclasses import dataclass
from fractions import Fraction
from typing import List, Mapping, Tuple



############################################################# DataTypes

@dataclass
class Frac:
    value: Fraction
    def __init__(self, *args) -> None:
        self.value = Fraction(*args)

@dataclass
class String:
    value: str
    def __init__(self, *args) -> None:
        self.value = str(*args)

@dataclass
class Float:
    value: float
    def __init__(self, *args) -> None:
        self.value = float(*args)

@dataclass
class Int:
    value: int
    def __init__(self, *args) -> None:
        self.value = int(*args)

@dataclass
class Bool:
    value: bool
    def __init__(self, *args) -> None:
        self.value = bool(*args)

############################################################# Operators

@dataclass
class Operator:
    op: str

@dataclass
class BinOp:
    operator: str
    left: 'AST'
    right: 'AST'

@dataclass
class MathOp:
    operator: str
    left: 'AST'
    right: 'AST'

@dataclass
class CndOp:
    operator: str
    left: 'AST'
    right: 'AST'

@dataclass
class UnOp:
    operator: str
    right: 'AST'

@dataclass
class BitOp:
    operator: str
    right: 'AST'
    left: 'AST'

############################################################# Identifier Classes

@dataclass
class Variable:
    name: str

############################################################# Keywords Constructs

@dataclass
class Let:
    var: 'AST'
    e1: 'AST'
    e2: 'AST'

@dataclass
class If:
    con: List['AST']
    seq: List['AST']

@dataclass
class While:
    cond: 'AST'
    body: 'AST'

@dataclass
class For:
    var: Variable
    list: list()

@dataclass
class Sequence:
    seq: List['AST']

@dataclass
class Assign:
    operator: str
    left: 'AST'
    right: 'AST'

############################################################# Identifier Constructs

@dataclass
class Identifier:
    word: str

@dataclass
class Keyword:
    word: str






############################################################################################################################


AST = Frac | BinOp | Variable | Let | If | UnOp | Assign | Sequence | MathOp | CndOp | BitOp | For

Value = Fraction | bool | int | float | None

Token = Int | Bool | Keyword | Identifier | Operator


############################################################################################################################


keywords = "if then else end while do done".split()
symbolic_operators = "+ - × / < > ≤ ≥ = ≠".split()
word_operators = "and or not quot rem".split()
whitespace = " \t\n"


############################################################################################################################
