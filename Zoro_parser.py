import numpy as np
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
class Expected_Params_Between_OF_and_IS(Exception): pass # since u've used "of" KW, must pass atleast one param
class Cannot_Assign_to_an_Expr(Exception): pass # Assi must be done to a location in memory
class Expected_A_Semicolon(Exception): pass # Missing Semicolon to end the stmt
class Invalid_Bracket_Character(Exception): pass # The encountered character cannot start a bracket type 
class Incorrect_Bracket_Sequence(Exception): pass # Paranthesis pairs are not matching
class Not_Enough_Closing_Brackets(Exception): pass # Add missing closing brackets properly
class Not_Enough_Opening_Brackets(Exception): pass # Add missing closing brackets properly
class Inappropriate_Type_of_Token(Exception): pass # if(type(var)!=Token_Type)
class Returns_Not_Allowed_Here(Exception): pass # Do not allow 'returns' ouside fun_def
class Invalid_Character_Inside_Brackets(Exception): pass # Inside parse_brackets unreachable case
class Returns_Not_Allowed_Here(Exception): pass # Do not allow 'returns' ouside fun_def
class Not_A_Basic_Datatype(Exception): pass # After "var", only Int,Float etc are allowed
class Inappropriate_No_of_Eles(Exception): pass # Noof eles in array does not meet declared


#############################################################################################################################
#############################################################################################################################

@dataclass
class Brkt_Stk_Cls:

    def __init__(self) -> None:
        self.stack = [] 
    def push(self,pushie):
        self.stack.append(pushie) 
    def pop(self,popie):
        self.check_not_empty()

        match popie:
            case Symbol(")"):
                if(self.stack[-1]==Symbol("(")): 
                    self.stack.pop(-1)
                else: 
                    raise Incorrect_Bracket_Sequence
                    self.comp_err("Incorrect_Bracket_Sequence","Brackets are too entagled as if they're your fingers!", self.Line_Numbers[self.Curr_Token_Index])
                    quit()
            case Symbol("]"):
                if(self.stack[-1]==Symbol("[")): 
                    self.stack.pop(-1)
                else: 
                    raise Incorrect_Bracket_Sequence
                    self.comp_err("Incorrect_Bracket_Sequence","Brackets are too entagled as if they're your fingers!", self.Line_Numbers[self.Curr_Token_Index])
                    quit()
            case Symbol("}"):
                if(self.stack[-1]==Symbol("{")): 
                    self.stack.pop(-1)
                else: 
                    raise Incorrect_Bracket_Sequence
                    self.comp_err("Incorrect_Bracket_Sequence","Remove the Brackets are too entagled as if they're your fingers!", self.Line_Numbers[self.Curr_Token_Index])
                    quit()

    def check_empty(self):
        if(len(self.stack)>0): 
            raise Not_Enough_Closing_Brackets
            self.comp_err("Not_Enough_Closing_Brackets","Please add some closing brackets to match the leading ones.", self.Line_Numbers[self.Curr_Token_Index])
            quit()
    def check_not_empty(self):
        if(len(self.stack)==0): 
            raise Not_Enough_Opening_Brackets
            self.comp_err("Not_Enough_Opening_Brackets","Please add some opening brackets to match the trailing ones.", self.Line_Numbers[self.Curr_Token_Index])
            quit()


# A class for End of File / End of Tokens detection - EOF/EOT Object-Class
@dataclass
class EndOfFile: pass
EOF = EndOfFile()

@dataclass
class ZoroParser:


    def __init__(self, Program_Stream):

        self.Token_Seq, self.Line_Numbers = print_tokens(Program_Stream); 
        self.Token_Seq.append(EOF)
        # print("\n\nTokens from Lexer", self.Token_Seq,"\n")

        self.n = len(self.Token_Seq)
        self.nn = self.n-1
        self.pos = 0
        self.Curr_Token_Index = 0

        self.inside_fun_def = False
        self.array_init_flag = False
        self.array_init_type = None
        self.array_init_length = None
        self.Parsed_AST = self.parse_Program()

        # for i in self.Parsed_AST.seq: pprint(i); 
    def advance(self):                          # Moves the pointer to the immidiate next token
        # print("advancing", self.next_token()); 
        self.pos += 1
        self.Curr_Token_Index += 1
        return
    def retreat(self):                          # Moves the pointer to the immidiate previous token
        # print("retreating", self.next_token()); 
        self.pos-=1
        self.Curr_Token_Index -= 1
        return
    def next_token(self):                       # Returns : First Upcoming Not-consumed token
        if(self.pos>=self.nn): 
            return EOF
        else: 
            return self.Token_Seq[self.pos]
        # Peeking at the beginning should return the first token
    def prev_token(self):                       # Returns : The last (most recent) consumed token
        if(self.pos==0): 
            return None
        else: 
            return self.Token_Seq[self.pos-1]
        # Peeking at the beginning should return None
    def consume_token(self, expected_token):    # Consumes the next_token if it is the expected one
        current_token = self.next_token()
        if(current_token==expected_token): 
            self.Curr_Token_Index += 1
            return self.advance()
        else:
            print(f"Parse Error : Expected : {expected_token} , but got : {current_token} //")
            raise UnExpected_Token
            self.comp_err("Invalid Syntax",f"I think you should spend your remaining life remembering the syntax of Zoro!", self.Line_Numbers[self.Curr_Token_Index])
            quit()
    def comp_err(self,cate,msg,line):           # Prints the error to the user
        print(f"\nCOMPILE TIME ERROR ENCOUNTERED : In line number {line} : as follows :")
        print(cate,"::",msg,"\n")


    #############################################################################################################################
    #############################################################################################################################


    def parse_name(self,name_flag):     # Parses_Regex ; name_flag = {0:variable , 1:fun_dec_name , 2:fun_call}
        identifier = self.next_token(); # Identifier(word="actual_word")
        # print("---> INSIDE PARSE NAME",end=' '); self.debug_print(); 
        
        try: 
            name = identifier.word; 
        except:
            print("\nRAISED IN PARSE NAME : ",identifier,"DOESN'T'VE WORD ATTR\n\n"); 
            raise UnExpected_Token; 
            self.comp_err("Invalid Syntax",f"Your mind, logic and the token '{identifier}' you used, are all the same, at the wrong place!", self.Line_Numbers[self.Curr_Token_Index])
            quit()
        
        if(name in keywords):
            return self.retreat()
            # raise Invalid_Syntax_VAR_KW
            # self.comp_err("Invalid_Syntax_VAR_KW","THIS_NEEDS_TO_BE_FILLED_IN_LATER", self.Line_Numbers[self.Curr_Token_Index])
            # quit()
        
        elif(re.match(Name_regex,name) == None):
            raise Invalid_Variable_Name
            self.comp_err("Invalid_Variable_Name",f"The varibale you named '{name}' is, just like you, invalid!", self.Line_Numbers[self.Curr_Token_Index])
            quit()
        
        else:
            if(name_flag==0):
                self.advance()
                if(self.next_token()==Keyword("of")):
                    self.retreat()
                    return self.parse_fun_call()
                else:
                    if(self.next_token()==Symbol(".")):
                        self.consume_token(Symbol("."))
                        if(self.next_token().word in " push pop len insert count index at update ".split()):
                            r1,r2,r3 = self.parse_list_fx()
                            return ListOp(Variable(name) , r1,r2,r3)
                        elif(self.next_token().word in " strlen concat slice locate count_char ".split()):
                            r1,r2 = self.parse_String_fx()
                            return StringOp(r1,[Variable(name),r2])
                        else:
                            raise UnExpected_Token
                            self.comp_err("UnExpected_Token"," . [Dot] k baad apna dimaag mat laga, valid operator laga.", self.Line_Numbers[self.Curr_Token_Index])
                            quit()
                    else:
                        return Variable(name)
            elif(name_flag==1):
                self.advance()
                return Function(name)


    def parse_atom(self):               # Parses Basic DTypes
        match (self.next_token()):
            case Int(value):
                self.advance(); 
                return Int(value); 
            case Float(value):
                self.advance(); 
                return Float(value); 
            case Frac(value):
                self.advance(); 
                return Frac(value); 
            case Bool(value):
                self.advance(); 
                return Bool(value); 
            
            case String(value):
                self.advance(); 
                if(self.next_token()==Symbol(".")):
                    self.consume_token(Symbol("."))
                    r1,r2 = self.parse_String_fx()
                    # if(type(r2)!=Null):
                    return StringOp(r1,[String(value),r2])
                    # else:
                    #     return StringOp(r1,[String(value)])
                return String(value); 
            case _:
                return self.parse_name(name_flag=0); 


    #############################################################################################################################


    def parse_power(self):
        left = self.parse_atom()
        while True:
            match self.next_token():
                case (Symbol("(")):
                    return self.parse_bracket()
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
                return self.parse_bracket()
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
                    return self.parse_bracket()
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
                    return self.parse_bracket()
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
                    return self.parse_bracket()
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
                    return self.parse_bracket()
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
                    return self.parse_bracket()
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
                    return self.parse_bracket()
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
                    return self.parse_bracket()
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
                    return self.parse_bracket()
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
                    return self.parse_bracket()
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
                    return self.parse_bracket()
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
                    return self.parse_bracket()
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
                    return self.parse_bracket()
                case Operator("nor"):
                    self.advance()
                    right = self.parse_lxor()
                    left = LogOp("nor", left, right)
                case _:
                    break
        return left
    def parse_lor(self,real_expr_flag):
        match self.next_token():
            case (Keyword("range")):
                return self.parse_range()
            # case (Symbol("(")):
            #     return self.parse_bracket()
            case (Symbol("[")):
                right = self.parse_list()
                return right
            case _:
                if(self.next_token()==Symbol("(") and real_expr_flag!=True): 
                    return self.parse_bracket()
                left = self.parse_lnor()
                while True:
                    match self.next_token():
                        case (Symbol("(")):
                            return self.parse_bracket()
                        case Operator("or"):
                            self.advance()
                            right = self.parse_lnor()
                            left = LogOp("or", left, right)
                        case _:
                            break
                return left
    def parse_assis_upds(self,real_expr_flag):     #TODO
        assign_flag = False
        num = None
        dtype = None                # SHOULD BE NULL(None)

        if(self.next_token()==Keyword("var")):
            self.consume_token(Keyword("var"))
            assign_flag = True

            match self.next_token():
                case Keyword("Int"):
                    self.consume_token(Keyword("Int"))
                    dtype = Int(0)
                case Keyword("Float"):
                    self.consume_token(Keyword("Float"))
                    dtype = Float(0.0)
                case Keyword("Frac"):
                    self.consume_token(Keyword("Frac"))
                    dtype = Frac(0/1)
                case Keyword("String"):
                    self.consume_token(Keyword("String"))
                    dtype = String("")
                case Keyword("Bool"):
                    self.consume_token(Keyword("Bool"))
                    dtype = Bool(False)
                case Keyword("Null"):
                    self.consume_token(Keyword("Null"))
                    dtype = Null(None)
                case Identifier(word):
                    pass
                case _:
                    raise Not_A_Basic_Datatype
                    self.comp_err("Not_A_Basic_Datatype","You know (even if you don't) that you can only write basic dtypes, why are you writing your intelligence, which is invalid here?", self.Line_Numbers[self.Curr_Token_Index])
                    quit()
        
        if(assign_flag==True):
            # left = self.parse_lor(real_expr_flag)
            left = self.parse_name(name_flag=0)
            if(type(left)!=Variable): 
                raise Cannot_Assign_to_an_Expr
                self.comp_err("Cannot_Assign_to_an_Expr","Shabash Beta! Expression me store karke bohot aage badhega.", self.Line_Numbers[self.Curr_Token_Index])
                quit()
            
            if(self.next_token()==Symbol("[")):
                self.consume_token(Symbol("["))
                num = self.next_token()
                if(not(type(num)==Int or type(num)==Variable or type(num)==Identifier)):
                    raise Inappropriate_Type_of_Token
                    self.comp_err("Inappropriate_Type_of_Token","Only Int is allowed as var[num]. ", self.Line_Numbers[self.Curr_Token_Index])
                    quit()
                self.advance()
                self.consume_token(Symbol("]"))

                self.array_init_flag = True
                self.array_init_type = dtype
                self.array_init_length = num.value

            self.consume_token(Operator("<-"))
            right = self.parse_lor(real_expr_flag)

            self.array_init_flag = False
            self.array_init_type = None
            self.array_init_length = None
            return AssignOp("<-", left, right, dtype)

        elif(assign_flag==False):
            left = self.parse_lor(real_expr_flag)

            if(self.next_token()==Operator("<-")):
                if(type(left)!=Variable): 
                    raise Cannot_Assign_to_an_Expr
                    self.comp_err("Cannot_Assign_to_an_Expr","Shabash Beta! Expression me store karke bohot aage badhega.", self.Line_Numbers[self.Curr_Token_Index])
                    quit()
                self.consume_token(Operator("<-"))
                right = self.parse_lor(real_expr_flag)
                return UpdateOp("<-", left, right)
            
            elif(self.next_token()==Operator("->")):
                self.consume_token(Operator("->"))

                if(self.next_token()==Keyword("var")):
                    self.consume_token(Keyword("var"))
                    assign_flag = True
                    
                    match self.next_token():
                        case Keyword("Int"):
                            self.consume_token(Keyword("Int"))
                            dtype = Int(0)
                        case Keyword("Float"):
                            self.consume_token(Keyword("Float"))
                            dtype = Float(0.0)
                        case Keyword("Frac"):
                            self.consume_token(Keyword("Frac"))
                            dtype = Frac(0/1)
                        case Keyword("String"):
                            self.consume_token(Keyword("String"))
                            dtype = String("")
                        case Keyword("Bool"):
                            self.consume_token(Keyword("Bool"))
                            dtype = Bool(False)
                        case Keyword("Null"):
                            self.consume_token(Keyword("Null"))
                            dtype = Null(None)
                        case Identifier(word):
                            pass
                        case _:
                            raise Not_A_Basic_Datatype
                            self.comp_err("Not_A_Basic_Datatype","You know (even if you don't) that you can only write basic dtypes, why are you writing your intelligence, which is invalid here?", self.Line_Numbers[self.Curr_Token_Index])
                            quit()
                
                # right = self.parse_lor(real_expr_flag)
                right = self.parse_name(name_flag=0)
                if(type(right)!=Variable): 
                    raise Cannot_Assign_to_an_Expr
                    self.comp_err("Cannot_Assign_to_an_Expr","Shabash Beta! Expression me store karke bohot aage badhega.", self.Line_Numbers[self.Curr_Token_Index])
                    quit()

                if(self.next_token()==Symbol("[")):
                    self.consume_token(Symbol("["))
                    num = self.next_token()
                    if(type(num)!=Int):
                        raise Inappropriate_Type_of_Token
                        self.comp_err("Inappropriate_Type_of_Token","Only Int is allowed as var[num]. ", self.Line_Numbers[self.Curr_Token_Index])
                        quit()
                    self.advance()
                    self.consume_token(Symbol("]"))
                
                    self.array_init_flag = True
                    self.array_init_type = dtype
                    self.array_init_length = num.value
                
                self.array_init_flag = False
                self.array_init_type = None
                self.array_init_length = None
                
                if(assign_flag==True):
                    return AssignOp("->", left, right, dtype)
                elif(assign_flag==False):
                    return UpdateOp("->", left, right)
            
            return left


    
    #############################################################################################################################

    def parse_Expr(self, real_expr_flag=True, inloop=False):
        # print("-> Inside PARSE_EXPR")
        match self.next_token():
            case Keyword("fun"): return self.parse_fun_def(); 
            case Keyword("if"): return self.parse_if(inloop=inloop); 
            case Keyword("for"): return self.parse_for(); 
            case Keyword("while"): return self.parse_while(); 
            case Keyword("print"): return self.parse_print(); 
            case Keyword("range"): return self.parse_range(); 
            case Keyword("returns"): return self.parse_returns(); 
            case (Symbol("[")): return self.parse_list(); 
            case _:
                if(self.next_token()==Symbol("(") and real_expr_flag!=True): 
                    return self.parse_bracket()
                expr_only = self.parse_assis_upds(real_expr_flag); 
                if(real_expr_flag==True):
                    self.consume_token(Symbol(";"))
                return expr_only

    def parse_Program(self):    # Program refers to the sequence of instuctions, must followed by an EOF token! 
        final_instrs=[]; self.brkt_stk_obj = Brkt_Stk_Cls(); 
        while(self.next_token()!=EOF): final_instrs.append(self.parse_Expr()); 
        # print("\n\n",Sequence(final_instrs),"\n\n")
        self.brkt_stk_obj.check_empty()
        
        assert self.inside_fun_def == False
        assert self.array_init_flag == False
        assert self.array_init_type == None
        assert self.array_init_length == None

        return Sequence(final_instrs)



    #############################################################################################################################

    def parse_bracket(self):
        #print("--> Inside parse_bracket"); self.debug_print(); 
        match self.next_token():
            case Symbol("("):
                sub_seq=[]
                self.consume_token(Symbol("(")); self.brkt_stk_obj.push(Symbol("(")); #print("Consumed OPENING BRACKET"); 
                expr = self.parse_Expr(real_expr_flag=False); sub_seq.append(expr); 
                while(True):
                    match self.next_token():
                        case Symbol(")"):
                            break
                        case Symbol(","):
                            self.consume_token(Symbol(","))
                            expr = self.parse_Expr(real_expr_flag=False); sub_seq.append(expr); 
                        case _ :
                            raise Invalid_Character_Inside_Brackets
                            self.comp_err("Invalid_Character_Inside_Brackets","Why you must use something so offendin' as a separator?", self.Line_Numbers[self.Curr_Token_Index])
                            quit()
                self.consume_token(Symbol(")")); self.brkt_stk_obj.pop(Symbol(")")); #print("Consumed CLOSING BRACKET"); print("sub_seq",sub_seq); 

                if(len(sub_seq)==1):
                    return sub_seq[0]; 
                else: 
                    return Sequence(sub_seq); 
            case _: 
                raise Invalid_Bracket_Character
                self.comp_err("Invalid_Bracket_Character","Bhai (not sorry if you aren't)! You created a new bracter character. Well Done! Indeed! Just one thing : Go and write it in your own language, Not Here!", self.Line_Numbers[self.Curr_Token_Index])
                quit()

    def parse_range(self):
        self.consume_token(Keyword("range")); 
        r1 = self.parse_Expr(real_expr_flag=False); 
        self.consume_token(Symbol(",")); 
        r2 = self.parse_Expr(real_expr_flag=False); 
        if(self.next_token()==Symbol(",")):
            self.consume_token(Symbol(",")); 
            r3 = self.parse_Expr(real_expr_flag=False); 
        else:
            r3 = Int(value=1)
        return List_([Int(i) for i in list(range(r1.value, r2.value, r3.value))])

    def parse_list(self):
        self.consume_token(Symbol("["))
        args = []

        if(self.next_token()!=Symbol("]")):
            if(self.array_init_flag==True):     # Parse an array
                
                len_args = 0
                arg = self.parse_Expr(real_expr_flag=False)
                if(self.array_init_type!=None and type(arg)!=type(self.array_init_type)):
                    raise Inappropriate_Type_of_Token
                    self.comp_err("Inappropriate_Type_of_Token","Only Int is allowed as var[num]. ", self.Line_Numbers[self.Curr_Token_Index])
                    quit()
                args.append(arg)
                len_args += 1

                while True:
                    match self.next_token():
                        case (Symbol("(")):
                            return self.parse_bracket()
                        case Symbol("]"):
                            break
                        case _:
                            self.consume_token(Symbol(","))
                            arg = self.parse_Expr(real_expr_flag=False)
                            if(self.array_init_type!=None and type(arg)!=type(self.array_init_type)):
                                raise Inappropriate_Type_of_Token
                                self.comp_err("Inappropriate_Type_of_Token","Only Int is allowed as var[num]. ", self.Line_Numbers[self.Curr_Token_Index])
                                quit()
                            args.append(arg)
                            len_args += 1
                
                diff_args_len = self.array_init_length - len_args
                if(diff_args_len<0):
                    raise Inappropriate_No_of_Eles
                    self.comp_err("Inappropriate_No_of_Eles","Abey. Declare length kuch aur hai and inserted length kuch aur. Kya kar rha hai bina dimaag lagaye?", self.Line_Numbers[self.Curr_Token_Index])
                    quit()
                elif(diff_args_len>0):
                    match self.array_init_type:
                        case Int(value):
                            args += [Int(0)] * (diff_args_len)
                        case Float(value):
                            args += [Float(0.0)] * (diff_args_len)
                        case Frac(value):
                            args += [Frac(0/1)] * (diff_args_len)
                        case String(value):
                            args += [String("")] * (diff_args_len)
                        case Bool(value):
                            args += [Bool(False)] * (diff_args_len)
                        case Null(value):
                            args += [Null(None)] * (diff_args_len)
                        case _:
                            print("Invalid")
                
                self.array_init_flag = False
                self.array_init_type = None

            else:   # Parse a list
                arg = self.parse_Expr(real_expr_flag=False)
                args.append(arg)
                while True:
                    match self.next_token():
                        case (Symbol("(")):
                            return self.parse_bracket()
                        case Symbol("]"):
                            break
                        case _:
                            self.consume_token(Symbol(","))
                            arg = self.parse_Expr(real_expr_flag=False)
                            args.append(arg)
            
        self.consume_token(Symbol("]"))

        if(self.array_init_flag==True):
            args=np.array(args,dtype=type(self.array_init_type))
        
        if(self.next_token()==Symbol(".")):
            self.consume_token(Symbol("."))
            r1,r2,r3 = self.parse_list_fx()
            return ListOp(List_(args) , r1,r2,r3)

        return List_(args)

    def parse_list_fx(self):
        match self.next_token():
            case Keyword("len"):
                self.consume_token(Keyword("len"))
                return "len", Null(None), Null(None)
            case Keyword("push"):
                self.consume_token(Keyword("push"))
                return "push", self.parse_Expr(real_expr_flag=False), Null(None)
            case Keyword("pop"):
                self.consume_token(Keyword("pop"))
                index = self.parse_Expr(real_expr_flag=False)
                if(type(index) != Int):
                    raise Inappropriate_Type_of_Token
                    self.comp_err("Inappropriate_Type_of_Token","Waah! Index ko Int hona chahiye ye bhi nhi pata tuze.", self.Line_Numbers[self.Curr_Token_Index])
                    quit()
                return "pop", Null(None), index
            case Keyword("insert"):
                self.consume_token(Keyword("insert"))
                item = self.parse_Expr(real_expr_flag=False)
                index = self.parse_Expr(real_expr_flag=False)
                if(type(index) != Int):
                    raise Inappropriate_Type_of_Token
                    self.comp_err("Inappropriate_Type_of_Token","Waah! Index ko Int hona chahiye ye bhi nhi pata tuze.", self.Line_Numbers[self.Curr_Token_Index])
                    quit()
                return "insert", item, index
            case Keyword("update"):
                self.consume_token(Keyword("update"))
                item = self.parse_Expr(real_expr_flag=False)
                index = self.parse_Expr(real_expr_flag=False)
                if(not(type(index)==Int or type(index)==Variable or type(index)==Identifier)):
                    raise Inappropriate_Type_of_Token
                    self.comp_err("Inappropriate_Type_of_Token","Waah! Index ko Int hona chahiye ye bhi nhi pata tuze.", self.Line_Numbers[self.Curr_Token_Index])
                    quit()
                return "update", item, index
            case Keyword("index"):
                self.consume_token(Keyword("index"))
                return "index", self.parse_Expr(real_expr_flag=False), Null(None)
            case Keyword("at"):
                self.consume_token(Keyword("at"))
                return "at", Null(None), self.parse_Expr(real_expr_flag=False)
            case Keyword("count"):
                self.consume_token(Keyword("count"))
                return "count", self.parse_Expr(real_expr_flag=False), Null(None)
            case _:
                raise UnExpected_Token
                self.comp_err("Invalid Syntax","Pata nhi konse naye functions bina banaye use karta rehta hai.", self.Line_Numbers[self.Curr_Token_Index])
                quit()

    def parse_String_fx(self):
        match self.next_token():
            case Keyword("strlen"):
                self.consume_token(Keyword("strlen"))
                return "strlen", Null(None)
            case Keyword("concat"):
                self.consume_token(Keyword("concat"))
                arg = self.parse_Expr(real_expr_flag=False)
                if(not(type(arg)==String or type(arg)==Variable)):
                    raise Inappropriate_Type_of_Token
                    self.comp_err("Inappropriate_Type_of_Token","String ko String ke saath concatnate karte hai, kam-akal. Pata nhi kya sikha itne saalo mein.", self.Line_Numbers[self.Curr_Token_Index])
                    quit()
                return "concat", arg
            case Keyword("slice"):
                self.consume_token(Keyword("slice"))
                ll = self.parse_Expr(real_expr_flag=False)
                rl = self.parse_Expr(real_expr_flag=False)
                
                if(not( (type(ll)==Int or type(ll)==Variable) and (type(rl)==Int or type(rl)==Variable) )):
                    raise Inappropriate_Type_of_Token
                    self.comp_err("Inappropriate_Type_of_Token","Waah! Index ko Int hona chahiye ye bhi nhi pata tuze.", self.Line_Numbers[self.Curr_Token_Index])
                    quit()
                return "slice", (ll, rl)
            case Keyword("locate"):
                self.consume_token(Keyword("locate"))
                arg = self.parse_Expr(real_expr_flag=False)
                return "locate", arg
            case Keyword("count_char"):
                self.consume_token(Keyword("count_char"))
                arg = self.parse_Expr(real_expr_flag=False)
                return "count_char", arg
            case _:
                raise UnExpected_Token
                self.comp_err("Invalid Syntax","Pata nhi konse naye functions bina banaye use karta rehta hai.", self.Line_Numbers[self.Curr_Token_Index])
                quit()



    #############################################################################################################################

    def parse_print(self):
        args = []
        self.consume_token(Keyword("print"))
        arg = self.parse_Expr(real_expr_flag=False)
        args.append(arg)
        while True:
            match self.next_token():
                case (Symbol("(")):
                    return self.parse_bracket()
                case (Symbol(";")):
                    break
                case _:
                    self.consume_token(Symbol(","))
                    arg = self.parse_Expr(real_expr_flag=False)
                    args.append(arg)
        
        self.consume_token(Symbol(";"))
        return Print(args)

    def parse_fun_call(self):
        args = []
        fn_name = self.parse_name(name_flag=1)

        if(self.next_token()==Keyword("of")):   # Only if fun had params defined in FuncDec
            self.consume_token(Keyword("of"))
            
            arg = self.parse_Expr(real_expr_flag=False)
            args.append(arg)
            while True:
                match self.next_token():
                    case (Symbol("(")):
                        return self.parse_bracket()
                    case (Symbol(";")):
                        break
                    case _:
                        self.consume_token(Symbol(","))
                        arg = self.parse_Expr(real_expr_flag=False)
                        args.append(arg)

        # self.consume_token(Symbol(";")); 
        return FuncCall(fn_name, (args))

    def parse_returns(self):
        if(self.inside_fun_def==False):
            raise Returns_Not_Allowed_Here
            self.comp_err("Returns_Not_Allowed_Here","What an imagination you have, to use 'returns' keyword outside of a function-definition. Hats off genius!", self.Line_Numbers[self.Curr_Token_Index])
            quit()
        
        self.consume_token(Keyword("returns"))

        if(self.next_token()!=Symbol(";")):
            returnable = self.parse_Expr(real_expr_flag=False)
        else:
            returnable = Null(None)
        
        self.consume_token(Symbol(";"))
        return Returns(returnable)

    def parse_fun_def(self):
        assert self.inside_fun_def == False
        self.inside_fun_def = True
        params = []
        body = []

        self.consume_token(Keyword("fun"))
        fn_name = self.parse_name(name_flag=1)

        if(self.next_token()==Keyword("of")):
            self.consume_token(Keyword("of"))
            
            if(self.next_token()==Keyword("is")): 
                raise Expected_Params_Between_OF_and_IS
                self.comp_err("Expected_Params_Between_OF_and_IS","Kya socha, function-definition me 'is' and 'of' k bich me parameters me apne aap daal dunga?!", self.Line_Numbers[self.Curr_Token_Index])
                quit()
            else:
                param = self.parse_name(name_flag=0)
                params.append(param)
                while True:
                    match self.next_token():
                        case (Symbol("(")):
                            return self.parse_bracket()
                        case Keyword("is"):
                            break
                        case _:
                            self.consume_token(Symbol(","))
                            param = self.parse_name(name_flag=0)
                            params.append(param)
        
        self.consume_token(Keyword("is"))

        while True:
            match self.next_token():
                case (Symbol("(")):
                    return self.parse_bracket()
                case Keyword("endfun"):
                    break
                case _:
                    expr = self.parse_Expr()
                    body.append(expr)
        
        self.consume_token(Keyword("endfun"))
        self.consume_token(Symbol(";"))

        assert self.inside_fun_def == True
        self.inside_fun_def = False
        return FuncDec(fn_name, params, Sequence(body))

    def parse_if(self, inloop=False):
        conds=[]
        bodies=[]
        
        self.consume_token(Keyword("if"))
        cond = self.parse_Expr(real_expr_flag=False)
        conds.append(cond)

        self.consume_token(Keyword("then"))
        curr_seq=[]
        while True:
            match self.next_token():
                case (Symbol("(")):
                    return self.parse_bracket()
                case Keyword("elif"):
                    break
                case Keyword("else"):
                    break
                case Keyword("endif"):
                    break
                case Keyword("break"):
                    curr_seq.append(Keyword("break"))
                    self.consume_token(Keyword("break"))
                    self.consume_token(Symbol(";"))
                case _:
                    expr = self.parse_Expr()
                    curr_seq.append(expr)
        bodies.append(Sequence(curr_seq, inloop=inloop))
        
        if(self.next_token()==Keyword("elif")):
            while True:
                match self.next_token():
                    case (Symbol("(")):
                        return self.parse_bracket()
                    case Keyword("endif"): 
                        break
                    case Keyword("else"): 
                        break
                    case Keyword("elif"):
                        self.consume_token(Keyword("elif"))
                        cond = self.parse_Expr(real_expr_flag=False)
                        conds.append(cond)
                        self.consume_token(Keyword("then"))

                        curr_seq=[]
                        while True:
                            match self.next_token():
                                case (Symbol("(")):
                                    return self.parse_bracket()
                                case Keyword("endif"): 
                                    break
                                case Keyword("elif"):
                                    break
                                case Keyword("else"):
                                    break
                                case Keyword("break"):
                                    curr_seq.append(Keyword("break"))
                                    self.consume_token(Keyword("break"))
                                    self.consume_token(Symbol(";"))
                                case _:
                                    expr = self.parse_Expr()
                                    curr_seq.append(expr)
                        bodies.append(Sequence(curr_seq, inloop=inloop))
        
        if(self.next_token()==Keyword("else")):
            self.consume_token(Keyword("else"))
            
            curr_seq=[]
            while True:
                match self.next_token():
                    case (Symbol("(")):
                        return self.parse_bracket()
                    case Keyword("endif"):
                        break
                    case Keyword("break"):
                        curr_seq.append(Keyword("break"))
                        self.consume_token(Keyword("break"))
                        self.consume_token(Symbol(";"))
                    case _:
                        expr = self.parse_Expr()
                        curr_seq.append(expr)
            bodies.append(Sequence(curr_seq, inloop=inloop))

        self.consume_token(Keyword("endif"))
        self.consume_token(Symbol(";"))
        return If(conds,(bodies))

    def parse_while(self):
        body = []

        self.consume_token(Keyword("while"))
        cond = self.parse_Expr(real_expr_flag=False, inloop=True)
        self.consume_token(Keyword("do"))

        while True:
            match self.next_token():
                case (Symbol("(")):
                    return self.parse_bracket()
                case Keyword("endwhile"):
                    break
                case Keyword("break"):
                    body.append(Keyword("break"))
                    self.consume_token(Keyword("break"))
                    self.consume_token(Symbol(";"))
                case _:
                    expr = self.parse_Expr(inloop=True)
                    body.append(expr)

        self.consume_token(Keyword("endwhile"))
        self.consume_token(Symbol(";"))
        return While(cond,Sequence(body, inloop=True))

    def parse_for(self):    # Only uni var iterates are allowed
        body = []

        self.consume_token(Keyword("for"))
        var = self.parse_name(name_flag=0)
        self.consume_token(Keyword("in"))
        
        if(self.next_token()==Symbol("[")):
            iterable = self.parse_list()
        elif(self.next_token()==Keyword("range")):
            iterable = self.parse_range()
        else:
            iterable = self.parse_name(name_flag=0)
        
        self.consume_token(Keyword("do"))

        while True:
            match self.next_token():
                case (Symbol("(")):
                    return self.parse_bracket()
                case Keyword("endfor"):
                    break
                case Keyword("break"):
                    body.append(Keyword("break"))
                    self.consume_token(Keyword("break"))
                    self.consume_token(Symbol(";"))
                case _:
                    expr = self.parse_Expr(inloop=True)
                    body.append(expr)

        self.consume_token(Keyword("endfor"))
        self.consume_token(Symbol(";"))
        return For(var,iterable,Sequence(body, inloop=True))

    def debug_print(self): print(f"(Pos , Next_Token)     =     ({self.pos} , {self.next_token()})")




#############################################################################################################################
#############################################################################################################################


def test_parse():       # Uncomment testcases one-by-one to test
    print("\n")

    """ Valid Programs """
    if(1):      # Basic Datatypes
        # (ZoroParser("True;"))
        # (ZoroParser("5;"))
        # (ZoroParser("7.68;"))
        # (ZoroParser( ' "This is abra kadabra string ! lOl ;) "; ' ))
        # (ZoroParser("____ ;"))
        # (ZoroParser("this_vAr1_is_var ;"))
        # (ZoroParser("____this_vAr1_is_var ;"))
        pass
    if(1):      # Assi Upd
        # (ZoroParser("var Int a <- 2 ;"))
        # (ZoroParser("1 -> var Float b ;"))
        # (ZoroParser("var _a <- 2 ;"))
        # (ZoroParser("1 -> var _b ;"))
        # (ZoroParser("_a <- 2 ;"))
        # (ZoroParser("1 -> _b ;"))
        pass
    if(1):      # Arithmetics
        # (ZoroParser("-----a ;"))
        # (ZoroParser("~~~~~a ;"))
        # (ZoroParser("not not not a ;"))
        # (ZoroParser("a**5**6**k ;"))
        # (ZoroParser("1+2**6-8//4+7/9 ;"))
        # (ZoroParser("a**5-9<<1^6+a**6 >= m&6%4/5//7--~not-8-6+2 ;"))
        # (ZoroParser("a**b-c<<d*z-y^e+f**g >= m&h%k/i//j-m+n ;"))
        pass
    if(1):      # If statement
        # (ZoroParser("if c>0 then b<-2; endif ;"))
        # (ZoroParser("if c>0 then b<-2; else c->d; endif ;"))
        # (ZoroParser("if c>0 then b<-2; elif k<k then l>5; endif ;"))
        # (ZoroParser("if c>0 then b<-2; elif k<k then l>l; elif pl^u then I_5; endif ;"))
        # (ZoroParser("if c>0 then b<-2; elif k<k then pka; else c->d; endif ;"))
        # (ZoroParser("if c>0 then b<-2; elif k<k then l>l; elif pl^u then I_5; else c->d; endif ;"))
        pass
    if(1):      # while & for - loops statements
        # (ZoroParser("while c>=0 do a<-2; b<-5; endwhile ;"))
        # (ZoroParser("for i in list_name do k<-2; a<-a+1; endfor ;"))
        # (ZoroParser("for i in [ 2 , 6 , alpha ] do k<-2;a<-a+1; endfor ;"))
        pass
    if(1):      # fun_def & returns statements
        # (ZoroParser("fun myfun is a<-2; endfun ;"))
        # (ZoroParser("fun myfun is returns; endfun ;"))
        # (ZoroParser("fun myfun is returns 3; endfun ;"))
        # (ZoroParser("fun myfun is a<-2; returns ; endfun ;"))
        # (ZoroParser("fun myfun is a<-2; returns 3; endfun ;"))
        # (ZoroParser("fun myfun of a,b is a<-2; endfun ;"))
        # (ZoroParser("fun myfun of a,b is a<-2; returns ; endfun ;"))
        # (ZoroParser("fun myfun of a,b is a<-2; returns 3; endfun ;"))
        # (ZoroParser("fun myfun of a,b,c is if(a+b<c) then  a<-b+c;  returns c;  elif (a-b<(c+b)) then returns b; else returns a; endif;  returns a+(b+c);  endfun;"))
        pass
    if(1):      # fun_call statement        ##TODO
        # (ZoroParser("myfun of a1,a2,a3 ;"))
        # (ZoroParser("var my_var <- myfun of a1,a2,a3 ; "))
        # (ZoroParser("print myfun of a1,a2,a3 ; "))
        # (ZoroParser("myfun of a1, my_other_fun of a2 , a3 ; "))   ##TODO : Dangling argument!
        pass
    if(1):      # print statement
        # (ZoroParser("print f of a1,a2,a3 ; "))
        # (ZoroParser("print f of (a1),(a2),a3 ; "))
        pass
    if(1):      # List
        # (ZoroParser("var a <- [] ; "))
        pass
    if(1):      # Brackets
        # (ZoroParser("(1) or (a);"))
        # (ZoroParser("(1) and (a);"))
        # (ZoroParser("(1) + (a);"))
        # (ZoroParser("(1+2)*a + 4 ^ 5 * 6;"))
        # (ZoroParser(" 2 * (3+5 or 9) xor 5 ** 6 + 4 * ~ (i +- 5 ^ 8) ; "))
        # (ZoroParser(" if (1+2>(3)) then 5+(6 * 8 or 5); else d<-5; endif; "))
        pass
    if(1):      # ListOps
        # (ZoroParser("a.len;"))
        # (ZoroParser('a.push "MY_STR" ;'))
        # (ZoroParser("a.pop 0 ;"))
        # (ZoroParser('a.insert "MY_STR" 0 ;'))
        # (ZoroParser("a.index 5 ;"))
        # (ZoroParser("a.at 5 ;"))
        # (ZoroParser("a.count 5 ;"))
        # (ZoroParser('var a <- [14,15,16,17,18,19,20] ; print a; var b<-a.len; print b; a.push 6 ; print a; a.pop 0 ;print a; a.insert 7 3 ;print a; var c<-a.index 5 ; print c; var d<-a.count 5 ; print d; print a; a<-[101,102,101,103,104]; var e<-a.len; print e; '))
        pass
    if(1):      # StringOps
        # (ZoroParser(' "My_str" . strlen ; '))
        # (ZoroParser(' "MY_str" . concat "UR_str" ; '))
        # (ZoroParser(' "MY_str" . slice 2 5 ; '))
        # # (ZoroParser(' "My_str" . locate 2 ; '))
        # # (ZoroParser(' "My_str" . count_char _ ; '))
        # # (ZoroParser(' "My_str" . count_char m ; '))
        
        # (ZoroParser(' a . strlen ; '))
        # (ZoroParser(' a . concat b ; '))
        # (ZoroParser(' a . slice a a ; '))
        # # (ZoroParser(' a . locate 2 ; '))
        # # (ZoroParser(' a . count_char _ ; '))
        # # (ZoroParser(' a . count_char m ; '))
        pass
    if(1):      # BREAK statement
        # (ZoroParser("var a<-2; var i<-0; while a>0 do if a>5 then break; else a<-a+1; i<-i+1; endif; endwhile; print a;"))
        pass
    if(1):      # range
        # (ZoroParser(" a <- range 3,2,5 ; "))
        # (ZoroParser(" a <- range 3,2 ; "))
        # (ZoroParser(" for i in range 3,11,2 do a<-1; endfor; "))
        # (ZoroParser(" for i in range 5,10 do a<-1; endfor; "))
        pass
    if(1):      # Arrays
        # (ZoroParser("var Int a[5] <- [2,1,4] ;"))
        # (ZoroParser("var Float a[5] <- [2.0,1.0,4.0] ;"))
        # (ZoroParser(""" var String c[5] <- ["1", "2", "3"]; print c;  var l <- [1, "2", 3.0];  print l; """))
        pass
    
    if(1):      # APNE PROGRAMS 1 : OLD_VERSION
        # ZoroParser("fun fib of n is  a <- 0;  if n > 1;   then n1 <- n - 1;  b <- fib of n1;;;  n2 <- n - 2;  c <- fib of n2;;;  a <- b + c;  else a <- n;  endif;  returns a;  endfun;  print fib of 5;;;;")
        # ZoroParser(" fun f of n is if n>1; then b<-f of n-1;;; c<-b*n; else c<-1; endif; returns c; endfun;   print f of 4;;;; ")
        # ZoroParser("sum <- 0;  i <- 0;  while i<1000; do      if     i%3 == 0 or i%5 == 0;    then          sum <- sum + i;      endif;      i <- i + 1; print i; sum; ; endwhile;  print sum;;")
        # ZoroParser("fun isprime of n is b<-True; j<-2; while   j<n and b==True;   do if n%j==0; then b<-False; endif; j<-j+1; endwhile; print b;; returns b; endfun; print isprime of 13;;;;")     #N<-26; mp<-2; i<-2; while i<N; do   a<-isprime of i;;;    if     a==True and N%i==0;    then mp<-i; endif; i<-i+1; endwhile; print mp;; ")
        # ZoroParser("fun fib of n is a<-0; if n>1; then n1<-n-1; cc<-fib of n-1;;; dd<-fib of n-2;;; c ; a<-b+c; else a<-n; endif; returns a; endfun; y<-fib of 5; ; ; print y;; ")
        # ZoroParser("fun double of x is a<-2*x; returns a; endfun; a<-5; y <- double of a; ; ; ")
        # ZoroParser("m1 <- 1000//3; s1 <- m1+1; s1 <- 3*s1*m1//2;  m2 <- 1000//5; s2 <- m2+1; s2 <- 5*s2*m2//2;  m3 <- 1000//15; s3 <- m3+1; s3 <- 15*s3*m3//2;  ans <- s1 + s2 - s3; print ans; ;")
        # ZoroParser("fun fib of n is a<-0; if n>1; then a<- ((fib of (n-1;)) + (fib of n-2;)) ; else a<-n; endif; returns a; endfun; print fib of 5; ")
        # ZoroParser(" list_name <- [1; 2; 5;] ; for i in list_name do k<-2; endfor; ")
        pass
    if(1):      # APNE PROGRAMS 2 : OLD_VERSION : EULER 1 3 7
        # (ZoroParser("sum <- 0; i <- 0; while i<10 do if i%3 == 0 or i%5 == 0 then sum <- sum + i; endif; i <- i + 1; endwhile; print sum;  "))
        # (ZoroParser("fun isPrime of n is var a <- True; var i <- 2; while i<n and a == True do if n%i == 0 then a <- False; endif; i <- i + 1; endwhile; returns a endfun; print isPrime of 13;; k <- 45; j <- 2; mp <- 2; while j <= k do p <- isPrime of j;; if k%p == 0 then mp <- j; endif; j <- j + 1; endwhile; print mp;"))
        # (ZoroParser("fun isPrime of n is var a <- True; var i <- 2; while i<n and a == True do if n%i == 0 then a <- False; endif; i <- i + 1; print a; endwhile; returns a endfun; p <- 2; cnt <- 0; j <- 2; while cnt <= 10001 do if isPrime of j; then cnt <- cnt + 1; p<- j; endif; j <- j + 1; endwhile; print p; "))
        pass
    


    """ Invalid Programs """ """ For Parser Only """
    if(1):
        # (ZoroParser(";"))
        # (ZoroParser("#"))
        # (ZoroParser("__#__"))
        # (ZoroParser("_this_85_#_65_ad_"))
        # (ZoroParser('_a.n'))
        # (ZoroParser(' 59.54 ^ invalid"This is abra kadabra string !  lOl ;) "    Dont%Do\\This '))
        pass
    if(1):                                          ##TODO
        # (ZoroParser("var a <- 5 -> b ; "))
        # (ZoroParser("var a <- b <- 5 ; "))
        # (ZoroParser("var a <- var b <- 5 ; "))
        # (ZoroParser("var a <- (var b <- 5) ; "))  ##TODO : This shouldn't parse, but thanks to brackets!
        # (ZoroParser("var Int a[5] <- [2,1,4.0] ;"))
        pass
    if(1):                                          ##TODO
        # (ZoroParser("if c>0 then b<-2; elif k<k then l>5; returns b; endif ;"))     # fun_def & returns statements
        # (ZoroParser(" f of a b c; "))   # fun_call statement
        # (ZoroParser(" f of   is my_bad; endfun; "))   # fun_call statement
        # (ZoroParser(" print a,b c; "))    # print
        # (ZoroParser("()"))
        pass
    
    if(1):            ##TODO ADD_INVALID_TESTCASES_BY_CATEGORY
        # (ZoroParser(""))    # Arithmetics
        # (ZoroParser(""))    # Arithmetics
        # (ZoroParser(""))    # Arithmetics
        # (ZoroParser(""))    # If
        # (ZoroParser(""))    # While
        # (ZoroParser(""))    # For
        pass
    if(1):            ##TODO ADD_INVALID_TESTCASES_BY_CATEGORY
        # (ZoroParser(""))    # Brackets
        # (ZoroParser(""))    # Brackets
        # (ZoroParser(""))    # ListOps
        # (ZoroParser(""))    # ListOps
        # (ZoroParser(""))    # StringOps
        # (ZoroParser(""))    # StringOps
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

