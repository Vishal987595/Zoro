from dataTypeDeclaration import *
from evalAST import *
# from parserLexer import *
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
    assert evalAST(UnOp("!",e1)) == True
    assert evalAST(UnOp("!",e2)) == False
    assert evalAST(UnOp("!",e3)) == False
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
    a = Variable("a")
    b = Variable("b")
    e1 = Let(b, Int(2), AssignOp("<-", a, MathOp("+", Get(a), Get(b))))
    e2 = Let(a, Int(1), Sequence([e1, Get(a)]))
    assert evalAST(e2) == 3

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

def test_seq():
    e1 = Int(5)
    e2 = Int(10)
    e3 = BinOp("and", CndOp(">", e1, e2), CndOp("<", e1, e2))
    e4 = BinOp("and", CndOp("<", e1, e2), CndOp("!=", e1, e2))
    e5 = BinOp("or", CndOp(">", e1, e2), CndOp("<", e1, e2))
    e6 = BinOp("or", CndOp(">", e1, e2), CndOp("!=", e1, e1))
    assert evalAST(Sequence([e3,e4,e5,e6])) == False
    e7 = BinOp("+", e1, e2)

def test_for():
    a = Variable("a")
    assert evalAST(For(a, [Int(5), Int(6), Int(7)], Sequence([]))) == None
    e1 = Int(5)
    e2 = Int(10)
    e3 = BinOp("and", CndOp(">", e1, e2), CndOp("<", e1, e2))
    e4 = BinOp("and", CndOp("<", e1, e2), CndOp("!=", e1, e2))
    e5 = BinOp("or", CndOp(">", e1, e2), CndOp("<", e1, e2))
    e6 = BinOp("or", CndOp(">", e1, e2), CndOp("!=", e1, e1))
    assert evalAST(For(a, [Int(5), Int(6), Int(7)], Sequence([e3,e4,e5,e6]))) == False

def test_while():
    pass

def test_func():
    v = Variable('a')
    f = "myfun"
    expr = Sequence([BinOp('+', v, v)])
    ret = v
    fun = FuncDec(f, [v], expr, ret)
    assert evalAST(fun) == {'args': [v], 'seq': expr, 'ret': v}
    
def test_print():
    e = Print([String("a"), BinOp('+', Int(1), Int(2))])
    evalAST(e)

def test_string():
    s1 = String("abc")
    s2 = String("def")
    n1 = Int(2)
    n2 = Int(4)
    assert evalAST(s1) == "abc"
    assert evalAST("concat", [s1, s2]) == "abcdef"
    assert evalAST("slice", [evalAST("concat", [s1, s2]), n1, n2]) == "cde"

def test_list():
    e1 = Variable('a')
    # e2 = Sequence([AssignOp("<-", e1, List_([])), ListOp("push", e1, item=Int(1), index=None)])
    e2 = Sequence([AssignOp("<-", e1, List_([])), ListOp("push", e1, item=Int(1), index = None),
                                                ListOp("push", e1, item=Int(2), index = None),
                                                ListOp("push", e1, item=Int(3), index = None),
                                                ListOp("push", e1, item=Int(4), index = None),
                                                ListOp("pop", e1, item=None, index = Int(-1)),
                                                ListOp("push", e1, item=Int(5), index = None),
                                                ListOp("pop", e1, item=None, index = Int(0)),
                                                ListOp("insert", e1, item=Int(10), index = Int(1)),
                                                ListOp("index", e1, item=Int(3), index = None),
                                                ListOp("push", e1, item=Int(11), index = None),
                                                ListOp("push", e1, item=Int(11), index = None),
                                                ListOp("push", e1, item=Int(11), index = None),
                                                ListOp("count", e1, item=Int(11), index = None),
                                                # e1
                                                ])
    # print(evalAST(e2))
    assert evalAST(e2) == 3

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
    test_seq()
    test_for()
    test_while()
    # test_func()
    # test_print()
    # test_string()
    test_list()

test()
