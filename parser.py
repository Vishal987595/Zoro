from dataclasses import dataclass
from dataTypeDeclaration import *


@dataclass
class Stream:
    source: str
    pos: int

    def from_string(s): return Stream(s, 0)
    def next_char(self): 
        if self.pos >= len(self.source): raise EndOfStream()
        self.pos = self.pos + 1
        return self.source[self.pos - 1]
    def unget(self):
        assert self.pos > 0
        self.pos = self.pos - 1



@dataclass
class If:
    con: list['AST']
    seq: list['AST']
@dataclass
class WHILE:
    cond: 'AST'
    do: 'AST'   #Seq
@dataclass
class FOR:
    iter_var: MyMut
    lst: Mylist
    do: 'AST'   #Seq






@dataclass
class ApnaParser:
    lexer: Lexer 

    def from_lexer(lexer): return ApnaParser(lexer)
    
    def parse_var(self):
        pass
    
    def parse_expr(self):
        match self.lexer.peek_token():
            case Keyword("if"): return self.parse_if()
            case Keyword("while"): return self.parse_while()
            case Keyword("for"): return self.parse_for()
            case Operator("-"): return self.parse_neg()
            case _: return self.parse_BASE()

    def parse_if(self):
        conds=[]; seqs=[]; 
        self.lexer.match(Keyword("if"))
        cond = self.parse_expr()
        conds.append(cond)
        self.lexer.match(Keyword("then"))
        seq = self.parse_expr()
        seqs.append(seq)

        while True:
            match self.lexer.peek_token():
                case Keyword("elif"):
                    self.lexer.match(Keyword("elif"))
                    cond = self.parse_expr()
                    conds.append(cond)
                    self.lexer.match(Keyword("then"))
                    seq = self.parse_expr()
                    seqs.append(seq)

                case Keyword("else"):
                    self.lexer.match(Keyword("else"))
                    seq = self.parse_expr()
                    seqs.append(seq)
                    self.lexer.match(Keyword("endif"))
                    break
        
        """ ############## typecheck ############### """
        return If(conds,seqs)

    def parse_while(self):
        self.lexer.match(Keyword("while")); 
        cond = self.parse_expr(); 
        self.lexer.match(Keyword("do")); 
        do = self.parse_expr(); 
        self.lexer.match(Keyword("endwhile")); 
        """ ############## typecheck ############### """
        return WHILE(cond,do); 

    def parse_for(self):
        self.lexer.match(Keyword("for")); 
        iter_var = self.parse_expr(); 
        self.lexer.match(Keyword(":")); 
        lst = self.parse_expr(); 
        self.lexer.match(Keyword("do")); 
        do = self.parse_expr(); 
        self.lexer.match(Keyword("endfor")); 
        """ ############## typecheck ############### """
        return FOR(iter_var,lst,do); 

    def parse_BASE(self): 
        return self.parse_rassi()




'''

import re
var_pattern = "^[_a-zA-z][a-zA-Z0-9_]*$" 
x = re.match(var_pattern, str) 

unary: not - ~ 
arithmetic: + - * / // % ** 
comparison: > < >= <= == !=  
shift: >> << and or ! xor xnor nand nor 
bitwise: ~ & | ^ 
assignment: <- -> 

Literals = dtypes 
atom = Literals | var_pattern | expr 

exp = atom | atom**exp 
neg = exp | -neg 
mul = neg | mul * neg | mul / neg | mul // neg | mul % neg 
add = mul | add + mul | add - mul 

shift = add | add >> shift | add << shift 
bnot = shift | ~bnot 
band = bnot | bnot & band 
bxor = band | band ^ bxor 
bor = bxor | "bxor | bor "

comp = bor | bor < bor | bor > bor | bor <= bor | bor >= bor | bor == bor | bor != bor  

lnot = comp | not(lnot) 
lnand = lnot | lnot "nand" lnand 
land = lnand | lnand "and" land 
lxnor = land | land "xnor" lxnor 
lxor = lxnor | lxnor "xor" lxor 
lnor = lxor | lxor "nor" lnor 
lor = lnor | lnor "or" lor 

assi = var <- lor | lor -> var 

'''
