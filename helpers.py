class Var:
    def __init__(self, name, line):
        self.name = name
        self.line = line
        self.is_initialized = False
        self.type = 'variable'
        self.id = name
        self.is_global = True
        self.is_covered = False
        self.var_covering = None
        self.var_covered = None

    def __repr__(self):
        return self.name


class Arr:
    def __init__(self, name, line, start, end):
        self.name = name
        self.line = line
        self.start = start
        self.end = end
        self.length = int(end) - int(start) + 1
        self.elements = []
        self.type = 'array'
        self.id = name

    def __repr__(self):
        return f"{self.name}({self.start}:{self.end})"


class ArrElem:
    def __init__(self, arr_name, line, index):
        self.arr_name = arr_name
        self.line = line
        self.index = index
        self.is_initialized = False
        self.type = 'array'

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


class Condition:
    def __init__(self, left, op, right, line):
        self.left = left
        self.right = right
        self.op = op
        self.line = line

    def __repr__(self):
        return f"{self.left} {self.op} {self.right}"


class IfThen:
    def __init__(self, condition: Condition, commands, line):
        self.condition = condition
        self.commands = commands
        self.line = line

    def __repr__(self):
        r = f"if {self.condition} then\n"
        for c in self.commands:
            r += f"{c}\n"
        r += "endif"
        return r


class IfThenElse:
    def __init__(self, condition: Condition, commands, else_commands, line):
        self.condition = condition
        self.commands = commands
        self.else_commands = else_commands
        self.line = line

    def __repr__(self):
        r = f"if {self.condition} then\n"
        for c in self.commands:
            r += f"{c}\n"
        r += "else \n"
        for ec in self.else_commands:
            r += f"{ec}\n"
        r += "endif"
        return r


class While:
    def __init__(self, condition: Condition, commands, line):
        self.condition = condition
        self.commands = commands
        self.line = line

    def __repr__(self):
        r = f"while {self.condition} do\n"
        for c in self.commands:
            r += f"{c}\n"
        r += "endwhile"
        return r


class Repeat:
    def __init__(self, condition: Condition, commands, line):
        self.condition = condition
        self.commands = commands
        self.line = line

    def __repr__(self):
        r = f"repeat \n"
        for c in self.commands:
            r += f"{c}\n"
        r += f"until {self.condition};\n"
        return r


class ForTo:
    def __init__(self, iterator, start, end, commands, line):
        self.iterator = iterator
        self.start = start
        self.end = end
        self.commands = commands
        self.line = line

    def __repr__(self):
        r = f"for {self.iterator} from {self.start} to {self.end} do \n"
        for c in self.commands:
            r += f"{c}\n"
        r += "endfor"
        return r


class ForDownTo:
    def __init__(self, iterator, start, end, commands, line):
        self.iterator = iterator
        self.start = start
        self.end = end
        self.commands = commands
        self.line = line

    def __repr__(self):
        r = f"for {self.iterator} from {self.start} downto {self.end} do \n"
        for c in self.commands:
            r += f"{c}\n"
        r += "endfor"
        return r
