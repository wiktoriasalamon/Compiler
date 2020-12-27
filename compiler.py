from helpers import *
from code_generator import CodeGenerator


class Compiler:

    def __init__(self, tree):
        self.variables = {}
        self.memory_indexes = {}
        self.next_free_memory_index = 0
        self.result = ""
        self.generator = CodeGenerator()
        self.tree = tree

        self.memory_indexes['put_memory_index'] = 0
        self.next_free_memory_index += 1

    def compile(self):
        self.walk_tree(self.tree)
        self.generator.end_program()

        if self.result != "":
            print(self.result)

        print('---------------')
        for i in self.memory_indexes.keys():
            print(i, self.memory_indexes[i])

        print('---------------')
        print(self.generator.code)
        return self.generator.code


    def declare_variable(self, var):
        if var.name in self.variables.keys():
            raise Exception(f'Variable {var.name} was already declared (line {var.line})')

        self.variables[var.name] = var
        self.memory_indexes[var.name] = self.next_free_memory_index

        if isinstance(var, Var):
            self.next_free_memory_index += 1
        elif isinstance(var, Arr):
            self.next_free_memory_index += var.length

        print(var)

    def get_variable(self, name, line):
        if name not in self.variables:
            # TODO: stop compilation or sth
            raise Exception(f'Variable {name} is not declared (line {line})')

        return self.variables[name]

    def binary_op(self, operation: BinaryOp):
        print(operation)

    def assign(self, command: Assign):
        try:
            var = self.get_variable(command.var, command.line)
            if isinstance(command.expr, BinaryOp):
                result_of_expr_reg = 'a'
                self.expression(result_of_expr_reg, command.expr)
                self.generator.assign_value_from_register(result_of_expr_reg, 'b', self.memory_indexes[command.var])
            else:
                # TODO registers management
                self.generator.assign_value('a', 'b', self.memory_indexes[command.var], int(command.expr))
        except Exception as e:
            print(e)

        print(command)

    def expression(self, result_register, expr: BinaryOp):
        if expr.op == "+":
            try:
                self.generator.gen_const(result_register, int(expr.left))
            except Exception as e:
                self.generator.load_var(self.memory_indexes[expr.left], result_register)

            try:
                self.generator.gen_const('b', int(expr.right))
            except Exception as e:
                self.generator.load_var(self.memory_indexes[expr.right], 'b')
            self.generator.add(result_register, 'b')

    def read(self, command: Read):

        print(command)

    def write(self, command: Write):
        try:
            self.generator.gen_const('a', int(command.value))
            self.generator.write('a')
        except Exception as e:
            self.generator.gen_const('a', self.memory_indexes[command.value])
            self.generator.write('a')
        print(command)

    def walk_tree(self, node):

        if node is None:
            return None

        if isinstance(node, Program):
            if node.declarations is None:
                self.walk_tree(node.commands)
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
