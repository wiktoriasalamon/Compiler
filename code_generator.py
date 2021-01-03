def gen_const(reg, num):
    code = f'(generate {num})\n'
    gen_const_code = ''
    num = int(num)
    while num != 0:
        if num % 2 == 0:
            num = num // 2
            gen_const_code = f"SHL {reg}\n" + gen_const_code
        else:
            num = num - 1
            gen_const_code = f"INC {reg}\n" + gen_const_code
    gen_const_code = f"RESET {reg}\n" + gen_const_code
    code += gen_const_code
    return code


def assign_value(help_reg1, help_reg2, mem_index, value):
    code = gen_const(help_reg1, mem_index)
    code += gen_const(help_reg2, value)
    code += f'(Store {value} in memory cell {mem_index})\n'
    code += f"STORE {help_reg2} {help_reg1}\n"
    return code


def save_val(reg_mem_index, reg):
    # self.gen_const(help_reg, mem_index)
    code = f"STORE {reg} {reg_mem_index}\n"
    return code


def assign_value_from_register(reg_with_value, help_reg, mem_index):
    code = gen_const(help_reg, mem_index)
    code += f'(Store value from register {reg_with_value} in memory cell {mem_index})\n'
    code += save_val(help_reg, reg_with_value)


def load_var(mem_index, reg):
    code = gen_const(reg, mem_index)
    code += f"LOAD {reg} {reg}\n"
    return code


def load(reg_for_value, reg_with_mem_cell):
    code = f"LOAD {reg_for_value} {reg_with_mem_cell}\n"
    return code


def add(reg1, reg2):
    code = f"ADD {reg1} {reg2}\n"
    #   f"STORE {reg1} {result_reg}"
    return code


def subtract(reg1, reg2):
    code = f"SUB {reg1} {reg2}\n"
    return code


def copy(from_reg, to_reg):
    code = f"RESET {to_reg}\n" \
            f"ADD {to_reg} {from_reg}\n"
    return code


def divide(reg1, reg2, reg3, reg4, reg5):
    code = f"RESET {reg4} \n" \
                 f"JZERO {reg2} 23 \n" \
                 f"RESET {reg3} \n" \
                 f"INC {reg3} \n" \
                 f"RESET {reg5} \n" \
                 f"ADD {reg5} {reg2} \n" \
                 f"INC {reg5} \n" \
                 f"SUB {reg5} {reg1} \n" \
                 f"JZERO {reg5} 2 \n" \
                 f"JUMP 4 \n" \
                 f"SHL {reg2} \n" \
                 f"SHL {reg3} \n" \
                 f"JUMP -8 \n" \
                 f"RESET {reg5} \n" \
                 f"ADD {reg5} {reg2} \n" \
                 f"SUB {reg5} {reg1} \n" \
                 f"JZERO {reg5} 2 \n" \
                 f"JUMP 3 \n" \
                 f"SUB {reg1} {reg2} \n" \
                 f"ADD {reg4} {reg3} \n" \
                 f"SHR {reg2} \n" \
                 f"SHR {reg3} \n" \
                 f"JZERO {reg3} 2 \n" \
                 f"JUMP -10"
    code += copy(reg4, reg1)
    return code


def modulo(reg1, reg2, reg3, reg4, reg5):
    code = f"JZERO {reg2} 24 \n" \
         f"RESET {reg4} \n" \
         f"RESET {reg3} \n" \
         f"INC {reg3} \n" \
         f"RESET {reg5} \n" \
         f"ADD {reg5} {reg2} \n" \
         f"INC {reg5} \n" \
         f"SUB {reg5} {reg1} \n" \
         f"JZERO {reg5} 2 \n" \
         f"JUMP 4 \n" \
         f"SHL {reg2} \n" \
         f"SHL {reg3} \n" \
         f"JUMP -8 \n" \
         f"RESET {reg5} \n" \
         f"ADD {reg5} {reg2} \n" \
         f"SUB {reg5} {reg1} \n" \
         f"JZERO {reg5} 2 \n" \
         f"JUMP 3 \n" \
         f"SUB {reg1} {reg2} \n" \
         f"ADD {reg4} {reg3} \n" \
         f"SHR {reg2} \n" \
         f"SHR {reg3} \n" \
         f"JZERO {reg3} 3 \n" \
         f"JUMP -10\n" \
         f"RESET {reg1}"
    return code


def multiply(reg1, reg2, reg3):
    code = f"RESET {reg3} \n" \
           f"ADD {reg3} {reg1} \n" \
           f"INC {reg3} \n" \
           f"SUB {reg3} {reg2} \n" \
           f"JZERO {reg3} 2 \n" \
           f"JUMP 7 \n" \
           f"RESET {reg3} \n" \
           f"ADD {reg3} {reg2}" \
           f"RESET {reg2} \n" \
           f"ADD {reg2} {reg1} \n" \
           f"RESET {reg1} \n" \
           f"ADD {reg1} {reg3} \n" \
           f"RESET {reg3}" \
             f"JODD {reg2} 2\n" \
             f"JUMP 2\n" \
             f"ADD {reg3} {reg1}" \
             f"SHL {reg1}\n" \
             f"SHR {reg2}\n" \
             f"JZERO {reg2} 2\n" \
             f"JUMP -6\n"
    code += copy(reg3, reg1)
    return code


def write(reg):
    return f"PUT {reg}\n"


def read(reg):
    return f"GET {reg}\n"


def end_program():
    return "HALT\n"


# if reg1 < reg2
# reg3=1 -> true, reg3=0 -> false
def less(reg1, reg2, reg3):
    code = f"RESET {reg3}\n" \
            f"ADD {reg3} {reg1} \n" \
            f"INC {reg3} \n" \
            f"SUB {reg3} {reg2} \n" \
            f"JZERO {reg3} 3\n" \
            f"RESET {reg3} \n" \
            f"JUMP 3 \n" \
            f"RESET {reg3} \n" \
            f"INC {reg3} \n"

    return code


def less_equal(reg1, reg2, reg3):
    code = f"RESET {reg3}\n" \
           f"ADD {reg3} {reg1} \n" \
           f"SUB {reg3} {reg2} \n" \
           f"JZERO {reg3} 3\n" \
           f"RESET {reg3} \n" \
           f"JUMP 3 \n" \
           f"RESET {reg3} \n" \
           f"INC {reg3} \n"

    return code


def greater(reg1, reg2, reg3):
    code = f"RESET {reg3}\n" \
           f"ADD {reg3} {reg2} \n" \
           f"INC {reg3} \n" \
           f"SUB {reg3} {reg1} \n" \
           f"JZERO {reg3} 3\n" \
           f"RESET {reg3} \n" \
           f"JUMP 3 \n" \
           f"RESET {reg3} \n" \
           f"INC {reg3} \n"

    return code


def greater_equal(reg1, reg2, reg3):
    code = f"RESET {reg3}\n" \
           f"ADD {reg3} {reg2} \n" \
           f"SUB {reg3} {reg1} \n" \
           f"JZERO {reg3} 3\n" \
           f"RESET {reg3} \n" \
           f"JUMP 3 \n" \
           f"RESET {reg3} \n" \
           f"INC {reg3} \n"

    return code


def equal(reg1, reg2, reg3):
    code = f"RESET {reg3}\n" \
           f"ADD {reg3} {reg1} \n" \
           f"SUB {reg3} {reg2} \n" \
           f"JZERO {reg3} 2\n" \
           f"JUMP 5 \n" \
           f"RESET {reg3} \n" \
           f"ADD {reg3} {reg2} \n" \
           f"SUB {reg3} {reg1} \n" \
           f"JZERO {reg3} 3" \
           f"RESET {reg3} \n" \
           f"JUMP 3 \n" \
           f"RESET {reg3} \n" \
           f"INC {reg3} \n"

    return code


def not_equal(reg1, reg2, reg3):
    code = f"RESET {reg3}\n" \
           f"ADD {reg3} {reg1} \n" \
           f"SUB {reg3} {reg2} \n" \
           f"JZERO {reg3} 2\n" \
           f"JUMP 5 \n" \
           f"RESET {reg3} \n" \
           f"ADD {reg3} {reg2} \n" \
           f"SUB {reg3} {reg1} \n" \
           f"JZERO {reg3} 4" \
           f"RESET {reg3} \n" \
           f"INC {reg3} \n" \
           f"JUMP 2 \n" \
           f"RESET {reg3} \n"

    return code


def jump_if_zero(reg, jump_lines):
    return f"JZERO {reg} {jump_lines} \n"


def jump(jump_lines):
    return f"JUMP {jump_lines} \n"


def increase(reg):
    return f"INC {reg} \n"


def decrease(reg, help_reg):
    code = f"RESET {help_reg} \n" \
           f"INC {help_reg} \n" \

    code += subtract(reg, help_reg)

    return code
