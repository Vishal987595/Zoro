from dataTypeDeclaration import *
from evalAST import *
import math

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
    assert evalAST(UnOp("-",e1)) == 0
    assert evalAST(UnOp("~",e2)) == -2
    assert evalAST(UnOp("-",e3)) == -7
    assert evalAST(UnOp("~",e3)) == -8

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
    e3 = LogOp("and", CndOp(">", e1, e2), CndOp("<", e1, e2))
    assert evalAST(e3) == False
    e4 = LogOp("and", CndOp("<", e1, e2), CndOp("!=", e1, e2))
    assert evalAST(e4) == True
    e5 = LogOp("or", CndOp(">", e1, e2), CndOp("<", e1, e2))
    assert evalAST(e5) == True
    e6 = LogOp("or", CndOp(">", e1, e2), CndOp("!=", e1, e1))
    assert evalAST(e6) == False

def test_seq():
    e1 = Int(5)
    e2 = Int(10)
    e4 = LogOp("and", CndOp("<", e1, e2), CndOp("!=", e1, e2))
    e3 = LogOp("and", CndOp(">", e1, e2), CndOp("<", e1, e2))
    e5 = LogOp("or", CndOp(">", e1, e2), CndOp("<", e1, e2))
    e6 = LogOp("or", CndOp(">", e1, e2), CndOp("!=", e1, e1))
    assert evalAST(Sequence([e3,e4,e5,e6])) == False
    e7 = BinOp("+", e1, e2)

def test_for():
    a = Variable("a")
    assert evalAST(For(a, List_([Int(5), Int(6), Int(7)]), Sequence([]))) == None
    e1 = Int(5)
    e2 = Int(10)
    e3 = LogOp("and", CndOp(">", e1, e2), CndOp("<", e1, e2))
    e4 = LogOp("and", CndOp("<", e1, e2), CndOp("!=", e1, e2))
    e5 = LogOp("or", CndOp(">", e1, e2), CndOp("<", e1, e2))
    e6 = LogOp("or", CndOp(">", e1, e2), CndOp("!=", e1, e1))
    assert evalAST(For(a, List_([Int(5), Int(6), Int(7)]), Sequence([e3,e4,e5,e6]))) == False

def test_while():
    pass

def test_funcdec():
    v = Variable('a')
    f = "myfun"
    expr = Sequence([BinOp('+', v, v)])
    ret = v
    fun = FuncDec(f, [v], expr, ret)
    assert evalAST(fun) == {'params': [v], 'seq': expr, 'ret': v}
    # print(evalAST(fun))
    
def test_print():
    e = Print([String("a"), MathOp('+', Int(1), Int(2))])
    evalAST(e)

def test_string():
    s1 = String("abc")
    s2 = String("def")
    n1 = Int(2)
    n2 = Int(4)
    assert evalAST(s1) == "abc"
    assert evalAST(StringOp("concat", [s1, s2])) == "abcdef"
    assert evalAST(StringOp("slice", [StringOp("concat", [s1, s2]), n1, n2])) == "cde"

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

def test_ifelse_find_max_abc():
    evalAST(Sequence(seq=[AssignOp(operator='<-', left=Variable(name='a'), right=Int(3)), AssignOp(operator='<-', left=Variable(name='b'), right=Int(4)), AssignOp(operator='<-', left=Variable(name='c'), right=Int(5)), If(con=[CndOp(operator='>', left=Variable(name='a'), right=Variable(name='b'))], seq=[Sequence(seq=[If(con=[CndOp(operator='>=', left=Variable(name='b'), right=Variable(name='c'))], seq=[Sequence(seq=[Print(contents=[Variable(name='a')])]), Sequence(seq=[If(con=[CndOp(operator='>', left=Variable(name='a'), right=Variable(name='c'))], seq=[Sequence(seq=[Print(contents=[Variable(name='a')])]), Sequence(seq=[Print(contents=[Variable(name='c')])])])])])]), Sequence(seq=[If(con=[CndOp(operator='>=', left=Variable(name='a'), right=Variable(name='c'))], seq=[Sequence(seq=[Print(contents=[Variable(name='b')])]), Sequence(seq=[If(con=[CndOp(operator='>', left=Variable(name='b'), right=Variable(name='c'))], seq=[Sequence(seq=[Print(contents=[Variable(name='b')])]), Sequence(seq=[Print(contents=[Variable(name='c')])])])])])])])]))

def test_euler1_multiple_3or5():
    evalAST(Sequence(seq=[AssignOp(operator='<-', left=Variable(name='m1'), right=MathOp(operator='//', left=Int(value=1000), right=Int(value=3))), AssignOp(operator='<-', left=Variable(name='s1'), right=MathOp(operator='+', left=Variable(name='m1'), right=Int(value=1))), AssignOp(operator='<-', left=Variable(name='s1'), right=MathOp(operator='//', left=MathOp(operator='*', left=MathOp(operator='*', left=Int(value=3), right=Variable(name='s1')), right=Variable(name='m1')), right=Int(value=2))), AssignOp(operator='<-', left=Variable(name='m2'), right=MathOp(operator='//', left=Int(value=1000), right=Int(value=5))), AssignOp(operator='<-', left=Variable(name='s2'), right=MathOp(operator='+', left=Variable(name='m2'), right=Int(value=1))), AssignOp(operator='<-', left=Variable(name='s2'), right=MathOp(operator='//', left=MathOp(operator='*', left=MathOp(operator='*', left=Int(value=5), right=Variable(name='s2')), right=Variable(name='m2')), right=Int(value=2))), AssignOp(operator='<-', left=Variable(name='m3'), right=MathOp(operator='//', left=Int(value=1000), right=Int(value=15))), AssignOp(operator='<-', left=Variable(name='s3'), right=MathOp(operator='+', left=Variable(name='m3'), right=Int(value=1))), AssignOp(operator='<-', left=Variable(name='s3'), right=MathOp(operator='//', left=MathOp(operator='*', left=MathOp(operator='*', left=Int(value=15), right=Variable(name='s3')), right=Variable(name='m3')), right=Int(value=2))), AssignOp(operator='<-', left=Variable(name='ans'), right=MathOp(operator='-', left=MathOp(operator='+', left=Variable(name='s1'), right=Variable(name='s2')), right=Variable(name='s3'))), Print(contents=[Variable(name='ans')])]))

def test_euler3_Lagest_Prime_factor():
    evalAST(Sequence(seq=[FuncDec(name=Function(name='isprime'), params=[Variable(name='n')], body=Sequence(seq=[AssignOp(operator='<-', left=Variable(name='b'), right=Bool(value=True)), AssignOp(operator='<-', left=Variable(name='j'), right=Int(value=2)), While(cnd=LogOp(operator='and', right=CndOp(operator='<', left=Variable(name='j'), right=Variable(name='n')), left=CndOp(operator='==', left=Variable(name='b'), right=Bool(value=True))), seq=Sequence(seq=[If(con=[CndOp(operator='==', left=MathOp(operator='%', left=Variable(name='n'), right=Variable(name='j')), right=Int(value=0))], seq=[Sequence(seq=[AssignOp(operator='<-', left=Variable(name='b'), right=Bool(value=False))])]), AssignOp(operator='<-', left=Variable(name='j'), right=MathOp(operator='+', left=Variable(name='j'), right=Int(value=1)))])), Print(contents=[Variable(name='b')])]), returns=[Variable(name='b')]), AssignOp(operator='<-', left=Variable(name='N'), right=Int(value=26)), AssignOp(operator='<-', left=Variable(name='mp'), right=Int(value=2)), AssignOp(operator='<-', left=Variable(name='i'), right=Int(value=2)), While(cnd=CndOp(operator='<', left=Variable(name='i'), right=Variable(name='N')), seq=Sequence(seq=[AssignOp(operator='<-', left=Variable(name='a'), right=FuncCall(name=Function(name='isprime'), args=[Variable(name='i')])), If(con=[LogOp(operator='and', right=CndOp(operator='==', left=Variable(name='a'), right=Bool(value=True)), left=CndOp(operator='==', left=MathOp(operator='%', left=Variable(name='N'), right=Variable(name='i')), right=Int(value=0)))], seq=[Sequence(seq=[AssignOp(operator='<-', left=Variable(name='mp'), right=Variable(name='i'))])]), AssignOp(operator='<-', left=Variable(name='i'), right=MathOp(operator='+', left=Variable(name='i'), right=Int(value=1)))])), Print(contents=[Variable(name='mp')])]))

def test_range():
    # evalAST(Sequence(seq=[For(var=Variable(name='i'), iter=Range(num1 = Int(0), num2 = Int(10), jmp = Int(2)), seq=Sequence(seq=[Print(contents=[Variable(name='i')])]))]) )
    # evalAST(Sequence(seq=[For(var=Variable(name='i'), iter=Range(num1 = Int(0), num2 = Int(10), jmp = NULL), seq=Sequence(seq=[Print(contents=[Variable(name='i')])]))]) )
    # evalAST(Sequence(seq=[For(var=Variable(name='i'), iter=Range(num1 = Int(-5), num2 = Int(10), jmp = Int(2)), seq=Sequence(seq=[Print(contents=[Variable(name='i')])]))]) )
    # evalAST(Sequence(seq=[For(var=Variable(name='i'), iter=Range(num1 = Int(-5), num2 = Int(-20), jmp = Int(2)), seq=Sequence(seq=[Print(contents=[Variable(name='i')])]))]) )
    # evalAST(Sequence(seq=[For(var=Variable(name='i'), iter=Range(num1 = Int(-20), num2 = Int(-5), jmp = Int(2)), seq=Sequence(seq=[Print(contents=[Variable(name='i')])]))]) )
    evalAST(Sequence(seq=[For(var=Variable(name='i'), iter=Range(num1 = Int(20), num2 = Int(-5), jmp = Int(2)), seq=Sequence(seq=[Print(contents=[Variable(name='i')])]))]) )

def test_listops():
    evalAST(Sequence(seq=[AssignOp(operator='<-', left=Variable(name='a'), right=List_(items=[Int(value=14), Int(value=15), Int(value=16), Int(value=17), Int(value=18), Int(value=19), Int(value=20)])), Print(contents=[Variable(name='a')]), AssignOp(operator='<-', left=Variable(name='b'), right=ListOp(list=Variable(name='a'), operator='len', item=Null(value=None), index=Null(value=None))), Print(contents=[Variable(name='b')]), 
 
 ListOp(list=Variable(name='a'), operator='push', item=Int(value=6), index=Null(value=None)), Print(contents=[Variable(name='a')]), 
 ListOp(list=Variable(name='a'), operator='pop', item=Null(value=None), index=Int(value=0)), Print(contents=[Variable(name='a')]), 
 ListOp(list=Variable(name='a'), operator='insert', item=Int(value=7), index=Int(value=3)), Print(contents=[Variable(name='a')]), 
 AssignOp(operator='<-', left=Variable(name='c'), right=ListOp(list=Variable(name='a'), operator='index', item=Int(value=5), index=Null(value=None))), Print(contents=[Variable(name='c')]), 
 AssignOp(operator='<-', left=Variable(name='d'), right=ListOp(list=Variable(name='a'), operator='count', item=Int(value=5), index=Null(value=None))), Print(contents=[Variable(name='d')]), Print(contents=[Variable(name='a')])]))

def test_printdebug():
    evalAST( Sequence(seq=[AssignOp(operator='<-', left=Variable(name='a'), right=Int(value=2)), Print(contents=[Variable(name='a')])]))

def dummy():
    a = Sequence(seq=[UpdateOp(operator='<-', left=Variable(name='a'), right=List_(items=[Int(value=1), Int(value=2), Int(value=5), Int(value=4)])), Print(contents=[ListOp(list=Variable(name='a'), operator='at', item=Null(value=None), index=Int(value=2))])]) 
    evalAST(a)



def test():
    # test_datatypes() # Works fine, don't touch
    # test_let() # Works fine, don't touch
    # test_mathOp() # Works fine, don't touch
    # test_cndOp() # Works fine, don't touch
    # test_unOp() # Works fine, don't touch
    # test_bitOp() # Works fine, don't touch
    # test_ifElse() # Works fine, don't touch
    # test_assign() # Works fine, don't touch
    # test_binOp() # Works fine, don't touch
    # test_seq() # Works fine, don't touch
    # test_for() # Works fine, don't touch
    # test_while() #Complete it first
    # test_funcdec() # Works fine, don't touch
    # test_print() # Works fine, don't touch 
    # test_string() # Works fine, don't touch
    # test_list() # Works fine, don't touch
    # test_ifelse_find_max_abc()
    # test_euler1_multiple_3or5()
    # test_euler3_Lagest_Prime_factor()
    # test_range()
    # test_listops()
    # test_printdebug()
    dummy()

test()
