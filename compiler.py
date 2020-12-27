from helpers import *
from code_generator import CodeGenerator
from exceptions import *


class Compiler:

    def __init__(self, tree):
        self.variables = {}
        self.memory_indexes = {}
        self.next_free_memory_index = 0
        self.generator = CodeGenerator()
        self.tree = tree

        self.memory_indexes['put_memory_index'] = 0
        self.next_free_memory_index += 1

    def compile(self):
        self.walk_tree(self.tree)
        self.generator.end_program()

        print('---------------')
        for i in self.memory_indexes.keys():
            print(i, self.memory_indexes[i])

        return self.generator.code

    def declare_variable(self, var):
        # TODO może istnieć zmienna o tej samej nazwie co nazwa tablicy
        if var.name in self.variables:
            raise VariableAlreadyDeclared(f'Variable {var.name} was already declared (line {var.line})')

        if isinstance(var, Arr):
            if var.end < var.start:
                raise InvalidArrayRange(f'Invalid range of array {var.name} (line {var.line})')

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
            raise VariableNotDeclared(f'Variable {name} is not declared (line {line})')

        return self.variables[name]

    def binary_op(self, operation: BinaryOp):
        print(operation)

    def assign(self, command: Assign):
        try:
            mem_index = self.get_mem_index(command.var, command.line)

            if isinstance(command.expr, BinaryOp):
                result_of_expr_reg = 'a'
                self.expression(result_of_expr_reg, command.expr)
                self.generator.assign_value_from_register(result_of_expr_reg, 'b', mem_index)
            elif isinstance(command.expr, ArrElem):
                print('----------------------narazie nie wiem')
                expr_mem_index = self.get_mem_index(command.expr, command.line)
                self.generator.load_var(expr_mem_index, 'a')
                var_mem_index = self.get_mem_index(command.var, command.line)
                self.generator.assign_value_from_register('a', 'b', var_mem_index)
            else:
                # TODO registers management
                self.generator.assign_value('a', 'b', self.memory_indexes[command.var], int(command.expr))
        except ValueError:
            expr_mem_index = self.get_mem_index(command.expr, command.line)
            self.generator.load_var(expr_mem_index, 'a')
            var_mem_index = self.get_mem_index(command.var, command.line)
            self.generator.assign_value_from_register('a', 'b', var_mem_index)
        except VariableNotDeclared as vnd:
            print(vnd)
        except Exception as e:
            print('Exception1', e)

        print(command)

    def expression(self, result_register, expr: BinaryOp):
        if expr.op == "+":
            try:
                self.generator.gen_const(result_register, int(expr.left))
            except (ValueError, TypeError):
                try:
                    left_mem_index = self.get_mem_index(expr.left, expr.line)
                    self.generator.load_var(left_mem_index, result_register)
                except VariableNotDeclared as vnd:
                    print(vnd)
                    # TODO
                    pass

            try:
                self.generator.gen_const('b', int(expr.right))
                self.generator.add(result_register, 'b')
            except (ValueError, TypeError):
                try:
                    right_mem_index = self.get_mem_index(expr.right, expr.line)
                    self.generator.load_var(right_mem_index, 'b')
                    self.generator.add(result_register, 'b')
                except VariableNotDeclared as vnd:
                    print(vnd)
                    # TODO
                    pass

    def read(self, command: Read):
        print(command)

    def write(self, command: Write):
        try:
            self.generator.gen_const('a', int(command.value))
            self.generator.write('a')
        except (ValueError, TypeError):
            try:
                mem_index = self.get_mem_index(command.value, command.line)
                self.generator.gen_const('a', mem_index)
                self.generator.write('a')
                print(command)
            except VariableNotDeclared as e:
                print('Exception2', e)
            except VariableIndexError:
                # TODO
                pass

    def get_mem_index(self, var, line):
        print(var)
        try:
            if isinstance(var, ArrElem):
                if isinstance(var.index, Var):
                    raise VariableIndexError
                else:
                    elem_id = int(var.index)
                    arr = self.get_variable(var.arr_name, line)
                    return self.memory_indexes[arr.name] + elem_id - int(arr.start)
            else:
                print('is var')
                v = self.get_variable(var, line)
                print(self.memory_indexes[var])
                return self.memory_indexes[var]
        except VariableNotDeclared as e:
            raise e

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
            try:
                self.declare_variable(node)
            except Exception as e:
                print('Exception3', e)

        if isinstance(node, BinaryOp):
            self.binary_op(node)

        if isinstance(node, Assign):
            self.assign(node)

        if isinstance(node, Read):
            self.read(node)

        if isinstance(node, Write):
            self.write(node)
