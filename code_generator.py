class CodeGenerator:

    def __init__(self):
        self.code = ''

    def gen_const(self, reg, num):
        gen_const_code = ''
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
        self.code += f"STORE {help_reg2} {help_reg1}\n"

    def assign_value_from_register(self, reg_with_value, help_reg, mem_index):
        self.gen_const(help_reg, mem_index)
        self.save_val(help_reg, reg_with_value)

    def load_var(self, mem_index, reg):
        self.gen_const(reg, mem_index)
        self.code += f"LOAD {reg} {reg}\n"

    def add(self, reg1, reg2):
        self.code += f"ADD {reg1} {reg2}\n"
                  #   f"STORE {reg1} {result_reg}"

    def write(self, reg):
        self.code += f"PUT {reg}\n"

    def save_val(self, mem_index, reg):
        self.code += f"STORE {reg} {mem_index}\n"

    def end_program(self):
        self.code += "HALT\n"


if __name__ == "__main__":
    generator = CodeGenerator()
    generator.gen_const(21, 'a')
    print(generator.code)