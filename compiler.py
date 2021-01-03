import re

from compiler_classes import *
import code_generator as g
from exceptions import *

PUT_MEMORY_CELL = 'put_memory_cell'


def count_commands(dirty_code):
    code = re.sub(r'\([-_A-Za-z0-9\s]*\)+\n?', '', dirty_code)
    TOKENS = ['GET', 'PUT', 'LOAD', 'STORE', 'ADD', 'SUB', 'RESET', 'INC', 'DEC', 'SHR', 'SHL', 'JUMP', 'JZERO', 'JODD']
    count = 0
    for t in TOKENS:
        count += len(list(re.finditer(t, code)))
    return count


class Compiler:

    def __init__(self, tree):
        self.variables = {}
        self.mem_indexes = {}
        self.next_free_memory_index = 0
        self.tree = tree

        self.mem_indexes[PUT_MEMORY_CELL] = self.next_free_memory_index
        self.next_free_memory_index += 1

    def compile(self):
        code = self.walk_tree(self.tree)
        code += g.end_program()
        return code

    def walk_tree(self, node):
        if node is None:
            return ''

        code = ''

        if isinstance(node, Program):
            if node.declarations is None:
                for c in node.commands:
                    code += self.walk_tree(c)
            else:
                for d in node.declarations:
                    code += self.walk_tree(d)
                for c in node.commands:
                    code += self.walk_tree(c)

        if isinstance(node, Var) or isinstance(node, Arr):
            code += self.declare_variable(node)

        if isinstance(node, Assign):
            code += self.assign_to_var(node)

        if isinstance(node, Read):
            code += self.read(node)

        if isinstance(node, Write):
            code += self.write(node)

        if isinstance(node, IfThen):
            code += self.if_then(node)

        if isinstance(node, IfThenElse):
            code += self.if_then_else(node)

        if isinstance(node, While):
            code += self.while_loop(node)

        if isinstance(node, Repeat):
            code += self.repeat_loop(node)

        if isinstance(node, ForTo):
            code += self.for_to_loop(node)

        if isinstance(node, ForDownTo):
            code += self.for_downto_loop(node)

        return code

    def declare_variable(self, var):
        if var.id in self.variables:
            raise VariableAlreadyDeclared(var.line, var.name)

        if isinstance(var, Var):
            self.variables[var.id] = var
            self.mem_indexes[var.id] = self.next_free_memory_index
            self.next_free_memory_index += 1

        elif isinstance(var, Arr):
            if int(var.start) > int(var.end):
                raise InvalidArrayRange(var.line, var.name)

            self.variables[var.id] = var
            self.mem_indexes[var.id] = self.next_free_memory_index
            self.next_free_memory_index += var.length

        print('declare', var)
        return ''

    def get_variable(self, var):
        name = ''
        if isinstance(var, Var) or isinstance(var, Arr):
            name = var.id
        elif isinstance(var, ArrElem):
            name = var.arr_name

        # check if variable is declared
        if name not in self.variables:
            raise VariableNotDeclared(var.line, name)

        variable = self.variables[name]

        # check invalid usage
        if variable.type != var.type:
            raise InvalidUsageOfVariable(var.line, name, variable.type)

        # check if variable is covered
        if isinstance(variable, Var):
            variable = self.get_covering_var(variable)

        return variable

    def assign(self, command: Assign):
        code = ''

        # save expr in register 'a'
        if isinstance(command.expr, BinaryOp):
            # assign expression to variable
            code += self.expression(command.expr)
        elif isinstance(command.expr, ArrElem):
            # assign array element to variable
            code += self.load_var_to_register(command.expr, 'a', 'b')
        elif isinstance(command.expr, Var):
            # assign variable to variable
            self.check_is_var_initialized(command.expr)
            expr_mem_index = self.get_mem_index(command.expr)
            code += g.load_var(expr_mem_index, 'a')
        else:
            # assign constant to variable
            code += g.gen_const('a', int(command.expr))

        # get variable memory cell to register b
        if isinstance(command.var, Var):
            # var =
            var_mem_index = self.get_mem_index(command.var)
            code += g.gen_const('b', var_mem_index)
        elif isinstance(command.var, ArrElem) \
                and isinstance(command.var.index, Var):
            # tab(i) =
            code += self.get_memory_cell_to_reg(command.var, 'b', 'c')
        else:
            # tab(1) =
            var_mem_index = self.get_mem_index(command.var)
            code += g.gen_const('b', var_mem_index)

        # save register a in memory cell stored in register b
        code += g.save_val('b', 'a')

        self.initialize_var(command.var)

        print(command)

        return code

    def assign_to_var(self, command: Assign):
        var = self.get_variable(command.var)

        if isinstance(var, Var):
            if not var.is_global:
                raise IteratorCannotBeModified(command.line, command.var.name)
        return self.assign(command)

    def expression(self, expr: BinaryOp):
        code = ''
        code += self.load_var_to_register(expr.left, 'a', 'c')
        code += self.load_var_to_register(expr.right, 'b', 'c')

        if expr.op == "+":
            code += g.add('a', 'b')
        elif expr.op == "-":
            code += g.subtract('a', 'b')
        elif expr.op == "*":
            code += g.multiply('a', 'b', 'c')
        elif expr.op == "/":
            code += g.divide('a', 'b', 'c', 'd', 'e')
        elif expr.op == "%":
            code += g.modulo('a', 'b', 'c', 'd', 'e')

        return code

    def read(self, command: Read):
        code = ''
        if isinstance(command.var, ArrElem) \
                and isinstance(command.var.index, Var):
            var = self.get_variable(command.var.index)
            code += self.get_memory_cell_to_reg(var, 'a', 'b')
        else:
            mem_index = self.get_mem_index(command.var)
            code += g.gen_const('a', mem_index)
        code += g.read('a')
        self.initialize_var(command.var)

        print(command)
        return code

    def write(self, command: Write):
        code = ''
        self.check_is_var_initialized(command.value)
        if isinstance(command.value, str):  # command.value is number
            code += g.gen_const('a', int(command.value))
            code += g.gen_const('b', self.mem_indexes[PUT_MEMORY_CELL])
            code += g.save_val('b', 'a')
            code += g.write('b')
        elif isinstance(command.value, ArrElem) \
                and isinstance(command.value.index, Var):
            code += self.get_memory_cell_to_reg(command.value, 'a', 'b')
            code += g.write('a')
        elif isinstance(command.value, Var) \
                or isinstance(command.value, ArrElem):
            mem_index = self.get_mem_index(command.value)
            code += g.gen_const('a', mem_index)
            code += g.write('a')

        print(command)
        return code

    def condition(self, cond: Condition):
        code = ''
        code += self.load_var_to_register(cond.left, 'b', 'a')
        code += self.load_var_to_register(cond.right, 'c', 'a')

        # result of condition is in register 'a'
        if cond.op == "=":
            code += g.equal('b', 'c', 'a')
        elif cond.op == "!=":
            code += g.not_equal('b', 'c', 'a')
        elif cond.op == "<":
            code += g.less('b', 'c', 'a')
        elif cond.op == ">":
            code += g.greater('b', 'c', 'a')
        elif cond.op == "<=":
            code += g.less_equal('b', 'c', 'a')
        elif cond.op == '>=':
            code += g.greater_equal('b', 'c', 'a')

        return code

    def if_then(self, command: IfThen):
        # result of condition is in register a
        condition_code = self.condition(command.condition)

        commands_code = ''
        for c in command.commands:
            commands_code += self.walk_tree(c)

        commands_lines = count_commands(commands_code)
        code = condition_code
        code += g.jump_if_zero('a', commands_lines + 1)
        code += commands_code

        print(command)
        return code

    def if_then_else(self, command: IfThenElse):
        # result of condition is in register a
        condition_code = self.condition(command.condition)

        commands_code = ''
        for c in command.commands:
            commands_code += self.walk_tree(c)

        else_commands_code = ''
        for c in command.else_commands:
            else_commands_code += self.walk_tree(c)

        commands_lines = count_commands(commands_code)
        else_commands_lines = count_commands(else_commands_code)

        code = condition_code
        code += g.jump_if_zero('a', commands_lines + 2)
        code += commands_code
        code += g.jump(else_commands_lines + 1)
        code += else_commands_code

        print(command)
        return code

    def while_loop(self, command: While):
        # result of condition is in register a
        condition_code = self.condition(command.condition)

        commands_code = ''
        for c in command.commands:
            commands_code += self.walk_tree(c)

        condition_lines = count_commands(condition_code)
        commands_lines = count_commands(commands_code)

        code = condition_code
        code += g.jump_if_zero('a', commands_lines + 2)
        code += commands_code
        code += g.jump(-(commands_lines + condition_lines + 1))

        print(command)
        return code

    def repeat_loop(self, command: Repeat):
        # result of condition is in register a
        condition_code = self.condition(command.condition)

        commands_code = ''
        for c in command.commands:
            commands_code += self.walk_tree(c)

        condition_lines = count_commands(condition_code)
        commands_lines = count_commands(commands_code)

        code = commands_code
        code += condition_code
        code += g.jump_if_zero('a', -(condition_lines + commands_lines))

        print(command)
        return code

    def for_to_loop(self, command: ForTo):
        # end of iterations
        end_for_name = command.iterator.id + '_end'
        end_for_var = Var(end_for_name, command.line)
        self.declare_variable(end_for_var)
        # end_for = command.end
        code = self.assign(
            Assign(
                end_for_var,
                command.end,
                command.line
            )
        )
        # iterator = command.start
        self.add_iterator(command.iterator)
        iterator = self.get_variable(command.iterator)
        code += self.assign(
            Assign(
                iterator,
                command.start,
                command.line
            )
        )

        commands_code = ''
        for c in command.commands:
            commands_code += self.walk_tree(c)

        # increase iterator by 1 and save it
        increasing_code = ''
        increasing_code += self.load_var_to_register(iterator, 'f', 'e')
        increasing_code += g.increase('f')
        iterator_mem_index = self.get_mem_index(iterator)
        increasing_code += g.gen_const('e', iterator_mem_index)
        increasing_code += g.save_val('e', 'f')

        # check if iterator <= end
        condition_code = self.condition(
            Condition(
                iterator,
                '<=',
                end_for_var,
                command.line
            )
        )

        increasing_lines = count_commands(increasing_code)
        commands_lines = count_commands(commands_code)
        condition_lines = count_commands(condition_code)

        code += condition_code
        code += g.jump_if_zero('a', commands_lines + increasing_lines + 2)
        code += commands_code
        code += increasing_code
        code += g.jump(-(increasing_lines + commands_lines + condition_lines + 1))

        self.delete_iterator(iterator)
        self.delete_iterator(end_for_var)

        print(command)
        return code

    def for_downto_loop(self, command: ForDownTo):
        # end of iterations
        end_for_name = command.iterator.id + '_end'
        end_for_var = Var(end_for_name, command.line)
        self.declare_variable(end_for_var)

        # end_for = end + 1
        code = self.assign(
            Assign(
                end_for_var,
                BinaryOp(
                    command.end,
                    '+',
                    1,
                    command.line
                ),
                command.line
            )
        )

        self.add_iterator(command.iterator)
        iterator = self.get_variable(command.iterator)

        # iterator = start + 1
        code += self.assign(
            Assign(
                iterator,
                BinaryOp(
                    command.start,
                    '+',
                    1,
                    command.line
                ),
                command.line
            )
        )

        commands_code = ''
        for c in command.commands:
            commands_code += self.walk_tree(c)

        # decrease iterator by 1 and save it
        decreasing_code = ''
        decreasing_code += self.load_var_to_register(iterator, 'f', 'e')
        decreasing_code += g.decrease('f', 'e')
        iterator_mem_index = self.get_mem_index(iterator)
        decreasing_code += g.gen_const('e', iterator_mem_index)
        decreasing_code += g.save_val('e', 'f')

        # check if iterator >= end
        condition_code = self.condition(
            Condition(
                iterator,
                '>=',
                end_for_var,
                command.line
            )
        )

        decreasing_lines = count_commands(decreasing_code)
        commands_lines = count_commands(commands_code)
        condition_lines = count_commands(condition_code)

        code += condition_code
        code += g.jump_if_zero('a', commands_lines + decreasing_lines + 2)
        code += decreasing_code
        code += commands_code
        code += g.jump(-(decreasing_lines + commands_lines + condition_lines + 1))

        self.delete_iterator(iterator)
        self.delete_iterator(end_for_var)

        print(command)
        return code

    #  -------- helpers --------

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
            return self.mem_indexes[v.name]

        if isinstance(var, ArrElem):
            if isinstance(var.index, Var):
                raise VariableIndexError(var.line, var.arr_name)  # for this case you should use get_memory_cell_to_reg
            else:
                elem_id = int(var.index)
                arr = self.get_variable(var)
                if elem_id < int(arr.start) or elem_id > int(arr.end):
                    raise ArrayIndexOutOfRange(var.line, var.arr_name)
                arr_elem_mem_index = self.mem_indexes[arr.name] + elem_id - int(arr.start)
                return arr_elem_mem_index

    def load_var_to_register(self, var, register, help_reg):
        code = ''
        if isinstance(var, Var):
            mem_index = self.get_mem_index(var)
            self.check_is_var_initialized(var)
            code += g.load_var(mem_index, register)
        elif isinstance(var, ArrElem) and isinstance(var.index, Var):
            code += self.get_memory_cell_to_reg(var, register, help_reg)
            code += g.load(help_reg, register)
            code += g.copy(help_reg, register)
        elif isinstance(var, ArrElem):
            mem_index = self.get_mem_index(var)
            code += g.load_var(mem_index, register)
        else:
            code += g.gen_const(register, int(var))

        return code

    def get_memory_cell_to_reg(self, var: ArrElem, register, help_reg):
        # check if variable which is used as an index of the array is declared
        self.check_is_var_initialized(var.index)

        code = ''

        arr_mem_index = self.mem_indexes[var.arr_name]
        arr_id_mem_index = self.mem_indexes[var.index.name]
        code += g.gen_const(register, arr_mem_index)
        code += g.load_var(arr_id_mem_index, help_reg)
        code += g.add(register, help_reg)
        arr_offset = self.variables[var.arr_name].start
        code += g.gen_const(help_reg, arr_offset)
        code += g.subtract(register, help_reg)

        return code

    def add_iterator(self, var: Var):
        var.is_global = False

        # covering other variable
        if var.id in self.variables:
            var_to_cover: Var = self.get_variable(var)
            var_to_cover.is_covered = True
            var.id = "#" + var_to_cover.id
            var.var_covered = var_to_cover
            var.var_covering = var

        self.declare_variable(var)

    def delete_iterator(self, var: Var):
        var_to_delete = self.get_variable(var)

        if var_to_delete.var_covered is not None:
            var_covered = self.get_variable(var_to_delete.var_covered)
            var_covered.var_covering = None
            var_covered.is_covered = False

        self.variables.pop(var_to_delete.id)
        self.mem_indexes.pop(var_to_delete.id)

    def get_covering_var(self, var: Var):
        if not var.is_covered or \
                var.var_covering is None:
            return var
        return self.get_covering_var(var.var_covering)
