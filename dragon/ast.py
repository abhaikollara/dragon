class Program:

    def __init__(self, statements=[]):
        self.statements = statements

    def __repr__(self):
        return f"ast.Program({repr(self.statements)})"

    def __getitem__(self, idx):
        return self.statements[idx]
    
    def __len__(self):
        return len(self.statements)

class Expression:
    pass

class AssignmentStatement:
    
    def __init__(self, ident, expr):
        self.ident = ident
        self.expr = expr
    
    def __repr__(self):
        return f"ast.AssignmentStatement({str(self.ident)}, {self.expr})"

class ReturnStatement:
    
    def __init__(self, expr):
        self.expr = expr
    
    def __repr__(self):
        return f"ast.ReturnStatement({self.expr})"


class ExpressionStatement:
    
    def __init__(self, expr):
        self.expr = expr

class IdentifierExpression(Expression):
    
    def __init__(self, token):
        self.token = token
        self.literal = self.token.literal

    def __repr__(self):
        return f"ast.IdentifierExpression('{self.literal}')"

class BlockStatement:

    def __init__(self, statements=[]):
        self.statements = statements
    
    def __len__(self):
        return len(self.statements)

    def __repr__(self):
        return f"ast.BlockStatement({repr(self.statements)})"

class IfExpression:
    
    def __init__(self, cond, cons, alt=None):
        self.cond = cond
        self.cons = cons
        self.alt = alt
    
    @property
    def has_alt(self):
        return self.alt is not None
    
    def __repr__(self):
        return f"ast.IfExpression({repr(self.cond)}, {repr(self.cons)}, {repr(self.alt)})"

class FunctionLiteral:

    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f"ast.FunctionLiteral('{self.name.literal}', {[x.literal for x in self.params]})"

class FunctionCall(Expression):

    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return f"FunctionCall({self.name}, {self.args})"

class IntLiteral(Expression):
    
    def __init__(self, token):
        self.token = token
        self.literal = self.token.literal
    
    def __repr__(self):
        return f"ast.IntLiteral('{self.literal}')"

class BoolLiteral(Expression):
    
    def __init__(self, token):
        self.token = token
        self.literal = self.token.literal
    
    def __repr__(self):
        return f"ast.BoolLiteral('{self.literal}')"

class BinaryOp(Expression):

    def __init__(self, left=None, op=None, right=None):
        self.left = left
        self.op = op
        self.right = right
    
    def __repr__(self):
        return f"ast.BinaryOp({repr(self.left)}, {self.op}, {self.right})"

class PrefixOp(Expression):

    def __init__(self, op=None, operand=None):
        self.op = op
        self.operand = operand
    
    def __repr__(self):
        return f"ast.PrefixOp({repr(self.op)}, {repr(self.operand)})"
