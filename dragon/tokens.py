class Token:

    def __init__(self):
        raise NotImplementedError

    def __repr__(self):
        return f"tokens.{self.__class__.__qualname__}('{self.literal}')"

    def __str__(self):
        return f"{self.__class__.__qualname__}('{self.literal}')"

class EOF(Token):
    __slots__ = ('literal',)

    def __init__(self):
        self.literal = '\0'

class ILLEGAL(Token):
    __slots__ = ('literal',)

    def __init__(self, literal):
        self.literal = str(literal)

class IDENT(Token):
    __slots__ = ('literal',)

    def __init__(self, literal):
        self.literal = str(literal)

class INT(Token):
    __slots__ = ('literal',)

    def __init__(self, literal):
        self.literal = str(literal)

class ASSIGN(Token):
    __slots__ = ('literal',)

    def __init__(self):
        self.literal = '='

class COMMA(Token):
    __slots__ = ('literal',)

    def __init__(self):
        self.literal = ','

class SEMICOLON(Token):
    __slots__ = ('literal',)

    def __init__(self):
        self.literal = ';'

#
# Arithmetic ops
#

class PLUS(Token):
    __slots__ = ('literal',)

    def __init__(self):
        self.literal = '+'

class MINUS(Token):
    __slots__ = ('literal',)

    def __init__(self):
        self.literal = '-'

class ASTERISK(Token):
    __slots__ = ('literal',)

    def __init__(self):
        self.literal = '*'

class SLASH(Token):
    __slots__ = ('literal',)

    def __init__(self):
        self.literal = '/'

# Relational ops

class GT(Token):
    __slots__ = ('literal',)

    def __init__(self):
        self.literal = '>'

class GTE(Token):
    __slots__ = ('literal',)

    def __init__(self):
        self.literal = '>='

class LT(Token):
    __slots__ = ('literal',)

    def __init__(self):
        self.literal = '<'

class LTE(Token):
    __slots__ = ('literal',)

    def __init__(self):
        self.literal = '<='

class EQ(Token):
    __slots__ = ('literal',)

    def __init__(self):
        self.literal = '=='

class NEQ(Token):
    __slots__ = ('literal',)

    def __init__(self):
        self.literal = '!='

# Keywords

# Booleans

class TRUE(Token):
    __slots__ = ('literal',)

    def __init__(self):
        self.literal = 'true'

class FALSE(Token):
    __slots__ = ('literal',)

    def __init__(self):
        self.literal = 'false'

class IF(Token):
    __slots__ = ('literal',)

    def __init__(self):
        self.literal = 'if'

class ELSE(Token):
    __slots__ = ('literal',)

    def __init__(self):
        self.literal = 'else'

class FUNCTION(Token):
    __slots__ = ('literal',)

    def __init__(self):
        self.literal = 'func'

class LET(Token):
    __slots__ = ('literal',)

    def __init__(self):
        self.literal = 'let'

class RETURN(Token):
    __slots__ = ('literal',)

    def __init__(self):
        self.literal = 'return'

#
# Brackets
#

class LPARAN(Token):
    __slots__ = ('literal',)

    def __init__(self):
        self.literal = '('

class RPARAN(Token):
    __slots__ = ('literal',)

    def __init__(self):
        self.literal = ')'

class LBRACE(Token):
    __slots__ = ('literal',)

    def __init__(self):
        self.literal = '{'

class RBRACE(Token):
    __slots__ = ('literal',)

    def __init__(self):
        self.literal = '}'

