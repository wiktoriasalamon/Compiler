from sly import Parser
from lexer import CompilerLexer
from helpers import *


class CompilerParser(Parser):
    tokens = CompilerLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE)
    )

    @_('DECLARE declarations BEGIN commands END')
    def program(self, p):
        return Program(p[3], p[1])

    @_('BEGIN commands END')
    def program(self, p):
        return Program(p[1])

    # ---------------- DECLARATIONS ----------------

    @_('declarations COMMA PIDENTIFIER')
    def declarations(self, p):
        p[0] = list(p[0]) if p[0] else []
        p[0].append(Var(p[2], p.lineno))
        return p[0]

    @_('declarations COMMA PIDENTIFIER LEFT_PAREN NUMBER COLON NUMBER RIGHT_PAREN')
    def declarations(self, p):
        p[0] = list(p[0]) if p[0] else []
        p[0].append(Arr(p[2], p.lineno, p[4], p[6]))
        return p[0]

    @_('PIDENTIFIER')
    def declarations(self, p):
        return list((Var(p[0], p.lineno),))

    @_('PIDENTIFIER LEFT_PAREN NUMBER COLON NUMBER RIGHT_PAREN')
    def declarations(self, p):
        return list((Arr(p[0], p.lineno, p[2], p[4]),))

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
        return Assign(p[0], p[2], p.lineno)  # [p[0], ':=', p[2]]

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
        return Read(p[1], p.lineno)

    @_('WRITE value SEMICOLON')
    def command(self, p):
        return Write(p[1], p.lineno)

    # ---------------- EXPRESSION ----------------

    @_('value')
    def expression(self, p):
        return p[0]

    @_('value PLUS value')
    @_('value MINUS value')
    @_('value TIMES value')
    @_('value DIVIDE value')
    @_('value MODULO value')
    def expression(self, p):
        return BinaryOp(p[0], p[1], p[2], p.lineno)

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
        return Var(p[0], p.lineno)

    @_('PIDENTIFIER LEFT_PAREN PIDENTIFIER RIGHT_PAREN')
    def identifier(self, p):
        return ArrElem(p[0], p.lineno, Var(p[2], p.lineno))

    @_('PIDENTIFIER LEFT_PAREN NUMBER RIGHT_PAREN')
    def identifier(self, p):
        return ArrElem(p[0], p.lineno, p[2])
