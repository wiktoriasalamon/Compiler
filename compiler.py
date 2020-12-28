from helpers import *
from code_generator import CodeGenerator
from exceptions import *

PUT_MEMORY_CELL = 'put_memory_cell'


class Compiler:

    def __init__(self, tree):
        self.variables = {}
        self.memory_indexes = {}
        self.next_free_memory_index = 0
        self.g = CodeGenerator()
        self.tree = tree

        self.memory_indexes[PUT_MEMORY_CELL] = self.next_free_memory_index
        self.next_free_memory_index += 1

    def compile(self):
        self.walk_tree(self.tree)
        self.g.end_program()

        print('---------------')
        for i in self.memory_indexes.keys():
            print(i, self.memory_indexes[i])

        return self.g.code

    def declare_variable(self, var):
        # TODO może istnieć zmienna o tej samej nazwie co nazwa tablicy
        if var.name in self.variables:
            raise VariableAlreadyDeclared(f'Line {var.line}: Variable "{var.name}" was already declared')

        if isinstance(var, Arr):
            if int(var.start) > int(var.end):
                raise InvalidArrayRange(f'Line {var.line}: Invalid range of array "{var.name}"')

        self.variables[var.name] = var
        self.memory_indexes[var.name] = self.next_free_memory_index

        if isinstance(var, Var):
            self.next_free_memory_index += 1
        elif isinstance(var, Arr):
            self.next_free_memory_index += var.length

        print('declare', var)

    def get_variable(self, name, line):
        if name not in self.variables:
            # TODO: stop compilation or sth
            raise VariableNotDeclared(f'Line {line}: Variable "{name}" is not declared')

        return self.variables[name]

    def binary_op(self, operation: BinaryOp):
        print(operation)

    def assign(self, command: Assign):
        mem_index = self.get_mem_index(command.var)
        if isinstance(command.expr, BinaryOp):
            result_of_expr_reg = 'a'
            second_operand_register = 'b'
            help_reg = 'c'
            self.expression(result_of_expr_reg, second_operand_register, help_reg, command.expr)
            self.g.assign_value_from_register(result_of_expr_reg, 'b', mem_index)
        elif isinstance(command.expr, ArrElem) \
                or isinstance(command.expr, Var):
            self.check_is_var_initialized(command.expr)
            expr_mem_index = self.get_mem_index(command.expr)
            self.g.load_var(expr_mem_index, 'a')
            var_mem_index = self.get_mem_index(command.var)
            self.g.assign_value_from_register('a', 'b', var_mem_index)
        else:
            self.g.assign_value('a', 'b', mem_index, int(command.expr))

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

    def expression(self, result_register, second_operand_reg, help_reg, expr: BinaryOp):
        self.load_var_to_register(expr.left, result_register, help_reg)
        self.load_var_to_register(expr.right, second_operand_reg, help_reg)
        if expr.op == "+":
            self.g.add(result_register, second_operand_reg)
        elif expr.op == "-":
            self.g.subtract(result_register, second_operand_reg)
        elif expr.op == "*":
            self.g.multiply()
        elif expr.op == "/":
            self.g.divide()
        elif expr.op == "%":
            self.g.modulo()

    def read(self, command: Read):
        if isinstance(command.var, ArrElem) \
                and isinstance(command.var.index, Var):
            var = self.get_variable(command.var.arr_name, command.line)
            self.get_memory_cell_to_reg(var, 'a', 'b')
        else:
            mem_index = self.get_mem_index(command.var)
            self.g.gen_const('a', mem_index)
        self.g.read('a')
        self.initialize_var(command.var)

    def get_memory_cell_to_reg(self, var: ArrElem, register, help_reg):
        arr_mem_index = self.memory_indexes[var.arr_name]
        arr_id_mem_index = self.memory_indexes[var.index.name]
        self.g.gen_const(register, arr_mem_index)
        self.g.load_var(arr_id_mem_index, help_reg)
        self.g.add(register, help_reg)
        arr_offset = self.variables[var.arr_name].start
        self.g.gen_const(help_reg, arr_offset)
        self.g.subtract(register, help_reg)

    def write(self, command: Write):
        self.check_is_var_initialized(command.value)
        if isinstance(command.value, str):  # command.value is number
            self.g.gen_const('a', int(command.value))
            self.g.gen_const('b', self.memory_indexes[PUT_MEMORY_CELL])
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
            v = self.get_variable(var.name, var.line)
            v.is_initialized = True

    def check_is_var_initialized(self, var):
        if isinstance(var, Var):
            v: Var
            v = self.get_variable(var.name, var.line)
            if not v.is_initialized:
                raise VariableNotInitialized(f'Line {var.line}: Variable "{var.name}" is not initialized')
        else:
            return

    def get_mem_index(self, var):
        if isinstance(var, Var):
            v = self.get_variable(var.name, var.line)
            return self.memory_indexes[v.name]

        if isinstance(var, ArrElem):
            if isinstance(var.index, Var):
                raise VariableIndexError  # TODO ?????????
            else:
                elem_id = int(var.index)
                arr = self.get_variable(var.arr_name, var.line)
                arr_elem_mem_index = self.memory_indexes[arr.name] + elem_id - int(arr.start)
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
