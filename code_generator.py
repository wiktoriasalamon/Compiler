class CodeGenerator:

    def __init__(self):
        self.code = ''

    def gen_const(self, reg, num):
        self.code += f'(generate {num})\n'
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
        self.code += gen_const_code

    def assign_value(self, help_reg1, help_reg2, mem_index, value):
        self.gen_const(help_reg1, mem_index)
        self.gen_const(help_reg2, value)
        self.code += f'(Store {value} in memory cell {mem_index})\n'
        self.code += f"STORE {help_reg2} {help_reg1}\n"

    def assign_value_from_register(self, reg_with_value, help_reg, mem_index):
        self.gen_const(help_reg, mem_index)
        self.code += f'(Store value from register {reg_with_value} in memory cell {mem_index})\n'
        self.save_val(help_reg, reg_with_value)

    def load_var(self, mem_index, reg):
        self.gen_const(reg, mem_index)
        self.code += f"LOAD {reg} {reg}\n"

    def load(self, reg_for_value, reg_with_mem_cell):
        self.code += f"LOAD {reg_for_value} {reg_with_mem_cell}\n"

    def add(self, reg1, reg2):
        self.code += f"ADD {reg1} {reg2}\n"
                  #   f"STORE {reg1} {result_reg}"

    def subtract(self, reg1, reg2):
        self.code += f"SUB {reg1} {reg2}\n"

    def divide(self, reg1, reg2, reg3, reg4, reg5):
        self.code += f"RESET {reg4} \n" \
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
        self.copy(reg4, reg1)

    def modulo(self, reg1, reg2, reg3, reg4, reg5):
        self.code += f"JZERO {reg2} 24 \n" \
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

    def multiply(self, reg1, reg2, reg3):
        self.code += f"RESET {reg3}\n" \
                     f"JODD {reg2} 2\n" \
                     f"JUMP 2\n" \
                     f"ADD {reg3} {reg1}" \
                     f"SHL {reg1}\n" \
                     f"SHR {reg2}\n" \
                     f"JZERO {reg2} 2\n" \
                     f"JUMP -6\n"
        self.copy(reg3, reg1)

    def write(self, reg):
        self.code += f"PUT {reg}\n"

    def read(self, reg):
        self.code += f"GET {reg}\n"

    def save_val(self, reg_mem_index, reg):
        # self.gen_const(help_reg, mem_index)
        self.code += f"STORE {reg} {reg_mem_index}\n"

    def end_program(self):
        self.code += "HALT\n"

    def copy(self, from_reg, to_reg):
        self.code += f"RESET {to_reg}\n" \
                     f"ADD {to_reg} {from_reg}\n"


if __name__ == "__main__":
    generator = CodeGenerator()
    generator.gen_const(21, 'a')
    print(generator.code)