from fractions import Fraction
import re
from dataclasses import dataclass
from typing import List

# A minimal example to illustrate typechecking.

class EndOfStream(Exception): pass
class EndOfTokens(Exception): pass
class TokenError(Exception): pass


@dataclass
class Stream:
    source: str
    pos: int

    def from_string(s):
        return Stream(s, 0)

    def next_char(self):
        if self.pos >= len(self.source):
            raise EndOfStream()
        self.pos = self.pos + 1
        return self.source[self.pos - 1]

    def unget(self):
        assert self.pos > 0
        self.pos = self.pos - 1


# Token Classes
@dataclass
class Int:
    value: int
    def __init__(self, value, *args) -> None:
        self.value = int(value)

@dataclass
class Float:
    value: float
    def __init__(self, value, *args) -> None:
        self.value = float(value)

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
class Bool:
    value: bool
    def __init__(self, value, *args) -> None:
        self.value = bool(value)


@dataclass
class Keyword:
    word: str

@dataclass
class Identifier:
    word: str

@dataclass
class Operator:
    op: str

@dataclass
class Symbol:
    sym: str

@dataclass
class UnknownWord:
    word: str

@dataclass
class end_of_all_tokens(Exception):
    e: str



Token = Int | Float | Frac | String | Bool | Keyword | Identifier | Operator | UnknownWord | Symbol | end_of_all_tokens

keywords = " Int Float Frac Bool String    var    if then elif else endif    print    fun of is returns endfun    while do endwhile  break    for in endfor    concat     push pop len insert count index at update ".split()
symbolic_operators = "+ - * / < > <= >= = ==  ! != ** % // ~ & | ^ -> <- << >>  ".split()
word_operators = "and or not xor xnor nand nor concat from to".split()
brackets = "[ ( ) ]".split()
whitespace = " \t \n".split() + [' ']



def word_to_token(word):
    if word in keywords:
        return Keyword(word)
    if word in word_operators:
        return Operator(word)
    if word in symbolic_operators:
        return Operator(word)
    if word == "True":
        return Bool(True)
    if word == "False":
        return Bool(False)
    a = None
    try:
        a = float(word)
        return Float(a)
    except ValueError:
        pass
    ptrn = "^[_a-zA-Z][_a-zA-Z0-9]*$"
    if(re.match(ptrn, word)):
        return Identifier(word)
    try:
        a = int(word)
        return Int(a)
    except ValueError:
        pass
    return UnknownWord(word)



@dataclass
class Lexer:
    stream: Stream
    save: Token = None

    def from_stream(s):
        return Lexer(s)

    def next_token(self) -> Token:
        try:
            match self.stream.next_char():
                case ',':
                    return Symbol(',')
                case ';':
                    return Symbol(';')
                case '.':
                    return Symbol('.')
                case '(':
                    return Symbol('(')
                case '[':
                    return Symbol('[')
                case ')':
                    return Symbol(')')
                case ']':
                    return Symbol(']')
                
                case c if c in symbolic_operators: 
                    s = c
                    while True:
                        try:
                            c = self.stream.next_char()
                            if s+c in symbolic_operators:
                                s = s + c
                            else:
                                self.stream.unget()
                                # print(Operator(s))
                                return Operator(s)
                        except EndOfStream:
                            # print(Operator(s))
                            return Operator(s)
                case c if c.isalpha() or c=='_':
                    s = c
                    while True:
                        try:
                            c = self.stream.next_char()
                            if c.isalpha() or c=='_' or c.isdigit():
                                s = s + c
                            else:
                                self.stream.unget()
                                # print(word_to_token(s))
                                return word_to_token(s)
                        except EndOfStream:
                            # print(word_to_token(s))
                            return word_to_token(s)
                case c if c.isdigit():
                    n = int(c)
                    decimal_point = False
                    while True:
                        try:
                            c = self.stream.next_char()
                            # print(c)
                            if ((c.isdigit()) and (decimal_point == False)):
                                n = n*10 + int(c)
                            # currently not handling the error of double decimal point.
                            elif ((c.isdigit()) and (decimal_point == True)):
                                n = n+int(c)*factor
                                factor = 0.1*factor
                            elif((c == '.') and (decimal_point == False)):
                                decimal_point = True
                                factor = 0.1
                            else:
                                self.stream.unget()
                                if (decimal_point):                                    
                                    return Float(n)
                                else:
                                    return Int(n)
                        except EndOfStream:
                            if(decimal_point):
                                return Float(n)
                            return Int(n)
                case c if c =='"':
                    s = c
                    c = self.stream.next_char()
                    while(c!= '"'):
                        s = s+c
                        c = self.stream.next_char()
                    s = s+c
                    return String(s[1:-1])
                case c if c in whitespace:
                    return self.next_token()
                case c if c=='#':
                    s = c
                    c = self.stream.next_char()
                    while(c!='#'):
                        c = self.stream.next_char()
                    return None
                case _:
                    pass
                
        except EndOfStream:
           raise EndOfTokens


    def peek_token(self) -> Token:
        if self.save is not None:
            return self.save
        self.save = self.next_token()
        return self.save

    def advance(self):
        assert self.save is not None
        self.save = None

    def match(self, expected):
        if self.peek_token() == expected:
            return self.advance()
        raise TokenError()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.next_token()
        except EndOfTokens:
            raise StopIteration




def print_tokens(code: str):
    # strs = code.split(';')
    # l= []
    # for i in range(len(strs)):
    #     code = strs[i]
    #     if(i!=len(strs)-1):
    #         code = code+';'
        stream = Stream.from_string(code)
        lexer = Lexer(stream)
        tokens = []
        try:
            while True:
                token = lexer.next_token()
                # if(token==None):
                #     continue
                tokens.append(token)
                # print(token)
        except EndOfTokens:
            pass
    #     l.append(tokens)
    # l[i].append(end_of_all_tokens("end_of_tokens"))
    # return l
        return tokens




# ans = print_tokens("a+b = 2;3+3=6")
# print(ans)
