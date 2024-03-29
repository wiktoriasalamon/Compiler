from sly import Parser
from lexer import CompilerLexer
from compiler_classes import *
from exceptions import InvalidCharacter


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
        return IfThenElse(p[1], p[3], p[5], p.lineno)

    @_('IF condition THEN commands ENDIF')
    def command(self, p):
        return IfThen(p[1], p[3], p.lineno)

    @_('WHILE condition DO commands ENDWHILE')
    def command(self, p):
        return While(p[1], p[3], p.lineno)

    @_('REPEAT commands UNTIL condition SEMICOLON')
    def command(self, p):
        return Repeat(p[3], p[1], p.lineno)

    @_('FOR PIDENTIFIER FROM value TO value DO commands ENDFOR')
    def command(self, p):
        return ForTo(
            Var(p[1], p.lineno),
            p[3],
            p[5],
            p[7],
            p.lineno
        )

    @_('FOR PIDENTIFIER FROM value DOWNTO value DO commands ENDFOR')
    def command(self, p):
        return ForDownTo(
            Var(p[1], p.lineno),
            p[3],
            p[5],
            p[7],
            p.lineno
        )

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
    @_('value NOT_EQUALS value')
    @_('value LESS_THAN value')
    @_('value GREATER_THAN value')
    @_('value LESS_EQUALS value')
    @_('value GREATER_EQUALS value')
    def condition(self, p):
        return Condition(p[0], p[1], p[2], p.lineno)

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

    def error(self, p):
        raise InvalidCharacter(p.lineno, p.value)
