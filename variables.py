class Variable:
    def __init__(self, name, line):
        self.name = name
        self.line = line
        self.is_initialized = False

    def get_initialization(self):
        return self.is_initialized()

    def set_initialization(self):
        self.is_initialized = True


class Integer(Variable):
    def __init__(self, name, line):
        self.value = None
        super().__init__(name, line)

    def set_value(self, value):
        self.value = value
        self.set_initialization()


class Array(Variable):
    def __init__(self, name, line, start_index, end_index):
        self.start_index = start_index
        self.end_index = end_index
        self.length = end_index - start_index + 1
        super().__init__(name, line)

