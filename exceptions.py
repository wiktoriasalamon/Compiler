class VariableNotDeclared(Exception):
    def __init__(self, line, name):
        self.message = f"Line {line}: Variable '{name}' is not declared"
        super().__init__(self.message)


class ArrayNotDeclared(Exception):
    def __init__(self, line, name):
        self.message = f"Line {line}: Array '{name}' is not declared"
        super().__init__(self.message)


class VariableAlreadyDeclared(Exception):
    def __init__(self, line, name):
        self.message = f"Line {line}: Variable '{name}' was already declared"
        super().__init__(self.message)


class ArrayAlreadyDeclared(Exception):
    def __init__(self, line, name):
        self.message = f"Line {line}: Array '{name}' was already declared"
        super().__init__(self.message)


class InvalidArrayRange(Exception):
    def __init__(self, line, name):
        self.message = f"Line {line}: Invalid range of array '{name}'"
        super().__init__(self.message)


class InvalidUsageOfVariable(Exception):
    def __init__(self, line, name, var_type):
        self.message = f"Line {line}: Invalid usage of {var_type} '{name}'"
        super().__init__(self.message)


class VariableIndexError(Exception):
    def __init__(self, line, name):
        self.message = f"Line {line}: Niejawne użycie indeksu tablicy '{name}'"
        super().__init__(self.message)


class VariableNotInitialized(Exception):
    def __init__(self, line, name):
        self.message = f"Line {line}: Variable '{name}' is not initialized"
        super().__init__(self.message)


class ArrayIndexOutOfRange(Exception):
    def __init__(self, line, name):
        self.message = f"Line {line}: Index of array '{name}' is out of range"
        super().__init__(self.message)


class InvalidCharacter(Exception):
    def __init__(self, line, character):
        self.message = f"Line {line}: Invalid character '{character}'"
        super().__init__(self.message)


class IteratorCannotBeModified(Exception):
    def __init__(self, line, name):
        self.message = f"Line {line}: Iterator '{name}' cannot be modified"
        super().__init__(self.message)
