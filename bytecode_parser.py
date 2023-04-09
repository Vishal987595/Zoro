from lib2to3.pgen2.token import OP
from dataTypeDeclaration import *
from Zoro_parser import ZoroParser


#in case of binary operations, please remember that left is pushed before right
#thus while popping, the first value you pop will be right, not left.
def parseAST_(ast: AST, code: ByteCode) -> None:

    def parse_(ast):
        parseAST_(ast, code)

    match ast:

        case MathOp("+", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('+'))
        case MathOp("-", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('-'))
        case MathOp("*", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('*'))
        case MathOp("/", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('/'))
        case MathOp("//", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('//'))
        case MathOp("**", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('**'))
        case MathOp("%", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('%'))

        case CndOp(">", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('>'))
        case CndOp("<", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('<'))
        case CndOp(">=", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('>='))
        case CndOp("<=", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('<='))
        case CndOp("==", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('=='))
        case CndOp("!=", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('!='))

        case UnOp("-", right):
            parse_(right)
            code.emit(Operator('u-'))
        case UnOp("~", right):
            parse_(right)
            code.emit(Operator('u~'))
        case UnOp("not", right):
            parse_(right)
            code.emit(Operator('not'))

        case BitOp("&", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('&'))
        case BitOp("|", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('|'))
        case BitOp("^", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('^'))
        case BitOp("<<", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('<<'))
        case BitOp(">>", left, right):
            parse_(left)
            parse_(right)
            code.emit(Operator('>>'))

