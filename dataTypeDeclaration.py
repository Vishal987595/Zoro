from dataclasses import dataclass
from fractions import Fraction
from typing import List



################################################################## DataTypes ##################################################################

@dataclass
class Frac:
    value: Fraction
    def __init__(self, value, *args) -> None:
        self.value = Fraction(value)

@dataclass
class String:
    value: str
    def __init__(self, value, *args) -> None:
        self.value = str(value)

@dataclass
class Float:
    value: float
    def __init__(self, value, *args) -> None:
        self.value = float(value)

@dataclass
class Int:
    value: int
    def __init__(self, value, *args) -> None:
        self.value = int(value)

@dataclass
class Bool:
    value: bool
    def __init__(self, value, *args) -> None:
        self.value = bool(value)

@dataclass
class Symbol:
    sym : str

@dataclass
class Get:
    var: 'AST'

@dataclass
class Put:
    var: 'AST'
    e1: 'AST'

################################################################## Operators ##################################################################

@dataclass
class Operator:
    op: str

@dataclass
class UnOp:
    operator: str
    right: 'AST'

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
class BitOp:
    operator: str
    right: 'AST'
    left: 'AST'

@dataclass
class LogOp:
    operator: str
    right: 'AST'
    left: 'AST'

@dataclass
class AssignOp:
    operator: str
    left: 'AST'
    right: 'AST'

@dataclass
class UpdateOp:
    operator: str
    left: 'AST'
    right: 'AST'

@dataclass
class StringOp:
    operator: str
    args: List['AST']

############################################################# Identifier Classes #############################################################

@dataclass
class Variable:
    name: str

@dataclass
class Function:
    name: str

############################################################ Data Structures #############################################################

@dataclass
class List_:
    items:  List['AST']

############################################################ Keywords Constructs #############################################################

@dataclass
class Sequence:
    seq: List['AST']

@dataclass
class For:
    var: Variable
    iter: List_
    seq: Sequence

@dataclass
class While:
    cnd: 'AST'
    seq: Sequence

@dataclass
class Let:
    var: 'AST'
    e1: 'AST'
    e2: 'AST'

@dataclass
class If:
    con: List['AST']
    seq: List[Sequence]
        
@dataclass
class Print:
    contents: List['AST']

@dataclass
class FuncDec:
    name: str
    params: List[Variable]
    body: Sequence
    returns: 'AST'

@dataclass
class FuncCall:
    name: str
    args: List['AST'] 

############################################################ Data Structures Operators #############################################################

@dataclass
class ListOp:
    operator: str
    list: List['AST']
    item: 'AST' 
    index: 'AST'

########################################################### Identifier Constructs ############################################################

@dataclass
class Identifier:
    word: str

@dataclass
class Keyword:
    word: str






###############################################################################################################################################


AST = Int | Float | Bool | String | Frac | Symbol    |    Operator | BinOp | MathOp | CndOp | UnOp | BitOp | AssignOp | StringOp    |    Variable | Let | If | Sequence    | Print | FuncDec 

Token = Int | Float | Bool | String | Frac | Symbol    |    Operator | BinOp | MathOp | CndOp | UnOp | BitOp | AssignOp | StringOp     |     Let | If     | Print


Value = Fraction | bool | int | float | str | None 


###############################################################################################################################################


keywords = "   if then elif else endif    let    Int Float String Bool Frac   ".split()

symbolic_operators = "  + - * / // % **    < <= => > == !=    >> <<    ~ & | ^     <- ->  ".split()

word_operators = " and or not xor xnor nand nor ".split()           # Logical Operators

whitespace = "\t \n".split() + [' ']


###############################################################################################################################################
