from sly import Lexer


class CompilerLex(Lexer):
    tokens = {
        DECLARE, BEGIN, END,

        IF, THEN, ELSE, ENDIF,
        WHILE, DO, ENDWHILE,
        REPEAT, UNTIL,
        FOR, FROM, TO, DOWNTO, ENDFOR,

        READ, WRITE,

        PLUS, MINUS, TIMES, DIVIDE, MODULO,
        EQUALS, NOT_EQUALS, LESS_THAN, GREATER_THAN,
        LESS_EQUALS, GREATER_EQUALS,

        COLON, SEMICOLON, COMMA,
        LEFT_PAREN, RIGHT_PAREN,
        ASSIGN,

        PIDENTIFIER, NUMBER
    }

    ENDIF = r'ENDIF'
    IF = r'IF'
    THEN = r'THEN'
    ELSE = r'ELSE'

    DOWNTO = r'DOWNTO'
    ENDFOR = r'ENDFOR'
    FOR = r'FOR'
    FROM = r'FROM'
    TO = r'TO'

    ENDWHILE = r'ENDWHILE'
    WHILE = r'WHILE'
    DO = r'DO'

    DECLARE = r'DECLARE'
    BEGIN = r'BEGIN'
    END = r'END'

    REPEAT = r'REPEAT'
    UNTIL = r'UNTIL'

    READ = r'READ'
    WRITE = r'WRITE'

    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    MODULO = r'%'

    EQUALS = r'='
    NOT_EQUALS = r'!='
    LESS_EQUALS = r'<='
    GREATER_EQUALS = r'>='
    LESS_THAN = r'<'
    GREATER_THAN = r'>'

    ASSIGN = r':='  # MUST APPEAR FIRST! (LONGER)
    COLON = r':'
    SEMICOLON = r';'
    COMMA = r','
    LEFT_PAREN = r'\('
    RIGHT_PAREN = r'\)'

    PIDENTIFIER = r'[_a-z]+'
    NUMBER = r'\d+'

    ignore = ' \t\r'
    ignore_comment = r'\[[^\]]*\]'

    # Tracks line numbers
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    # Error handling
    def error(self, t):
        print('Line %d: Illegal character %r' % (self.lineno, t.value[0]))
        self.index += 1
