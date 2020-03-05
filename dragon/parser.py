import ast
import tokens

class ParserError(Exception):
    pass

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def step(self, n=1):
        self.position += n

    def read_token(self):
        self.position += 1
        return self.current_token

    @property
    def current_token(self):
        try:
            return self.tokens[self.position]
        except IndexError:
            return tokens.EOF()


    @property
    def next_token(self):
        try:
            return self.tokens[self.position+1]
        except IndexError:
            return tokens.EOF()

    def bp(self, op):
        if op in {'>', '<'}:
            return 10
        if op in {'+', '-'}:
            return 50
        if op in {'*', '/'}:
            return 60
        
        return 0

    def led(self, left, token):
        if isinstance(token, (tokens.PLUS, tokens.MINUS, tokens.ASTERISK, tokens.SLASH)):
            self.step()
            return ast.BinaryOp(left, token, self.expr(self.bp(token.literal)))
        if isinstance(token, (tokens.LT, tokens.GT)):
            self.step()
            return ast.BinaryOp(left, token, self.expr(self.bp(token.literal)))
        else:
            raise ParserError(f"Infix parse function not found for {token}")

    def _wrap_in_ast(self, token):
        if isinstance(token, tokens.INT):
            return ast.IntLiteral(token)
        if isinstance(token, (tokens.TRUE, tokens.FALSE)):
            return ast.BoolLiteral(token)
        if isinstance(token, tokens.IDENT):
            return ast.IdentifierExpression(token)

    def nud(self, token):
        if isinstance(token, tokens.LPARAN):
            self.step()
            exp = self.expr()
            if not isinstance(self.next_token, tokens.RPARAN):
                raise ParserError("Expected closing paranthesis")
            self.step()
            return exp
        if isinstance(token, tokens.INT):
            return ast.IntLiteral(token)
        if isinstance(token, (tokens.TRUE, tokens.FALSE)):
            return ast.BoolLiteral(token)
        if isinstance(token, tokens.IDENT):
            return ast.IdentifierExpression(token)
        if isinstance(token, tokens.MINUS):
            return ast.PrefixOp(token, self._wrap_in_ast(self.read_token()))
        else:
            raise ParserError(f"Prefix parse function not found for {token}")

    def expr(self, rbp=0):
        left = self.nud(self.current_token)

        # while not isinstance(self.next_token, (tokens.SEMICOLON, tokens.EOF)) and self.bp(self.next_token.literal) > rbp:
        while self.bp(self.next_token.literal) > rbp:
            left = self.led(left, self.read_token())

        return left

    def parse_expression(self):
        left = self.expr()


        self.step()

        # Necessary ?
        if isinstance(self.current_token, tokens.SEMICOLON):
            self.step()

        return left

    def parse_let_statement(self):
        self.step()
        if not isinstance(self.current_token, tokens.IDENT):
            raise ParserError(f'Expected identifier after `let`, found {self.current_token}')

        ident = self.parse_identifier() ## Is this the best way to do this ??
        
        self.step()
        if not isinstance(self.current_token, tokens.ASSIGN):
            raise ParserError(f"Expected '=' after identifier, found {self.current_token}")
        self.step()
        
        expr = self.parse_expression()
        # self.step()

        return ast.AssignmentStatement(ident, expr)
    
    def parse_return_statement(self):
        self.step()
        expr = self.parse_expression()

        return ast.ReturnStatement(expr)

    def parse_if(self):
        self.step()
        cond = self.parse_expression()
        cons = self.parse_block_statement()
        alt = None
        if isinstance(self.current_token, tokens.ELSE):
            self.step()
            alt = self.parse_block_statement()
        return ast.IfExpression(cond, cons, alt)

    def parse_block_statement(self):
        if not isinstance(self.current_token, tokens.LBRACE):
            raise ParserError(f"Block statements should begin with {'{'} found {self.current_token}")
        self.step()
        if isinstance(self.current_token, tokens.RBRACE):
            return ast.BlockStatement()

        statements = []
        while True:
            l = self.parse_statement()
            statements.append(l)
            if isinstance(self.current_token, tokens.RBRACE):
                break
        self.step()
        return ast.BlockStatement(statements)

    def parse_func_literal(self):
        self.step()
        ident = self.parse_identifier()
        self.step()
        if not isinstance(self.current_token, tokens.LPARAN):
            raise ParserError(f"Expected parameter list after function declaration")
        
        self.step()
        params = []
        while not isinstance(self.current_token, tokens.RPARAN):
            params.append(self.parse_identifier())
            self.step()
            if isinstance(self.current_token, tokens.COMMA):
                self.step()

        self.step()
        body = self.parse_block_statement()

        return ast.FunctionLiteral(ident, params, body)

    def parse_func_call(self):
        ident = self.parse_identifier()
        self.step()
        if not isinstance(self.current_token, tokens.LPARAN):
            raise ParserError(f"Expected parameter list after function declaration")
        
        self.step()
        params = []
        while not isinstance(self.current_token, tokens.RPARAN):
            params.append(self.parse_identifier())
            self.step()
            if isinstance(self.current_token, tokens.COMMA):
                self.step()

        self.step()

        return ast.FunctionCall(ident, params)

    def parse_identifier(self):
        return ast.IdentifierExpression(self.current_token)

    def parse_statement(self):
        if isinstance(self.current_token, tokens.LET):
            return self.parse_let_statement()
        if isinstance(self.current_token, tokens.RETURN):
            return self.parse_return_statement()
        if isinstance(self.current_token, tokens.LBRACE):
            return self.parse_block_statement()
        if isinstance(self.current_token, tokens.IF):
            return self.parse_if()
        if isinstance(self.current_token, tokens.FUNCTION):
            return self.parse_func_literal()
        if isinstance(self.current_token, tokens.IDENT):
            if isinstance(self.next_token, tokens.RPARAN):
                return self.parse_func_call()

        return self.parse_expression()
            # raise ParserError(f"Unable to parse {self.current_token}")

    def parse(self):
        statements = []
        while not isinstance(self.current_token, tokens.EOF):
            statements.append(self.parse_statement())

        return ast.Program(statements)
