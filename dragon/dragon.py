from lexer import Lexer
from parser import Parser
import ast
import tokens

class IntObject(int):

    def __init__(self, value):
        self.value = value

class BoolObject():

    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"<{self.value}>".lower()

    def __str__(self):
        return f"<{self.value}>".lower()

class ReturnValue():

    def __init__(self, value=None):
        self.value = value
    
    def __repr__(self):
        return f"ReturnValue({self.value})"

class Environment:

    def __init__(self, parent=None):
        self.parent = parent
        self.table = {}
    
    def get(self, ident):
        if ident in self.table:
            return self.table[ident]
        
        if self.parent:
            return self.parent.get(ident)
        
        raise ValueError(f"Unbound variable: {ident}")
    
    def set_(self, ident, val):
        self.table[ident] = val
    
    def __repr__(self):
        return f"Environment({repr(self.table)})"

def eval_assignment(tree, env):
    val = evaluate(tree.expr, env)
    env.set_(tree.ident.literal, val)

    return val

def eval_program(tree, env):
    for stmt in tree.statements:
        # evaluate(stmt, env)
        # print(stmt)
        print(evaluate(stmt, env)) # Print will be removed

def eval_binop(tree, env):
    if isinstance(tree.op, tokens.PLUS):
        return evaluate(tree.left, env) + evaluate(tree.right, env)
    if isinstance(tree.op, tokens.MINUS):
        return evaluate(tree.left, env) - evaluate(tree.right, env)
    if isinstance(tree.op, tokens.ASTERISK):
        return evaluate(tree.left, env) * evaluate(tree.right, env)
    if isinstance(tree.op, tokens.SLASH):
        return evaluate(tree.left, env) / evaluate(tree.right, env)
    if isinstance(tree.op, tokens.LT):
        return BoolObject(evaluate(tree.left, env) < evaluate(tree.right, env))
    if isinstance(tree.op, tokens.GT):
        return BoolObject(evaluate(tree.left, env) > evaluate(tree.right, env))

    raise NotImplementedError(f"Eval has not been implemented for {tree.op}")

def eval_int_literal(tree, env):
    return IntObject(int(tree.literal))

def eval_bool_literal(tree, env):
    if tree.literal == 'true':
        return BoolObject(True)
    return BoolObject(False)

def eval_identifier(tree, env):
    return env.get(tree.literal)

def eval_expression(tree, env):
    if isinstance(tree, ast.IdentifierExpression):
        return eval_identifier(tree, env)
    if isinstance(tree, ast.BinaryOp):
        return eval_binop(tree, env)
    if isinstance(tree, ast.PrefixOp):
        return eval_prefixop(tree, env)
    if isinstance(tree, ast.IntLiteral):
        return eval_int_literal(tree, env)
    if isinstance(tree, ast.BoolLiteral):
        return eval_bool_literal(tree, env)
    if isinstance(tree, ast.FunctionCall):
        return eval_function_call(tree, env)

    raise NotImplementedError(f"Eval has not been implemented for {type(tree)}")

def eval_if_expression(tree, env):
    if evaluate(tree.cond, env).value:
        return evaluate(tree.cons, env)
    if tree.has_alt:
        return evaluate(tree.alt, env)

def eval_block_statement(tree, env):
    for stmt in tree.statements:
        ret = evaluate(stmt, env)
    
    return ret

def eval_function_literal(tree, env):
    env.set_(tree.name.literal, tree)
    return tree

def eval_func_body(tree, env):
    for stmt in tree.statements:
        ret = evaluate(stmt, env)
        if isinstance(ret, ReturnValue):
            return ret
    
    return ReturnValue()


def eval_function_call(tree, env):
    new_env = Environment(parent=env)
    func = env.get(tree.name.literal)
    if len(tree.args) != len(func.params):
        raise ValueError("Argument mismatch")


    actual_params = [evaluate(arg, env) for arg in tree.args]
    for x, y in zip(func.params, actual_params):
        new_env.set_(x.literal, y)

    return eval_func_body(func.body, new_env).value

def eval_return(tree, env):
    ret = evaluate(tree.expr, env)
    return ReturnValue(value=ret)

def evaluate(tree, env):
    if isinstance(tree, ast.AssignmentStatement):
        return eval_assignment(tree, env)
    if isinstance(tree, ast.Expression):
        return eval_expression(tree, env)
    if isinstance(tree, ast.IfExpression):
        return eval_if_expression(tree, env)
    if isinstance(tree, ast.BlockStatement):
        return eval_block_statement(tree, env)
    if isinstance(tree, ast.FunctionLiteral):
        return eval_function_literal(tree, env)
    if isinstance(tree, ast.ReturnStatement):
        return eval_return(tree, env)

def main():
    s = '''
    let x =1;
    let y=4;
    x+y;
    func boo(z){
        return z*10;
    }
    boo(x+y)
    '''

    # s = '''
    # func boo(x){
    #     if (x < 1){
    #         return 0;
    #     }else{
    #         return boo(x-1);
    #     }
    # }
    # boo(3)
    # '''

    l = Lexer(s)
    toks = l.scan()
    p = Parser(toks)
    tree = p.parse()

    e = Environment()
    eval_program(tree, e)

if __name__ == '__main__':
    main()