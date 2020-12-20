from sly import Parser
from lexer import CompilerLexer

class CompilerParser(Parser):
    tokens = CompilerLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE)

    )

    @_('DECLARE declarations BEGIN commands END')
    def program(self, p):
        # TODO
        return ''

    @_('BEGIN commands END')
    def program(self, p):
        # TODO
        return ''

    @_('declarations COMMA PIDENTIFIER')
    def declarations(self, p):
        # TODO

    @_('declarations COMMA PIDENTIFIER LEFT_PAREN NUMBER COLON NUMBER RIGHT_PAREN')
    def declarations(self, p):
        # TODO

    @_('PIDENTIFIER')
    def declarations(self, p):
        # TODO

    @_('PIDENTIFIER LEFT_PAREN NUMBER COLON NUMBER RIGHT_PAREN')
    def declarations(self, p):
        # TODO

    @_('commands command')
    def commands(self, p):
        #TODO

    @_('command')
    def commands(self, p):
        #TODO

    @_('identifier ASSIGN expression SEMICOLON')
    def command(self, p):
        # TODO

    @_('IF condition THEN commands ELSE commands ENDIF')
    def command(self, p):
        #TODO

    @_('IF condition THEN commands ENDIF')
    def command(self, p):
        # TODO

    @_('WHILE condition DO commands ENDWHILE')
    def command(self, p):
        # TODO

    @_('REPEAT commands UNTIL condition SEMICOLON')
    def command(self, p):
        # TODO

    @_('FOR PIDENTIFIER FROM value TO value DO commands ENDFOR')
    def command(self, p):
        # TODO

    @_('FOR PIDENTIFIER FROM value DOWNTO value DO commands ENDFOR')
    def command(self, p):
        # TODO

    @_('READ identifier SEMICOLON')
    def command(self, p):
        # TODO

    @_('WRITE value SEMICOLON')
    def command(self, p):
        # TODO

    @_('value')
    def expression(self, p):
        return p.value

    @_('value PLUS value')
    def expression(self, p):
        return p[0] + p[2]

    @_('value MINUS value')
    def expression(self, p):
        return p[0] - p[2]

    @_('value TIMES value')
    def expression(self, p):
        return p[0] * p[2]

    @_('value DIVIDE value')
    def expression(self, p):
        return p[0] / p[2]

    @_('value MODULO value')
    def expression(self, p):
        return p[0] % p[2]

    @_('value EQUALS value')
    def condition(self, p):
        # TODO

    @_('value NOT_EQUALS value')
    def condition(self, p):
        # TODO

    @_('value LESS_THAN value')
    def condition(self, p):
        # TODO

    @_('value GREATER_THAN value')
    def condition(self, p):
        # TODO

    @_('value LESS_EQUALS value')
    def condition(self, p):
        # TODO

    @_('value GREATER_EQUALS value')
    def condition(self, p):
        # TODO

    @_('NUMBER')
    def value(self, p):
        return p.NUMBER

    @_('identifier')
    def value(self, p):
        # TODO

    @_('PIDENTIFIER')
    def identifier(self, p):
        # TODO

    @_('PIDENTIFIER LEFT_PAREN PIDENTIFIER RIGHT_PAREN')
    def identifier(self, p):
        # TODO

    @_('PIDENTIFIER LEFT_PAREN NUMBER RIGHT_PAREN')
    def identifier(self, p):
        # TODO
