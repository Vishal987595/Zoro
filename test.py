from dataTypeDeclaration import *
from evalAST import *
from parserLexer import *
from exceptions import *

def test_datatypes():
    pass

def test_let():
    assert evalAST(Frac(2.5))==5/2
    assert evalAST(Frac(2.5))==2.5
    assert evalAST(Frac(2.5))==Fraction(2.5)
    assert evalAST(Frac(2.5))==Fraction(5/2)
    assert evalAST(Frac(5/2))==5/2
    assert evalAST(Frac(5/2))==2.5
    assert evalAST(Frac(5/2))==Fraction(2.5)
    assert evalAST(Frac(5/2))==Fraction(5/2)
    # assert evalAST(Frac(math.pi))==Fraction(22/7) #This Error shows that input of Frac should be terminating
    assert evalAST(Int(2)) == 2
    assert evalAST(Int(math.pi)) == 3
    assert evalAST(Int(-math.pi)) == -3
    assert evalAST(Float(2)) == 2
    assert evalAST(Float(2)) == 2.0
    assert evalAST(Float(2/5)) == 0.4
    assert evalAST(Bool(7)) == True
    assert evalAST(Bool(-7)) == True
    assert evalAST(Bool(0)) == False

def test_mathOp():
    e1 = Int(5)
    e2 = Int(2)
    e3 = MathOp("+", e1, e1)
    e4 = MathOp("*", e3, e2)
    e5 = MathOp("-", e4, e1)
    e6 = MathOp("/", e5, e1)
    assert evalAST(e6) == 3

def test_cndOp():
    e1 = Int(5)
    e2 = Int(10)
    assert evalAST(CndOp(">", e1, e2)) == False
    assert evalAST(CndOp("<", e1, e2)) == True
    assert evalAST(CndOp("!=", e1, e2)) == True
    assert evalAST(CndOp("!=", e1, e1)) == False
    assert evalAST(CndOp("==", e1, e2)) == False
    assert evalAST(CndOp("==", e1, e1)) == True
    assert evalAST(CndOp(">=", e1, e1)) == True
    assert evalAST(CndOp("<=", e1, e1)) == True

def test_unOp():
    e1 = Int(0)
    e2 = Int(1)
    e3 = Int(7)
    e4 = String("")
    e4 = String("dhdv")
    assert evalAST(UnOp("!",e1)) == True
    assert evalAST(UnOp("!",e2)) == False
    assert evalAST(UnOp("!",e3)) == False
    assert evalAST(UnOp("!",e4)) == True
    assert evalAST(UnOp("!",e3)) == False

def test_bitOp():
    e1 = Int(74)
    e2 = Int(71)
    e3 = Int(4)
    assert evalAST(BitOp("&",e1,e2)) == 66
    assert evalAST(BitOp("|",e1,e2)) == 79 
    assert evalAST(BitOp("^",e1,e2)) == 13
    assert evalAST(BitOp("<<",e1,e3)) == 1184
    assert evalAST(BitOp(">>",e1,e3)) == 4

def test_ifElse():
    e1 = Int(5)
    e2 = Int(10)
    e3 = Int(15)
    e4 = Int(20)
    e5 = MathOp("+", e1, e2)
    e6 = MathOp("+", e3, e4)
    e7 = MathOp("+", e2, e4)
    e8 = If([CndOp(">", e1, e2), CndOp(">", e3, e4)],[e5, e6, e7])
    assert evalAST(e8) == 30

def test_assign():
    e1 = Variable("a")
    e2 = Int(5)
    e3 = Assign("<-",e1, e2)
    evalAST(e3)
    assert evalAST(e1) == 5
    e4 = Int(6)
    e5 = Assign("->",e4, e1)
    evalAST(e5)
    assert evalAST(e5) == 6

def test_binOp():
    e1 = Int(5)
    e2 = Int(10)
    e3 = BinOp("and", CndOp(">", e1, e2), CndOp("<", e1, e2))
    assert evalAST(e3) == False
    e4 = BinOp("and", CndOp("<", e1, e2), CndOp("!=", e1, e2))
    assert evalAST(e4) == True
    e5 = BinOp("or", CndOp(">", e1, e2), CndOp("<", e1, e2))
    assert evalAST(e5) == True
    e6 = BinOp("or", CndOp(">", e1, e2), CndOp("!=", e1, e1))
    assert evalAST(e6) == False


def test():
    test_datatypes()
    test_let()
    test_mathOp()
    test_cndOp()
    test_unOp()
    test_bitOp()
    test_ifElse()
    test_assign()
    test_binOp()

test()