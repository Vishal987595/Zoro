from dataclasses import dataclass
from dataTypeDeclaration import *
from lexer import *


# Our variable and function name's regex
import re
Name_regex = "^[_a-zA-z][a-zA-Z0-9_]*$" 


# Exception Classes
class Invalid_Syntax_VAR_KW: pass
class Invalid_Variable_Name: pass
class UnExpected_Token: pass




#############################################################################################################################
#############################################################################################################################





@dataclass
class ApnaParser:
    lexer: Lexer

    def from_lexer(lexer): 
        return ApnaParser(lexer)
    

    #############################################################################################################################


    def parse_BASE(self): 
        return self.parse_rassi()

    def parse_name(self):
        name = self.lexer.peek_token(); 
        if(name in keywords): 
            raise Invalid_Syntax_VAR_KW
        elif(re.match(Name_regex, name) == None ):
            raise Invalid_Variable_Name
        else:
            self.lexer.advance(); 
            return Variable(name); 

    def parse_expr(self):
        match self.lexer.peek_token():
            case Operator("-"): return self.parse_neg()
            case Operator("~"): return self.parse_bnot()
            case Keyword("not"): return self.parse_lnot()
            case Keyword("fun"): return self.parse_fun()
            case Keyword("if"): return self.parse_if()
            case _: return self.parse_BASE()

    def parse_atom(self):
        match self.lexer.peek_token():
            case Int(value):        
                self.lexer.advance(); 
                return Int(value); 
            case Float(value):      
                self.lexer.advance(); 
                return Float(value); 
            case Frac(value):       
                self.lexer.advance(); 
                return Frac(value); 
            case Bool(value):       
                self.lexer.advance(); 
                return Bool(value); 
            
            case Identifier(name): 
                if(name in keywords): 
                    self.lexer.advance(); 
                    return Keyword(name); 
                else: 
                    return self.parse_name(); 


    #############################################################################################################################


    def parse_exp(self):
        left = self.parse_atom()
        while True:
            match self.lexer.peek_token():
                case Operator("**"):
                    self.lexer.advance()
                    m = self.parse_exp()
                    # m = self.parse_atom()
                    left = MathOp("**", left, m)
                case _: break
        return left

    def parse_neg(self):
        while True:
            match self.lexer.peek_token():
                case Operator("-"):
                    self.lexer.advance()
                    # return -(self.parse_expr())
                    return UnOp("-",self.parse_expr())
                case _:	
                    return self.parse_exp()

    def parse_mul(self):
        left = self.parse_neg()
        while True:
            match self.lexer.peek_token():
                case Operator(op) if op in (" * / // % ".split()):
                    self.lexer.advance()
                    m = self.parse_atom()
                    left = MathOp(op, left, m)
                case _: break
        return left

    def parse_add(self):
        left = self.parse_mul()
        while True:
            match self.lexer.peek_token():
                case Operator(op) if op in (" + - ".split()):
                    self.lexer.advance()
                    m = self.parse_mul()
                    left = MathOp(op, left, m)
                case _: break
        return left

    def parse_shift(self):
        left = self.parse_add()
        while True:
            match self.lexer.peek_token():
                case Operator(op) if op in (" >> << ".split()):
                    self.lexer.advance()
                    m = self.parse_atom()
                    left = BitOp(op, left, m)
                case _: break
        return left

    def parse_bnot(self):
        while True:
            match self.lexer.peek_token():
                case Operator("~"):
                    self.lexer.advance()
                    # return ~(self.parse_expr())
                    return UnOp("~",self.parse_expr())
                case _:	
                    return self.parse_shift()

    def parse_band(self):
        left = self.parse_bnot()
        while True:
            match self.lexer.peek_token():
                case Operator("&"):
                    self.lexer.advance()
                    m = self.parse_bnot()
                    left = BitOp("&", left, m)
                case _: break
        return left

    def parse_bxor(self):
        left = self.parse_band()
        while True:
            match self.lexer.peek_token():
                case Operator("^"):
                    self.lexer.advance()
                    m = self.parse_band()
                    left = BitOp("^", left, m)
                case _: break
        return left

    def parse_bor(self):
        left = self.parse_bxor()
        while True:
            match self.lexer.peek_token():
                case Operator("|"):
                    self.lexer.advance()
                    m = self.parse_bxor()
                    left = BitOp("|", left, m)
                case _: break
        return left

    def parse_cmp(self):
        left = self.parse_bor()
        match self.lexer.peek_token():
            case Operator(op) if op in (" < > <= >= == != ".split()):
                self.lexer.advance()
                right = self.parse_bor()
                return CndOp(op, left, right)
        return left

    def parse_lnot(self):
        left = self.parse_cmp()
        while True:
            match self.lexer.peek_token():
                case Keyword("not"):
                    self.lexer.advance()
                    m = self.parse_cmp()
                    left = LogOp("not", left, m)
                case _: break
        return left

    def parse_lnand(self):
        left = self.parse_lnot()
        while True:
            match self.lexer.peek_token():
                case Keyword("nand"):
                    self.lexer.advance()
                    m = self.parse_lnot()
                    left = LogOp("nand", left, m)
                case _: break
        return left

    def parse_land(self):
        left = self.parse_lnand()
        while True:
            match self.lexer.peek_token():
                case Keyword("and"):
                    self.lexer.advance()
                    m = self.parse_lnand()
                    left = LogOp("and", left, m)
                case _: break
        return left

    def parse_lxnor(self):
        left = self.parse_land()
        while True:
            match self.lexer.peek_token():
                case Keyword("xnor"):
                    self.lexer.advance()
                    m = self.parse_land()
                    left = LogOp("xnor", left, m)
                case _: break
        return left

    def parse_lxor(self):
        left = self.parse_lxnor()
        while True:
            match self.lexer.peek_token():
                case Keyword("xor"):
                    self.lexer.advance()
                    m = self.parse_lxnor()
                    left = LogOp("xor", left, m)
                case _: break
        return left

    def parse_lnor(self):
        left = self.parse_lxor()
        while True:
            match self.lexer.peek_token():
                case Keyword("nor"):
                    self.lexer.advance()
                    m = self.parse_lxor()
                    left = LogOp("nor", left, m)
                case _: break
        return left

    def parse_lor(self):
        left = self.parse_lnor()
        while True:
            match self.lexer.peek_token():
                case Keyword("or"):
                    self.lexer.advance()
                    m = self.parse_lnor()
                    left = LogOp("or", left, m)
                case _: break
        return left

    def parse_lassi(self):
        left = self.parse_name()
        match self.lexer.peek_token():
            case Operator("<-"):
                self.lexer.advance()
                m = self.parse_lor()
                left = AssignOp("<-", left, m)
        return left

    def parse_rassi(self):
        left = self.parse_lor()
        match self.lexer.peek_token():
            case Operator("->"):
                self.lexer.advance()
                m = self.parse_name()
                right = AssignOp("->", left, m)
                return right
        return left


    #############################################################################################################################


    def parse_fun(self):
        params = []
        body = []
        returns = []

        self.lexer.match(Keyword("fun"))
        fun_name = self.parse_name()
        self.lexer.match(Keyword("of"))

        while True:
            match self.lexer.peek_token():
                case Keyword("is"):
                    break
                case _:
                    param = self.parse_name()
                    params.append(param)

        self.lexer.match(Keyword("is"))

        while True:
            match self.lexer.peek_token():
                case Keyword("returns"):
                    break
                case _:
                    expr = self.parse_expr()
                    body.append(expr)

        self.lexer.match(Keyword("returns"))

        while True:
            match self.lexer.peek_token():
                case Keyword("endfun"):
                    break
                case _:
                    ret_var = self.parse_expr()
                    returns.append(ret_var)

        self.lexer.match(Keyword("endfun"))

        return fun_name, params, body, returns


    def parse_if(self):
        conds=[]
        bodies=[]

        self.lexer.match(Keyword("if"))
        cond = self.parse_expr()
        conds.append(cond)

        self.lexer.match(Keyword("then"))
        curr_seq=[]
        while True:
            match self.lexer.peek_token():
                case Keyword("elif"):
                    break
                case Keyword("else"):
                    break
                case _:
                    expr = self.parse_expr()
                    curr_seq.append(expr)
        bodies.append(curr_seq)

        while True:
            match self.lexer.peek_token():
                case Keyword("elif"):
                    self.lexer.match(Keyword("elif"))
                    cond = self.parse_expr()
                    conds.append(cond)
                    self.lexer.match(Keyword("then"))

                    curr_seq=[]
                    while True:
                        match self.lexer.peek_token():
                            case Keyword("elif"):
                                break
                            case Keyword("else"):
                                break
                            case _:
                                expr = self.parse_expr()
                                curr_seq.append(expr)
                    bodies.append(curr_seq)

                case Keyword("else"):
                    self.lexer.match(Keyword("else"))
                    
                    curr_seq=[]
                    while True:
                        match self.lexer.peek_token():
                            case Keyword("endif"):
                                break
                            case _:
                                expr = self.parse_expr()
                                curr_seq.append(expr)
                    bodies.append(curr_seq)

                    self.lexer.match(Keyword("endif"))
                    break

                case _:
                    raise UnExpected_Token
        
        return If(conds,bodies)


    def parse_while(self): 
        pass # """TO BE COMPLETED"""


    def parse_for(self): 
        pass # """TO BE COMPLETED"""






#############################################################################################################################
#############################################################################################################################
#############################################################################################################################





print("\n")

def test_parse():
    def parse(string): 
        return ApnaParser.parse_expr( 
                    ApnaParser.from_lexer( 
                            Lexer.from_stream( Stream.from_string(string) ) ) )

    # print(parse("a"))
    # print(parse("m*6*b"))
    # print(parse("this_vAr1_is_var <= 2"))
    # print(parse("_this_vAr1_is_var <= 2"))
    # print(parse("1+2**6-8//4+7/9"))
    # print(parse("a**5-9<<<1^6+~a**6 >= m&6%4/5//8-6+!2"))
    # print(parse("a**5**6**k"))

# test_parse()

print("\n")







#############################################################################################################################
#############################################################################################################################



'''

import re
var_pattern = "^[_a-zA-z][a-zA-Z0-9_]*$" 
x = re.match(var_pattern, str) 


unary: ! - ~ 
arithmetic: + - * / // % ** 
comparison: > < >= <= == !=  
shift: >> << 
logical : and or not xor xnor nand nor 
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

