from typing import Dict


class Error():
    def __init__(self, msg):
        print(msg)

class Variable:
    def __init__(self, name: str):
        self.name = name

class Int:
    def __init__(self, value: int):
        self.value = value

class CndOp:
    def __init__(self, operator: str, left, right):
        self.operator = operator
        self.left = left
        self.right = right

class AssignOp:
    def __init__(self, operator: str, left, right):
        self.operator = operator
        self.left = left
        self.right = right

class Print:
    def __init__(self, contents):
        self.contents = contents

class If:
    def __init__(self, con, seq):
        self.con = con
        self.seq = seq

class Sequence:
    def __init__(self, seq):
        self.seq = seq

def check_types(node, var_types: Dict[str, str]):
    if isinstance(node, Variable):
        if node.name not in var_types:
            e = Error(f" BRUH! Variable '{node.name}' is not defined.")
            return
        if var_types[node.name] != 'int':
            e = Error(f" DUDE! Variable '{node.name}' is not an integer.")
            return
        return 'int'

    if isinstance(node, Int):
        return 'int'

    if isinstance(node, CndOp):
        left_type = check_types(node.left, var_types)
        right_type = check_types(node.right, var_types)

        if node.operator in ['<', '>', '<=', '>='] and left_type != right_type:
            e = Error("Comparison operators can only be used between operands of the same type.")
            return
        return 'bool'

    if isinstance(node, AssignOp):
        right_type = check_types(node.right, var_types)

        if node.left.name in var_types and var_types[node.left.name] != right_type:
            e = Error(f"Cannot assign a value of type '{right_type}' to variable '{node.left.name}' of type '{var_types[node.left.name]}'")
            return
        var_types[node.left.name] = right_type
        return right_type

    if isinstance(node, Print):
        for item in node.contents:
            check_types(item, var_types)
        return 'void'

    if isinstance(node, Sequence):
        for sub_node in node.seq:
            check_types(sub_node, var_types)
        return 'void'

    if isinstance(node, If):
        con_type = check_types(node.con[0], var_types)
        if con_type != 'bool':
            e = Error(f"Condition in if statement must evaluate to type 'bool', not '{con_type}'")
            return
        check_types(node.seq[0], var_types)
        check_types(node.seq[1], var_types)
        return 'void'

# if __name__ == '__main__':
#     ast = Sequence(seq=[If(con=[CndOp(operator='>', left=Variable(name='c'), right=Int(value=0))], seq=[Sequence(seq=[AssignOp(operator='<-', left=Variable(name='b'), right=Int(value=2))]), Sequence(seq=[AssignOp(operator='->', left=Variable(name='c'), right=Variable(name='d'))])])])
#     check_types(ast, {})
