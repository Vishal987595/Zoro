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
class Null:
    value: None

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
    left: 'AST'
    right: 'AST'

@dataclass
class LogOp:
    operator: str
    left: 'AST'
    right: 'AST'

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
class Identifier:
    word: str

@dataclass
class Keyword:
    word: str

@dataclass
class Variable:
    name: str

@dataclass
class Let:
    var: 'AST'
    e1: 'AST'
    e2: 'AST'


############################################################ Data Structures #############################################################

@dataclass
class List_:
    items:  List['AST']

@dataclass
class ListOp:
    list: List_ | Variable
    operator: str
    item: 'AST' 
    index: 'AST'


############################################################ Keyword Statements #############################################################

@dataclass
class Print:
    contents: List['AST']

@dataclass
class Sequence:
    seq: List['AST']
    inloop : bool = False


@dataclass
class If:
    con: List['AST']
    seq: List[Sequence]

@dataclass
class While:
    cnd: 'AST'
    seq: Sequence

@dataclass
class For:
    var: Variable
    iter: List_
    seq: Sequence

@dataclass
class Range:
    num1: Int
    num2: Int
    jmp: Int | Null


@dataclass
class FuncDec:
    name: str
    params: List[Variable]
    body: Sequence

@dataclass
class FuncCall:
    name: str
    args: List['AST'] 

@dataclass
class Function:
    name: str

@dataclass
class Returns:
    value: 'AST'

@dataclass
class Break:
    pass




###############################################################################################################################################


AST = Int | Float | Bool | String | Frac | Null | Symbol    |    Operator | BinOp | MathOp | CndOp | UnOp | BitOp | AssignOp | UpdateOp | StringOp | ListOp    |    Returns | FuncDec | FuncCall | If | While | For | List_ | Range | Print | Sequence | Break   |    Variable | Identifier | Keyword

Token = Int | Float | Bool | String | Frac | Symbol    |    Operator | BinOp | MathOp | CndOp | UnOp | BitOp | AssignOp | StringOp     |     If | Print


Value = Fraction | bool | int | float | str | None 


###############################################################################################################################################


keywords = " Int Float Frac Bool String    var   if then elif else endif    print    fun of is returns endfun   while do endwhile   for in endfor break  concat   len push pop insert count ".split()

symbolic_operators = "  + - * / // % **    < <= => > == !=    >> <<    ~ & | ^     <- ->  ".split()

word_operators = " and or not xor xnor nand nor ".split()           # Logical Operators

brackets = " ( ) [ ] ".split()

whitespace = "\t \n".split() + [' ']


###############################################################################################################################################
