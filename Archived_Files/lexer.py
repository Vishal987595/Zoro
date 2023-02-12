from dataclasses import dataclass
import re
from typing import List
class EndOfStream(Exception):
    pass

@dataclass
class Stream:
    source: str
    pos: int

@dataclass
class Int:
    n: int

@dataclass
class Bool:
    b: bool

@dataclass
class Keyword:
    word: str

@dataclass
class Identifier:
    word: str

@dataclass
class UnknownWord:
    word: str

@dataclass
class Operator:
    op: str

@dataclass
class Float:
    f: float

Token = Int | Bool | Keyword | Identifier | Operator
keywords = "int float bool let in if then else while endwhile do elif endif".split()
symbolic_operators = "+ - * / < > <= >= == != ** % // ~ & | ^".split()
word_operators = "and or not xor nand nor xnor".split()
whitespace = [' ', '\t', '\n']

class EndOfTokens(Exception):
    pass

class TokenError(Exception):
    pass

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
        a = int(word)
        return Int(a)
    except ValueError:
        pass
    try:
        a = float(word)
        return Float(a)
    except ValueError:
        pass
    ptrn = "^[_a-zA-Z][a-zA-Z0-9_]*$"
    if(re.match(ptrn, word)):
        return Identifier(word)
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
                case c if c in symbolic_operators: return Operator(c)
                case c if c.isdigit():
                    n = int(c)
                    while True:
                        try:
                            c = self.stream.next_char()
                            if c.isdigit():
                                n = n*10 + int(c)
                            else:
                                self.stream.unget()
                                return Int(n)
                        except EndOfStream:
                            return Int(n)
                case c if c.isalpha():
                    s = c
                    while True:
                        try:
                            c = self.stream.next_char()
                            if c.isalpha():
                                s = s + c
                            else:
                                self.stream.unget()
                                return word_to_token(s)
                        except EndOfStream:
                            return word_to_token(s)
                case c if c in whitespace:
                    return self.next_token()
        except EndOfStream:
            raise EndOfTokens

    def peek_token(self) -> Token:
        if self.save is not None:
            return self.save
        self.save = self.next_token()
        return self.save
    
    def tokenize(self) -> List[Token]:
        lst = []
        issinglecom = False
        ismultcom = False
        pos = 0
        src = self.stream.source
        for i in src:
            if i=='#':
                issinglecom = True
            if i == "/":
                if src[pos+1] == "*":
                    ismultcom == True
            if i == '\n' and issinglecom:
                issinglecom = False
            if i == "/" and ismultcom:
                if src[pos-1] == "*":
                    ismultcom = False
            if issinglecom or ismultcom:
                pass
            else:
                lst.append(i)
            pos += 1
        return lst




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
