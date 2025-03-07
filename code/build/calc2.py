# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.   This is from O'Reilly's
# "Lex and Yacc", p. 63.
# -----------------------------------------------------------------------------

import sys
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

tokens = (
    'NAME','NUMBER',
    )

literals = ['=','+','-','*','/', '(',')']

# Tokens

t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = " \t"

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lex.lex()

# Parsing rules

precedence = (
    ('left','+','-'),
    ('left','*','/'),
    ('right','UMINUS'),
    )

# dictionary of names
names = { }

def p_statement_assign(p):
    'statement : NAME "=" expression'
    names[p[1]] = p[3]

def p_statement_expr(p):
    'statement : expression'
    print(p[1])
    print(eval(p[1]))

def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression'''
    p[0] = [p[2], p[1], p[3]]

def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = [p[1], p[2]]

def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]

def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]

def p_expression_name(p):
    "expression : NAME"
    if p[1] not in names:
        print("Undefined name '%s'" % p[1])
        p[0] = 0
    else:
        p[0] = p[1] 

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

def eval(e):
    if isinstance(e, int):
        return e
    elif isinstance(e, str):
        return names[e]
    elif isinstance(e, list):
        if len(e) == 2:
            return -eval(e[1])
        else:
            if   e[0] == '+': return eval(e[1])+eval(e[2])
            elif e[0] == '-': return eval(e[1])-eval(e[2])
            elif e[0] == '*': return eval(e[1])*eval(e[2])
            elif e[0] == '/': return eval(e[1])/eval(e[2])
    return 0

import ply.yacc as yacc
yacc.yacc()

while 1:
    try:
        s = raw_input('calc > ')
    except EOFError:
        break
    if not s: continue
    yacc.parse(s)
