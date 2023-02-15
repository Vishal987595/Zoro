from fractions import Fraction
import re
from dataclasses import dataclass
from typing import Optional, NewType

# A minimal example to illustrate typechecking.

class EndOfStream(Exception):
    pass

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

# Define the token types.

@dataclass
class Int:
    n: int

@dataclass
class String:
    s: str

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

Token = Int | Bool | Keyword | Identifier | Operator | Float

class EndOfTokens(Exception):
    pass

keywords = "Int String Float Bool let if then else elif endif".split()
symbolic_operators = "+ - * / < > <= >= == != ** % // ~ & | ^ -> <- << >>".split()
word_operators = "and or not xor xnor nand nor".split()
whitespace = " \t \n".split() + [' ']

def word_to_token(word):
    if word in keywords:
        return Keyword(word)
    if word in word_operators:
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



class TokenError(Exception):
    pass

@dataclass
class Lexer:
    stream: Stream
    save: Token = None

    def from_stream(s):
        return Lexer(s)

    def next_token(self) -> Token:
        try:
            match self.stream.next_char():
                case c if c in symbolic_operators: 
                    s = c
                    while True:
                        try:
                            c = self.stream.next_char()
                            if s+c in symbolic_operators:
                                s = s + c
                            else:
                                self.stream.unget()
                                return Operator(s)
                        except EndOfStream:
                            return Operator(s)

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
                case c if c.isalpha() or c=='_':
                    s = c
                    while True:
                        try:
                            c = self.stream.next_char()
                            if c.isalpha() or c=='_':
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
