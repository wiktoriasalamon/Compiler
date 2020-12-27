class Number:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.value


class Var:
    def __init__(self, name, line):
        self.name = name
        self.line = line

    def __repr__(self):
        return self.name


class Arr:
    def __init__(self, name, line, start, end):
        self.name = name
        self.line = line
        self.start = start
        self.end = end
        self.length = int(end) - int(start) + 1

    def __repr__(self):
        return f"{self.name}({self.start}:{self.end})"


class ArrElem:
    def __init__(self, arr_name, line, index):
        self.arr_name = arr_name
        self.line = line
        self.index = index

    def __repr__(self):
        return f"{self.arr_name}({self.index})"


class Assign:
    def __init__(self, var: Var, expr, line):
        self.var = var
        self.expr = expr
        self.line = line

    def __repr__(self):
        return f"{self.var} := {self.expr}"


class BinaryOp:
    def __init__(self, left, op, right, line):
        self.left = left
        self.right = right
        self.line = line
        self.op = op

    def __repr__(self):
        return f"{self.left} {self.op} {self.right}"


class Read:
    def __init__(self, var, line):
        self.var = var
        self.line = line

    def __repr__(self):
        return f"read {self.var}"


class Write:
    def __init__(self, value, line):
        self.value = value
        self.line = line

    def __repr__(self):
        return f"write {self.value}"


class Program:
    def __init__(self, commands, declarations=None):
        self.declarations = declarations
        self.commands = commands

    def __repr__(self):
        return f"[{self.declarations}, {self.commands}]"