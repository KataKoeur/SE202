from ast.nodes import *
from . import tokenizer
import ply.yacc as yacc

tokens = tokenizer.tokens

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'INF'),
    ('left', 'SUP'),
    ('left', 'EQU'),
    ('left', 'DIFF'),
    ('left', 'INFEQU'),
    ('left', 'SUPEQU'),
    ('left', 'MINUS'),
    ('left', 'PLUS'),
    ('left', 'DIV'),
    ('left', 'TIMES')
)

def p_expression_binop(p):
    '''expression : expression OR expression
                  | expression AND expression
                  | expression INF expression
                  | expression SUP expression
                  | expression EQU expression
                  | expression DIFF expression
                  | expression INFEQU expression
                  | expression SUPEQU expression
                  | expression MINUS expression
                  | expression PLUS expression
                  | expression DIV expression
                  | expression TIMES expression'''
    p[0] = BinaryOperator(p[2], p[1], p[3])

def p_expression_parentheses(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = IntegerLiteral(p[1])

def p_expression_identifier(p):
    'expression : ID'
    p[0] = Identifier(p[1])

def p_error(p):
    import sys
    sys.stderr.write("no way to analyze %s\n" % p)
    sys.exit(1)

parser = yacc.yacc()

def parse(text):
    return parser.parse(text, lexer = tokenizer.lexer.clone())
