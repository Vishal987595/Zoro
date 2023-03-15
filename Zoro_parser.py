##################################### THIS IS NEW PARSER.PY , INDEPENDENT OF LEXER.PY #####################################

from pprint import pprint
from dataclasses import dataclass
from dataTypeDeclaration import *
from lexer import *

# Our regex for variable and function names
import re
Name_regex = "^[_a-zA-z][a-zA-Z0-9_]*$"

# Exception Classes : These all are compile time errors
class Invalid_Syntax_VAR_KW(Exception): pass # VarN cant be KW name
class Invalid_Variable_Name(Exception): pass # doesnt satisfy regex
class UnExpected_Token(Exception): pass # The construct is inapproprite
class Expected_ParamsArgs_After_OF(Exception): pass # since u've used "of" KW, must pass atleast one param
class Cannot_Assign_to_an_Expr(Exception): pass # Assi must be done to a location in memory
class Expected_A_Semicolon(Exception): pass # Missing Semicolon to end the stmt
class Invalid_Bracket_Character(Exception): pass # The encountered character cannot start a bracket type 
class Incorrect_Parantheses(Exception): pass # Paranthesis pairs are not matching


#############################################################################################################################
#############################################################################################################################



# A class for End of File / End of Tokens detection - EOF/EOT Object-Class
@dataclass
class EndOfFile: pass; 
EOF = EndOfFile(); 


@dataclass
class ZoroParser:
    
    def __init__(self, Program_Stream):
        # This type of thing needs to be implemented
        # Lexer_Object = Lexer(Program_Stream); 
        # self.Token_Seq = Lexer_Object.Token_Seq; 
        # pprint(self.Token_Seq); 

        self.Token_Seq = print_tokens(Program_Stream); 
        self.Token_Seq.append(EOF); 
        # print("\n\nTokens from Lexer", self.Token_Seq,"\n"); 
        self.n=len(self.Token_Seq); 
        self.nn=self.n-1; 
        self.pos=0; 
        self.Parsed_AST = self.parse_Program(); 
        # for i in self.Parsed_AST.seq: pprint(i); 
    
    def advance(self):                          # Moves the pointer to the immidiate next token
        # print("advancing", self.next_token()); 
        self.pos+=1; 
        return; 
    
    def retreat(self):                          # Moves the pointer to the immidiate previous token
        # print("retreating", self.next_token()); 
        self.pos-=1; 
        return; 

    def next_token(self):                       # Returns : First Upcoming Not-consumed token
        if(self.pos>=self.nn): 
            return EOF; 
        else: 
            return self.Token_Seq[self.pos]; 
        # Peeking at the beginning should return the first token

    def consume_token(self,expected_token):     # Consumes the next_token if it is the expected one
        if(self.next_token()==expected_token): 
            return self.advance(); 
        else: 
            raise UnExpected_Token; 
    



    #############################################################################################################################
    #############################################################################################################################


    def parse_name(self,name_flag):       # name_flag = {0:variable , 1:fun_dec_name , 2:fun_call}
        identifier = self.next_token();   # Identifier(word="actual_word")
        
        try: 
            name = identifier.word; 
        except: 
            # print("\nraise identifier.word --> ",identifier,"\n\n"); 
            raise UnExpected_Token; 
        
        if(name in keywords):
            # raise Invalid_Syntax_VAR_KW
            return self.retreat(); 
        elif(re.match(Name_regex,name) == None):
            raise Invalid_Variable_Name
            # return self.retreat(); 
        else:
            if(name_flag==0):
                self.advance(); 
                if(self.next_token()==Keyword("of")):
                    self.retreat(); 
                    return self.parse_fun_call(); 
                else:
                    return Variable(name); 
            elif(name_flag==1):
                self.advance(); 
                return Function(name); 


    def parse_atom(self):
        match (self.next_token()):   # Int(n=k) => Int & value=k  ; where k is actual number from the program 
            case Int(value):
                self.advance(); 
                return Int(value); 
            case Float(value):
                self.advance(); 
                return Float(value); 
            case Frac(value):        # MAY NOT EVEN BE LEXED, IDK
                self.advance(); 
                return Frac(value); 
            case Bool(value):
                self.advance(); 
                return Bool(value); 
            case String(value):      # NOT YET LEXED
                self.advance(); 
                return String(value); 
            case _:
                return self.parse_name(name_flag=0); 


    #############################################################################################################################


    def parse_power(self):
        left = self.parse_atom()
        while True:
            match self.next_token():
                case (Symbol("(")):
                    self.parse_bracket()
                case (Symbol(")")):
                    return; 
                case Operator("**"):
                    self.advance()
                    right = self.parse_power()
                    left = MathOp("**", left, right)
                case _:
                    break
        return left
    def parse_neg_bnot_lnot(self):
        match self.next_token():
            case (Symbol("(")):
                self.parse_bracket()
            case (Symbol(")")):
                return; 
            case Operator(op) if op in ("- ~ not".split()):
                self.advance()
                right = self.parse_neg_bnot_lnot()
                left = UnOp(op, right)
                return left
            case _:	
                whole = self.parse_power()
                return whole
    def parse_mul(self):
        left = self.parse_neg_bnot_lnot()
        while True:
            match self.next_token():
                case (Symbol("(")):
                    self.parse_bracket()
                case (Symbol(")")):
                    return; 
                case Operator(op) if op in (" * / // % ".split()):
                    self.advance()
                    right = self.parse_neg_bnot_lnot()
                    left = MathOp(op, left, right)
                case _:
                    break
        return left
    def parse_add(self):
        left = self.parse_mul()
        while True:
            match self.next_token():
                case (Symbol("(")):
                    self.parse_bracket()
                case (Symbol(")")):
                    return; 
                case Operator(op) if op in (" + - ".split()):
                    self.advance()
                    right = self.parse_mul()
                    left = MathOp(op, left, right)
                case _:
                    break
        return left
    def parse_shift(self):
        left = self.parse_add()
        while True:
            match self.next_token():
                case (Symbol("(")):
                    self.parse_bracket()
                case (Symbol(")")):
                    return; 
                case Operator(op) if op in (" >> << ".split()):
                    self.advance()
                    right = self.parse_add()
                    left = BitOp(op, left, right)
                case _:
                    break
        return left
    def parse_band(self):
        left = self.parse_shift()
        while True:
            match self.next_token():
                case (Symbol("(")):
                    self.parse_bracket()
                case (Symbol(")")):
                    return; 
                case Operator("&"):
                    self.advance()
                    right = self.parse_shift()
                    left = BitOp("&", left, right)
                case _:
                    break
        return left
    def parse_bxor(self):
        left = self.parse_band()
        while True:
            match self.next_token():
                case (Symbol("(")):
                    self.parse_bracket()
                case (Symbol(")")):
                    return; 
                case Operator("^"):
                    self.advance()
                    right = self.parse_band()
                    left = BitOp("^", left, right)
                case _:
                    break
        return left
    def parse_bor(self):
        left = self.parse_bxor()
        while True:
            match self.next_token():
                case (Symbol("(")):
                    self.parse_bracket()
                case (Symbol(")")):
                    return; 
                case Operator("|"):
                    self.advance()
                    right = self.parse_bxor()
                    left = BitOp("|", left, right)
                case _:
                    break
        return left
    def parse_cmp(self):
        left = self.parse_bor()
        while True:
            match self.next_token():
                case (Symbol("(")):
                    self.parse_bracket()
                case (Symbol(")")):
                    return; 
                case Operator(op) if op in (" < > <= >= == != ".split()):
                    self.advance()
                    right = self.parse_bor()
                    left = CndOp(op, left, right)
                case _:
                    break
        return left
    def parse_lnand(self):
        left = self.parse_cmp()
        while True:
            match self.next_token():
                case (Symbol("(")):
                    self.parse_bracket()
                case (Symbol(")")):
                    return; 
                case Operator("nand"):
                    self.advance()
                    right = self.parse_cmp()
                    left = LogOp("nand", left, right)
                case _:
                    break
        return left
    def parse_land(self):
        left = self.parse_lnand()
        while True:
            match self.next_token():
                case (Symbol("(")):
                    self.parse_bracket()
                case (Symbol(")")):
                    return; 
                case Operator("and"):
                    self.advance()
                    right = self.parse_lnand()
                    left = LogOp("and", left, right)
                case _:
                    break
        return left
    def parse_lxnor(self):
        left = self.parse_land()
        while True:
            match self.next_token():
                case (Symbol("(")):
                    self.parse_bracket()
                case (Symbol(")")):
                    return; 
                case Operator("xnor"):
                    self.advance()
                    right = self.parse_land()
                    left = LogOp("xnor", left, right)
                case _:
                    break
        return left
    def parse_lxor(self):
        left = self.parse_lxnor()
        while True:
            match self.next_token():
                case (Symbol("(")):
                    self.parse_bracket()
                case (Symbol(")")):
                    return; 
                case Operator("xor"):
                    self.advance()
                    right = self.parse_lxnor()
                    left = LogOp("xor", left, right)
                case _:
                    break
        return left
    def parse_lnor(self):
        left = self.parse_lxor()
        while True:
            match self.next_token():
                case (Symbol("(")):
                    self.parse_bracket()
                case (Symbol(")")):
                    return; 
                case Operator("nor"):
                    self.advance()
                    right = self.parse_lxor()
                    left = LogOp("nor", left, right)
                case _:
                    break
        return left
    def parse_lor(self):
        match self.next_token():
            case (Symbol("(")):
                self.parse_bracket()
            case (Symbol(")")):
                return; 
            case (Symbol("[")):
                right = self.parse_list()
                return right
            case _:
                left = self.parse_lnor()
                while True:
                    match self.next_token():
                        case (Symbol("(")):
                            self.parse_bracket()
                        case (Symbol(")")):
                            return; 
                        case Operator("or"):
                            self.advance()
                            right = self.parse_lnor()
                            left = LogOp("or", left, right)
                        case _:
                            break
                return left
    
    def parse_lassi(self):          # TO BE DONE : ONLY WHEN "var" is used : Add a while loop 
        left = self.parse_lor() 
        match self.next_token():
            case Operator("<-"):
                if(type(left)!=Variable):
                    raise Cannot_Assign_to_an_Expr
                self.advance()
                right = self.parse_lor()
                left = AssignOp("<-", left, right)
            case (Symbol("[")):
                right = self.parse_list(); 
                return right; 
            case (Symbol("(")):
                self.parse_bracket()
            case (Symbol(")")):
                return; 
        return left

    def parse_rassi(self):          # TO BE DONE : Add a while loop
        left = self.parse_lassi(); 
        match self.next_token():
            case (Symbol("(")):
                self.parse_bracket()
            case (Symbol(")")):
                return; 
            case Operator("->"):
                self.advance()
                right = self.parse_lassi()
                # if(type(left)!=Variable): raise Cannot_Assign_to_an_Expr      # TO BE RESOLVED
                right = AssignOp("->", left, right)
                return right
        return left


    #############################################################################################################################

    def parse_list(self):
        self.consume_token(Symbol("[")); 
        args = []

        arg = self.parse_Expr()
        args.append(arg)
        while True:
            match self.next_token():
                case (Symbol("(")):
                    self.parse_bracket()
                case (Symbol(")")):
                    return; 
                case Symbol("]"):
                    break
                case _:
                    # self.consume_token(Symbol(","))
                    arg = self.parse_Expr()
                    args.append(arg)
        
        self.consume_token(Symbol("]"))
        return List_(args)

    def parse_bracket(self):
        match self.next_token():
            case Symbol("("):
                self.consume_token(Symbol("(")); 
                expr = self.parse_Expr(); 
                self.consume_token(Symbol(")")); 
                return expr; 
            case (Symbol(")")):
                return; 
            case _: 
                raise Invalid_Bracket_Character


    #############################################################################################################################


    def parse_Base(self):
        return self.parse_rassi(); 
    
    def parse_Expr(self):
        match self.next_token():
            case Keyword("fun"): return self.parse_fun_def(); 
            case Keyword("if"): return self.parse_if(); 
            case Keyword("for"): return self.parse_for(); 
            case Keyword("while"): return self.parse_while(); 
            case Keyword("print"): return self.parse_print(); 
            case (Symbol("[")): return self.parse_list(); 
            case (Symbol("(")): return self.parse_bracket(); 
            case (Symbol(")")): return; 
            case _:
                expr_only = self.parse_Base(); # self.debug_print()
                self.consume_token(Symbol(";"))
                return expr_only

    def parse_Program(self):
        final_instrs=[]; 
        while(self.next_token()!=EOF): final_instrs.append(self.parse_Expr()); #print("\n\n",Sequence(final_instrs),"\n\n")
        return Sequence(final_instrs); 



    #############################################################################################################################

    def parse_print(self):
        args = []; 
        self.consume_token(Keyword("print")); 

        arg = self.parse_Expr()
        args.append(arg)
        while True:
            match self.next_token():
                case Symbol("("):
                    self.parse_bracket()
                case (Symbol(")")):
                    return; 
                case Symbol(";"):
                    break
                case _:
                    arg = self.parse_Expr()
                    args.append(arg)

        self.consume_token(Symbol(";")); 
        return Print(args)

    def parse_fun_call(self):
        args = []
        fn_name = self.parse_name(name_flag=1); 

        if(self.next_token()==Keyword("of")):   # Only if fun had params defined in FuncDec
            self.consume_token(Keyword("of")); 
            
            arg = self.parse_Expr()
            args.append(arg)
            while True:
                match self.next_token():
                    case (Symbol("(")):
                        self.parse_bracket()
                    case (Symbol(")")):
                        return; 
                    case (Symbol(";")):
                        break
                    case _:
                        if(self.next_token()==Symbol(",")): self.consume_token(Symbol(","))
                        arg = self.parse_Expr()
                        args.append(arg)

        self.consume_token(Symbol(";"))
        return FuncCall(fn_name, (args))

    def parse_fun_def(self):
        params = []
        body = []
        # returns = []

        self.consume_token(Keyword("fun"))
        fn_name = self.parse_name(name_flag=1)

        if(self.next_token()==Keyword("of")):
            self.consume_token(Keyword("of"))
            
            if(self.next_token()==Keyword("is")): 
                raise Expected_ParamsArgs_After_OF
            else:
                param = self.parse_name(name_flag=0)
                params.append(param)
                while True:
                    match self.next_token():
                        case (Symbol("(")):
                            self.parse_bracket()
                        case (Symbol(")")):
                            return; 
                        case Keyword("is"):
                            break
                        case _:
                            if(self.next_token()==Symbol(",")): self.consume_token(Symbol(","))
                            param = self.parse_name(name_flag=0)
                            params.append(param)
        
        self.consume_token(Keyword("is"))

        while True:
            match self.next_token():
                case (Symbol("(")):
                    self.parse_bracket()
                case (Symbol(")")):
                    return; 
                case Keyword("returns"):
                    break
                case Keyword("endfun"):
                    break
                case _:
                    expr = self.parse_Expr()
                    body.append(expr)

        if(self.next_token()==Keyword("returns")):
            self.consume_token(Keyword("returns"))
            
            if self.next_token()==Keyword("endfun"):
                pass    # SHOULD RETURN NIL 
            else:
                returnable = self.parse_Expr()
                # returns.append(returnable)
                # while True:
                #     match self.next_token():
                #         case (Symbol("(")):
                #             self.parse_bracket()
                #         case (Symbol(")")):
                #             return; 
                #         case Keyword("endfun"):
                #             break
                #         case _:
                #             if(self.next_token()==Symbol(",")): self.consume_token(Symbol(","))
                #             returnable = self.parse_Expr()
                #             returns.append(returnable)
        
        self.consume_token(Keyword("endfun"))
        self.consume_token(Symbol(";"))

        return FuncDec(fn_name, params, Sequence(body), returnable)

    def parse_if(self):
        conds=[]
        bodies=[]
        
        self.consume_token(Keyword("if"))
        cond = self.parse_Expr()
        conds.append(cond)

        self.consume_token(Keyword("then"))
        curr_seq=[]
        while True:
            match self.next_token():
                case (Symbol("(")):
                    self.parse_bracket()
                case (Symbol(")")):
                    return; 
                case Keyword("elif"):
                    break
                case Keyword("else"):
                    break
                case Keyword("endif"):
                    break
                case _:
                    expr = self.parse_Expr()
                    curr_seq.append(expr)
        bodies.append(Sequence(curr_seq))
        
        if(self.next_token()==Keyword("elif")):
            while True:
                match self.next_token():
                    case (Symbol("(")):
                        self.parse_bracket()
                    case (Symbol(")")):
                        return; 
                    case Keyword("endif"): 
                        break
                    case Keyword("else"): 
                        break
                    case Keyword("elif"):
                        self.consume_token(Keyword("elif"))
                        cond = self.parse_Expr()
                        conds.append(cond)
                        self.consume_token(Keyword("then"))

                        curr_seq=[]
                        while True:
                            match self.next_token():
                                case (Symbol("(")):
                                    self.parse_bracket()
                                case (Symbol(")")):
                                    return; 
                                case Keyword("endif"): 
                                    break
                                case Keyword("elif"):
                                    break
                                case Keyword("else"):
                                    break
                                case _:
                                    expr = self.parse_Expr()
                                    curr_seq.append(expr)
                        bodies.append(Sequence(curr_seq))
        
        if(self.next_token()==Keyword("else")):
            self.consume_token(Keyword("else"))
            
            curr_seq=[]
            while True:
                match self.next_token():
                    case (Symbol("(")):
                        self.parse_bracket()
                    case (Symbol(")")):
                        return; 
                    case Keyword("endif"):
                        break
                    case _:
                        expr = self.parse_Expr()
                        curr_seq.append(expr)
            bodies.append(Sequence(curr_seq))

        self.consume_token(Keyword("endif"))
        self.consume_token(Symbol(";"))
        return If(conds,(bodies))

    def parse_while(self):
        body = []

        self.consume_token(Keyword("while"))
        cond = self.parse_Expr()
        self.consume_token(Keyword("do"))

        while True:
            match self.next_token():
                case (Symbol("(")):
                    self.parse_bracket()
                case (Symbol(")")):
                    return; 
                case Keyword("endwhile"):
                    break
                case _:
                    expr = self.parse_Expr()
                    body.append(expr)

        self.consume_token(Keyword("endwhile"))
        self.consume_token(Symbol(";"))
        return While(cond,Sequence(body))

    def parse_for(self):    # Only uni var iterates are allowed
        body = []

        self.consume_token(Keyword("for"))
        var = self.parse_name(name_flag=0)
        self.consume_token(Keyword("in"))
        
        if(self.next_token()==Symbol("[")):
            iterable = self.parse_list()
        else:
            iterable = self.parse_name(name_flag=0)
        
        self.consume_token(Keyword("do"))

        while True:
            match self.next_token():
                case (Symbol("(")):
                    self.parse_bracket()
                case (Symbol(")")):
                    return; 
                case Keyword("endfor"):
                    break
                case _:
                    expr = self.parse_Expr()
                    body.append(expr)

        self.consume_token(Keyword("endfor"))
        self.consume_token(Symbol(";"))
        return For(var,iterable,Sequence(body))

    def debug_print(self): print(f"\n (Pos , Next_Token)  =  ({self.pos} , {self.next_token()})"); 




#############################################################################################################################
#############################################################################################################################


def test_parse():
    print("\n")

    """ Valid Programs """
    if(1):  # APNE PROGRAMS
        # ZoroParser("fun fib of n is  a <- 0;  if n > 1;   then n1 <- n - 1;  b <- fib of n1;;;  n2 <- n - 2;  c <- fib of n2;;;  a <- b + c;  else a <- n;  endif;  returns a;  endfun;  print fib of 5;;;;")
        # ZoroParser(" fun f of n is if n>1; then b<-f of n-1;;; c<-b*n; else c<-1; endif; returns c; endfun;   print f of 4;;;; ")
        # ZoroParser("sum <- 0;  i <- 0;  while i<1000; do      if     i%3 == 0 or i%5 == 0;    then          sum <- sum + i;      endif;      i <- i + 1; print i; sum; ; endwhile;  print sum;;")
        # ZoroParser("fun isprime of n is b<-True; j<-2; while   j<n and b==True;   do if n%j==0; then b<-False; endif; j<-j+1; endwhile; print b;; returns b; endfun; print isprime of 13;;;;")     #N<-26; mp<-2; i<-2; while i<N; do   a<-isprime of i;;;    if     a==True and N%i==0;    then mp<-i; endif; i<-i+1; endwhile; print mp;; ")
        # ZoroParser("fun fib of n is a<-0; if n>1; then n1<-n-1; cc<-fib of n-1;;; dd<-fib of n-2;;; c ; a<-b+c; else a<-n; endif; returns a; endfun; y<-fib of 5; ; ; print y;; ")
        # ZoroParser("fun double of x is a<-2*x; returns a; endfun; a<-5; y <- double of a; ; ; ")
        # (ZoroParser("m1 <- 1000//3; s1 <- m1+1; s1 <- 3*s1*m1//2;  m2 <- 1000//5; s2 <- m2+1; s2 <- 5*s2*m2//2;  m3 <- 1000//15; s3 <- m3+1; s3 <- 15*s3*m3//2;  ans <- s1 + s2 - s3; print ans; ;"))
        # (ZoroParser("fun fib of n is a<-0; if n>1; then a<- ((fib of (n-1;)) + (fib of n-2;)) ; else a<-n; endif; returns a; endfun; print fib of 5; "))
        # ZoroParser(" list_name <- [1; 2; 5;] ; for i in list_name do k<-2; endfor; ")
        # ZoroParser("(a<-2;)")
        pass
    if(1):
        # (ZoroParser("True;"))
        # (ZoroParser("5;"))
        # (ZoroParser("7.68;"))
        # (ZoroParser( ' "This is abra kadabra string ! lOl ;) "; ' ))      ######### TO DOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
        pass
    if(1):
        # (ZoroParser("____ ;"))
        # (ZoroParser("this_vAr1_is_var ;"))
        # (ZoroParser("____this_vAr1_is_var ;"))
        # (ZoroParser("_a <- 2 ;"))
        # (ZoroParser("1 -> _b ;"))
        pass
    if(1):
        # (ZoroParser("-----a ;"))
        # (ZoroParser("~~~~~a ;"))
        # (ZoroParser("not not not a ;"))
        # (ZoroParser("a**5**6**k ;"))
        # (ZoroParser("1+2**6-8//4+7/9 ;"))
        # (ZoroParser("a**5-9<<1^6+a**6 >= m&6%4/5//7--~not-8-6+2 ;"))
        # (ZoroParser("a**b-c<<d*z-y^e+f**g >= m&h%k/i//j-m+n ;"))
        pass
    if(1):
        # (ZoroParser("if c>0; then b<-2; endif ;"))
        # (ZoroParser("if c>0; then b<-2; else c->d; endif ;"))
        # (ZoroParser("if c>0; then b<-2; elif k<k; then l>5 endif ;"))
        # (ZoroParser("if c>0; then b<-2; elif k<k; then l>l; elif pl^u; then I_5; endif ;"))
        # (ZoroParser("if c>0; then b<-2;  elif    m % n >= k ^ l ;   then pika else c->d; endif ;"))
        # (ZoroParser("if c>0; then b<-2; elif k<k then l>l; elif pl^u; then I_5; else c->d; endif ;"))
        pass
    if(1):
        # (ZoroParser("while c>=0; do a<-2; endwhile ;"))
        pass
    if(1):
        # (ZoroParser("for i in list_name do k<-2; endfor ;"))
        # (ZoroParser("for i in [ 2; , 6; , var; ] do k<-2; endfor ;"))      ######### TO DOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
        pass
    if(1):
        # (ZoroParser("fun myfun is a<-2; endfun ;"))
        # (ZoroParser("fun myfun is a<-2; returns b endfun ;"))
        # (ZoroParser("fun myfun of a,b is a<-2; endfun ;"))
        # (ZoroParser("fun myfun of a,b is a<-2; returns b endfun ;"))
        # (ZoroParser("fun fn_nm of a,b c is a<-b+c; returns a b,c endfun ;"))

        # (ZoroParser("myfun of myvar_one myvar_two,myvar_three ;"))
        pass
    if(1):
        # (ZoroParser("print (myvar_one myvar_two, myvar_three); "))
        pass
    if(1):
        # (ZoroParser("a<2; b<-5; c->3; "))
        # (ZoroParser("if (;) then a<-2 ; b<5; else I_have<6; endif;"))
        pass

    """ Invalid Programs """    ######### TO DOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    if(1):
        # (ZoroParser(";"))
        # (ZoroParser("#"))
        # (ZoroParser("__#__"))
        # (ZoroParser("_this_85_#_65_ad_"))
        # (ZoroParser(' 59.54 ^ invalid"This is abra kadabra string !  lOl ;) "    Dont%This '))
        pass

    print("\n")
# test_parse()

#############################################################################################################################
#############################################################################################################################



'''

Our Variable/Function names rules :

    import re
    var_pattern = "^[_a-zA-z][a-zA-Z0-9_]*$" 
    x = re.match(var_pattern, str) 

    

Allowed operators and their classes

    unary: - ~ 
    arithmetic: + - * / // % ** 
    comparison: > < >= <= == !=  
    shift: >> << 
    logical : and or not xor xnor nand nor 
    bitwise: ~ & | ^ 
    assignment: <- -> 

    

Our language's Grammar

    atom = dtypes | var_name | expr 

    Initiate = atom | fun_dec | fun_call | if_elif_else | while_loop | for_loop

    exp = atom | atom**exp 
    neg_bnot_lnot = exp | -neg_bnot_lnot | ~neg_bnot_lnot | not neg_bnot_lnot
    mul = neg | mul * neg | mul / neg | mul // neg | mul % neg 
    add = mul | add + mul | add - mul 

    shift = add | add >> shift | add << shift 
    band = shift | shift & band 
    bxor = band | band ^ bxor 
    bor = bxor | "bxor | bor "

    comp = bor | bor < bor | bor > bor | bor <= bor | bor >= bor | bor == bor | bor != bor  

    lnand = comp | comp "nand" lnand 
    land = lnand | lnand "and" land 
    lxnor = land | land "xnor" lxnor 
    lxor = lxnor | lxnor "xor" lxor 
    lnor = lxor | lxor "nor" lnor 
    lor = lnor | lnor "or" lor 

    assi = var <- lor | lor -> var 

    Body = expr* 
    Cond = expr 
    List = var_name | "[" (ASTs,)* "]" 

    fun_dec = "fun" fn_name ["of" (params,)*] is Body [returns (returnables,)*] 
    fun_call = fn_name ["of" (args,)*] 
    if_elif_else = "if" Cond "then" Body ("elif" Cond "then" Body)* [else Body] "endif" 
    while_loop = "while" Cond "do" Body "endwhile" 
    for_loop = "for" var_name "in" List "do" Body "endfor" 
    
'''
