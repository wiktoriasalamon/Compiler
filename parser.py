from sly import Parser
from lexer import CompilerLexer

class CompilerParser(Parser):
    tokens = CompilerLexer.tokens

    def __init__(self):
        self.variables = {}
        self.memory_indexes = {}
        self.next_free_memory_index = 0

    def declare_variable(self, var: Variable):
        if var.name in self.variables.keys():
            declaration_line = self.variables[var.name].line
            raise Exception(f'Variable {var.name} was already declared in line {declaration_line} (line {var.line})')

        self.variables[var.name] = var
        self.memory_indexes[var.name] = self.next_free_memory_index
        if isinstance(var, Integer):
            self.next_free_memory_index += 1
        elif isinstance(var, Array):
            self.next_free_memory_index += var.length

    def get_variable(self, name, line):
        if name not in self.variables.keys():
            raise Exception(f'Variable {name} is not declared (line {line})')

        return self.variables[name]

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE)
    )

    @_('DECLARE declarations BEGIN commands END')
    def program(self, p):
        return [p[1], p[3]]

    @_('BEGIN commands END')
    def program(self, p):
        return [p[1]]

    # ---------------- DECLARATIONS ----------------

    @_('declarations COMMA PIDENTIFIER')
    def declarations(self, p):
        p[0] = list(p[0]) if p[0] else []
        #var = Integer(name=p[2], line=p.lineno)
        #self.declare_variable(var)
        #p[0].append(var)
        p[0].append(p[2])
        return p[0]

    @_('declarations COMMA PIDENTIFIER LEFT_PAREN NUMBER COLON NUMBER RIGHT_PAREN')
    def declarations(self, p):
        p[0] = list(p[0]) if p[0] else []
        #arr = Array(name=p[2], line=p.lineno, start_index=p[4], end_index=p[6])
        #self.declare_variable(arr)
        #p[0].append(arr)
        p[0].append([p[2], p[4], p[6]])
        return p[0]

    @_('PIDENTIFIER')
    def declarations(self, p):
        #var = Integer(name=p[0], line=p.lineno)
        #self.declare_variable(var)
        return list((p[0],))

    @_('PIDENTIFIER LEFT_PAREN NUMBER COLON NUMBER RIGHT_PAREN')
    def declarations(self, p):
        #arr = Array(name=p[0], line=p.lineno, start_index=p[2], end_index=p[4])
        #self.declare_variable(arr)
        return list(([p[0], p[2], p[4]],))

    # ---------------- COMMANDS ----------------

    @_('commands command')
    def commands(self, p):
        p[0] = list(p[0]) if p[0] else []
        p[0].append(p[1])
        return p[0]

    @_('command')
    def commands(self, p):
        return list((p[0],))

    # ---------------- COMMAND ----------------

    @_('identifier ASSIGN expression SEMICOLON')
    def command(self, p):
        try:
            #self.get_variable(name=p.identifier, line=p.lineno)
            #return "assign", p.identifier, p.expression
            return [p[0], ':=', p[2]]
        except Exception as e:
            print(e)
            pass

    @_('IF condition THEN commands ELSE commands ENDIF')
    def command(self, p):
        return ["if", p[1], 'then', p[3], 'else', p[5], 'endif']

    @_('IF condition THEN commands ENDIF')
    def command(self, p):
        return ["if", p[1], 'then', p[3], 'endif']

    @_('WHILE condition DO commands ENDWHILE')
    def command(self, p):
        return ["while", p[1], 'do', p[3], 'endwhile']

    @_('REPEAT commands UNTIL condition SEMICOLON')
    def command(self, p):
        return ["repeat", p[1], 'until', p[3], ';']

    @_('FOR PIDENTIFIER FROM value TO value DO commands ENDFOR')
    def command(self, p):
        return ["for", p[1], 'from', p[3], "to", p[5], 'do', p[7], 'endfor']

    @_('FOR PIDENTIFIER FROM value DOWNTO value DO commands ENDFOR')
    def command(self, p):
        return ["for", p[1], 'from', p[3], "downto", p[5], 'do', p[7], 'endfor']

    @_('READ identifier SEMICOLON')
    def command(self, p):
        return ['read', p[1]]

    @_('WRITE value SEMICOLON')
    def command(self, p):
        return ['write', p[1]]

    # ---------------- EXPRESSION ----------------

    @_('value')
    def expression(self, p):
        return p[0]

    @_('value PLUS value')
    def expression(self, p):
        #  return p[0] + p[2]
        return [p[0], '+', p[2]]

    @_('value MINUS value')
    def expression(self, p):
        # return p[0] - p[2]
        return [p[0], '-', p[2]]

    @_('value TIMES value')
    def expression(self, p):
        # return p[0] * p[2]
        return [p[0], '*', p[2]]

    @_('value DIVIDE value')
    def expression(self, p):
        # return p[0] / p[2]
        return [p[0], '/', p[2]]


    @_('value MODULO value')
    def expression(self, p):
        # return p[0] % p[2]
        return [p[0], '%', p[2]]


    # ---------------- CONDITION ----------------

    @_('value EQUALS value')
    def condition(self, p):
        return [p[0], '=', p[2]]

    @_('value NOT_EQUALS value')
    def condition(self, p):
        return [p[0], '!=', p[2]]

    @_('value LESS_THAN value')
    def condition(self, p):
        return [p[0], '<', p[2]]


    @_('value GREATER_THAN value')
    def condition(self, p):
        return [p[0], '>', p[2]]

    @_('value LESS_EQUALS value')
    def condition(self, p):
        return [p[0], '<=', p[2]]

    @_('value GREATER_EQUALS value')
    def condition(self, p):
        return [p[0], '>=', p[2]]

    # ---------------- VALUE ----------------

    @_('NUMBER')
    def value(self, p):
        return p[0]

    @_('identifier')
    def value(self, p):
        return p[0]

    # ---------------- IDENTIFIER ----------------

    @_('PIDENTIFIER')
    def identifier(self, p):
        return p[0]

    @_('PIDENTIFIER LEFT_PAREN PIDENTIFIER RIGHT_PAREN')
    def identifier(self, p):
        return [p[0],p[2]]

    @_('PIDENTIFIER LEFT_PAREN NUMBER RIGHT_PAREN')
    def identifier(self, p):
        return [p[0],p[2]]
