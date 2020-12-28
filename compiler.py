from helpers import *
from code_generator import CodeGenerator
from exceptions import *

PUT_MEMORY_CELL = 'put_memory_cell'


class Compiler:

    def __init__(self, tree):
        self.variables = {}
        self.arrays = {}
        self.var_mem_indexes = {}
        self.arr_mem_indexes = {}
        self.next_free_memory_index = 0
        self.g = CodeGenerator()
        self.tree = tree

        self.var_mem_indexes[PUT_MEMORY_CELL] = self.next_free_memory_index
        self.next_free_memory_index += 1

    def compile(self):
        self.walk_tree(self.tree)
        self.g.end_program()

        return self.g.code

    def declare_variable(self, var):
        if isinstance(var, Var):
            if var.name in self.variables:
                raise VariableAlreadyDeclared(var.line, var.name)

            self.variables[var.name] = var
            self.var_mem_indexes[var.name] = self.next_free_memory_index
            self.next_free_memory_index += 1

        elif isinstance(var, Arr):
            if var.name in self.arrays:
                raise ArrayAlreadyDeclared(var.line, var.name)

            if int(var.start) > int(var.end):
                raise InvalidArrayRange(var.line, var.name)

            self.arrays[var.name] = var
            self.arr_mem_indexes[var.name] = self.next_free_memory_index
            self.next_free_memory_index += var.length

        print('declare', var)

    def get_variable(self, var):
        if isinstance(var, Var):
            if var.name not in self.variables:
                raise VariableNotDeclared(var.line, var.name)
            else:
                return self.variables[var.name]
        if isinstance(var, ArrElem):
            if var.arr_name not in self.arrays:
                raise ArrayNotDeclared(var.line, var.arr_name)
            else:
                return self.arrays[var.arr_name]


    def binary_op(self, operation: BinaryOp):
        print(operation)

    def assign(self, command: Assign):

        # save expr in register 'a'
        if isinstance(command.expr, BinaryOp):
            # assign expression to variable
            result_of_expr_reg = 'a'
            second_operand_register = 'b'
            help_reg = 'c'
            self.expression(
                command.expr
            )
        elif isinstance(command.expr, ArrElem):
            # assign array element to variable
            self.load_var_to_register(command.expr, 'a', 'b')
        elif isinstance(command.expr, Var):
            # assign variable to variable
            self.check_is_var_initialized(command.expr)
            expr_mem_index = self.get_mem_index(command.expr)
            self.g.load_var(expr_mem_index, 'a')
        else:
            # assign constant to variable
            self.g.gen_const('a', int(command.expr))

        # get variable memory cell to register b
        if isinstance(command.var, Var):
            # var =
            var_mem_index = self.get_mem_index(command.var)
            self.g.gen_const('b', var_mem_index)
        elif isinstance(command.var, ArrElem) \
                and isinstance(command.var.index, Var):
            # tab(i) =
            self.get_memory_cell_to_reg(command.var, 'b', 'c')
        else:
            # tab(1) =
            var_mem_index = self.get_mem_index(command.var)
            self.g.gen_const('b', var_mem_index)

        # save register a in memory cell stored in register b
        self.g.save_val('b', 'a')

        self.initialize_var(command.var)

        print(command)

    def load_var_to_register(self, var, register, help_reg):
        if isinstance(var, Var):
            mem_index = self.get_mem_index(var)
            self.check_is_var_initialized(var)
            self.g.load_var(mem_index, register)
        elif isinstance(var, ArrElem) and isinstance(var.index, Var):
            self.get_memory_cell_to_reg(var, register, help_reg)
            self.g.load(help_reg, register)
            self.g.copy(help_reg, register)
        elif isinstance(var, ArrElem):
            mem_index = self.get_mem_index(var)
            self.g.load_var(mem_index, register)
        else:
            self.g.gen_const(register, int(var))

    def expression(self, expr: BinaryOp):
        self.load_var_to_register(expr.left, 'a', 'd')
        self.load_var_to_register(expr.right, 'c', 'd')

        if expr.op == "+":
            self.g.add('a', 'c')
        elif expr.op == "-":
            self.g.subtract('a', 'c')
        elif expr.op == "*":
            self.g.multiply('a', 'c', 'd')
        elif expr.op == "/":
            self.g.divide('a', 'c', 'd', 'e', 'f')
        elif expr.op == "%":
            self.g.modulo('a', 'c', 'd', 'e', 'f')

    def read(self, command: Read):
        if isinstance(command.var, ArrElem) \
                and isinstance(command.var.index, Var):
            var = self.get_variable(command.var)
            self.get_memory_cell_to_reg(var, 'a', 'b')
        else:
            mem_index = self.get_mem_index(command.var)
            self.g.gen_const('a', mem_index)
        self.g.read('a')
        self.initialize_var(command.var)

    def get_memory_cell_to_reg(self, var: ArrElem, register, help_reg):
        arr_mem_index = self.arr_mem_indexes[var.arr_name]
        arr_id_mem_index = self.var_mem_indexes[var.index.name]
        self.g.gen_const(register, arr_mem_index)
        self.g.load_var(arr_id_mem_index, help_reg)
        self.g.add(register, help_reg)
        arr_offset = self.arrays[var.arr_name].start
        self.g.gen_const(help_reg, arr_offset)
        self.g.subtract(register, help_reg)

    def write(self, command: Write):
        self.check_is_var_initialized(command.value)
        if isinstance(command.value, str):  # command.value is number
            self.g.gen_const('a', int(command.value))
            self.g.gen_const('b', self.var_mem_indexes[PUT_MEMORY_CELL])
            self.g.save_val('b', 'a')
            self.g.write('b')

        elif isinstance(command.value, Var) \
                or isinstance(command.value, ArrElem):
            mem_index = self.get_mem_index(command.value)
            self.g.gen_const('a', mem_index)
            self.g.write('a')
            print(command)

    def initialize_var(self, var):
        if isinstance(var, Var):
            v = self.get_variable(var)
            v.is_initialized = True

    def check_is_var_initialized(self, var):
        if isinstance(var, Var):
            v: Var
            v = self.get_variable(var)
            if not v.is_initialized:
                raise VariableNotInitialized(var.line, var.name)
        else:
            return

    def get_mem_index(self, var):
        if isinstance(var, Var):
            v = self.get_variable(var)
            return self.var_mem_indexes[v.name]

        if isinstance(var, ArrElem):
            if isinstance(var.index, Var):
                raise VariableIndexError(var.line, var.arr_name)  # TODO ????????? robie to w innym miejscu
            else:
                elem_id = int(var.index)
                arr = self.get_variable(var)
                if elem_id < int(arr.start) or elem_id > int(arr.end):
                    raise ArrayIndexOutOfRange(var.line, var.arr_name)
                arr_elem_mem_index = self.arr_mem_indexes[arr.name] + elem_id - int(arr.start)
                return arr_elem_mem_index

    def walk_tree(self, node):
        if node is None:
            return None

        if isinstance(node, Program):
            if node.declarations is None:
                for c in node.commands:
                    self.walk_tree(c)
            else:
                for d in node.declarations:
                    self.walk_tree(d)
                for c in node.commands:
                    self.walk_tree(c)

        if isinstance(node, Var) or isinstance(node, Arr):
            self.declare_variable(node)

        if isinstance(node, BinaryOp):
            self.binary_op(node)

        if isinstance(node, Assign):
            self.assign(node)

        if isinstance(node, Read):
            self.read(node)

        if isinstance(node, Write):
            self.write(node)
