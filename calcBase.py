# -----------------------------------------------------------------------------
# calc.py
#
# Expressions arithmétiques sans variables
# -----------------------------------------------------------------------------
from genereTreeGraphviz2 import printTreeGraph

# PREPARER DES INPUTS POUR LA SOUTENANCE

tokens = [
    'NUMBER', 'MINUS',
    'PLUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'AND', 'OR',
    'SEMICOLON',
    'NAME', 'EQUAL',
    'COMPARE',
    'LACCOL', 'RACCOL',
    'SEPARATOR', 'QUOTE',
    'LBRACKET', 'RBRACKET'
]

# Tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LACCOL = r'\{'
t_RACCOL = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_AND = r'&'
t_OR = r'\|'
t_SEMICOLON = r';'
t_EQUAL = r'='
t_COMPARE = r'[<>]'
t_SEPARATOR = r','
t_QUOTE = r'\"'

reserved = {
    'print': 'PRINT',
    'true': 'TRUE',
    'false': 'FALSE',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'function': 'FUNCTION'
}

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('nonassoc', 'AND', 'OR', 'EQUAL', 'COMPARE'),
    ('left', 'TIMES', 'DIVIDE')
)

tokens += reserved.values()

names = {}
functions = {}
params = {}


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Ignored characters
t_ignore = " \t"


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
import ply.lex as lex

lex.lex()


def p_start(p):
    """start : bloc"""
    p[0] = ('START', p[1])
    printTreeGraph(p[1])
    print(p[0])
    evalInst(p[1])


def p_bloc(p):
    """bloc : bloc statement SEMICOLON
                            | statement SEMICOLON"""
    if p[2] == ";":
        p[0] = ('bloc', p[1], 'empty')
    else:
        p[0] = ('bloc', p[1], p[2])


def p_print(p):
    """statement : PRINT LPAREN params RPAREN"""
    p[0] = ('print', p[3])


def p_expression_binop_plus(p):
    """expression : expression PLUS expression"""

    p[0] = ('+', p[1], p[3])


def p_expressionTrue(p):
    """expression : TRUE"""
    p[0] = ('true')


def p_expressionFalse(p):
    """expression : FALSE"""
    p[0] = ('false')


def p_name_assign(p):
    """statement : NAME EQUAL expression
                | NAME PLUS PLUS"""
    if p[2] == "=":
        p[0] = ('assign', p[1], p[3])
    else:
        p[0] = ('assign', p[1], p[2], p[3])

##########################################

def p_array_assign(p):
    """statement : NAME EQUAL LBRACKET values RBRACKET"""
    if p[2] == "=":
        p[0] = ('assign', p[1], p[4])

def p_array_values(p):
    """values : expression SEPARATOR values
                        | expression"""

    if len(p) == 2:
        p[0] = ('value', p[1], 'empty')
    else:
        p[0] = ('value', p[1], p[3])

##########################################


def p_expression_binop_bool2(p):
    """expression : expression COMPARE expression"""

    p[0] = (p[2], p[1], p[3])


def p_expression_binop_bool(p):
    """expression : expression AND expression
                                | expression OR expression"""
    if p[2] == '&':
        p[0] = ('and', p[1], p[3])
    else:
        p[0] = ('or', p[1], p[3])


def p_expression_binop_times(p):
    """expression : expression TIMES expression"""
    p[0] = ('*', p[1], p[3])


def p_expression_binop_divide_and_minus(p):
    """expression : expression MINUS expression
				    | expression DIVIDE expression"""
    p[0] = (p[2], p[1], p[3])


def p_expression_group(p):
    """expression : LPAREN expression RPAREN"""
    p[0] = p[2]


def p_condition(p):
    """statement : IF expression LACCOL bloc RACCOL
                                | IF expression LACCOL bloc RACCOL ELSE LACCOL bloc RACCOL"""
    if len(p) > 6:
        p[0] = ('if', p[2], p[4], p[8])
    else:
        p[0] = ('if', p[2], p[4])


def p_loop(p):
    """statement : WHILE expression LACCOL bloc RACCOL"""
    p[0] = ('while', p[2], p[4])


def p_for(p):
    """statement : FOR LPAREN statement SEMICOLON expression SEMICOLON statement RPAREN LACCOL bloc RACCOL"""
    p[0] = ('for', p[3], p[5], p[7], p[10])


def p_params(p):
    """params : expression SEPARATOR params
                        | expression"""

    if len(p) == 2:
        p[0] = ('param', p[1], 'empty')
    else:
        p[0] = ('param', p[1], p[3])


def p_function(p):
    """statement : FUNCTION NAME LPAREN RPAREN LACCOL bloc RACCOL
                                | FUNCTION NAME LPAREN params RPAREN LACCOL bloc RACCOL"""
    if len(p) == 8:
        p[0] = ('function', p[2], p[6])
    else:
        p[0] = ('function', p[2], p[4], p[7])


def p_expression_number(p):
    """expression : NUMBER"""
    p[0] = p[1]


def p_name(p):
    """expression : NAME"""
    p[0] = p[1]


def p_word(p):
    """expression : QUOTE expression
                        | NAME QUOTE
                        | NAME expression"""

    if p[1] == '"':
        p[0] = p[2]
    elif p[2] == '"':
        p[0] = ('string', p[1], 'empty')
    else:
        p[0] = ('string', p[1], p[2])


def p_function_call(p):
    """statement : NAME LPAREN RPAREN
                       | NAME LPAREN params RPAREN"""
    if len(p) == 4:
        p[0] = ('call', p[1])
    else:
        p[0] = ('call', p[1], p[3])


def p_error(p):
    print("Syntax error at '%s'" % p.value)


def evalExpr(t):
    if type(t) == int:
        return t
    elif type(t) == str:
        if t == "true":
            return True
        elif t == "false":
            return False
        else:
            return names[t]
    else:
        if t[0] == "+":
            return evalExpr(t[1]) + evalExpr(t[2])
        elif t[0] == "-":
            return evalExpr(t[1]) - evalExpr(t[2])
        elif t[0] == "*":
            return evalExpr(t[1]) * evalExpr(t[2])
        elif t[0] == "/":
            return evalExpr(t[1]) / evalExpr(t[2])
        elif t[0] == "and":
            return evalExpr(t[1]) and evalExpr(t[2])
        elif t[0] == "or":
            return evalExpr(t[1]) or evalExpr(t[2])
        elif t[0] == ">":
            return evalExpr(t[1]) > evalExpr(t[2])
        elif t[0] == "<":
            return evalExpr(t[1]) < evalExpr(t[2])
        elif t[0] == "string":
            res = ''
            unstack_val = t
            while True:
                res += unstack_val[1]
                if unstack_val[2] == "empty":
                    break
                else:
                    res += ' '
                    unstack_val = unstack_val[2]
            return res


def evalInst(t):
    if t[0] == "bloc":
        evalInst(t[1])
        evalInst(t[2])
    elif t[0] == "print":
        unstack_val = t[1]
        while True:
            print('calc >', str(evalExpr(unstack_val[1])))
            if unstack_val[2] == "empty":
                break
            else:
                unstack_val = unstack_val[2]
    elif t[0] == "assign":
        if len(t) == 4:
            names[t[1]] += 1
        else:
            names[t[1]] = evalExpr(t[2])
    elif t[0] == "function":
        if len(t) == 4:
            params[t[1]] = t[2]
            functions[t[1]] = t[3]
        else:
            functions[t[1]] = t[2]
    elif t[0] == "call":
        if t[1] in functions:
            if len(t) > 2:
                unstack_val = t[2]
                unstack_var = params[t[1]]
                while True:
                    names[unstack_var[1]] = evalExpr(unstack_val[1])
                    if unstack_val[2] == "empty":
                        break
                    else:
                        unstack_val = unstack_val[2]
                        unstack_var = unstack_var[2]
            evalInst(functions[t[1]])
    elif t[0] == "if":
        if evalExpr(t[1]):
            evalInst(t[2])
        elif len(t) > 3:
            evalInst(t[3])
    elif t[0] == "while":
        while evalExpr(t[1]):
            evalInst(t[2])
    elif t[0] == "for":
        evalInst(t[1])
        while evalExpr(t[2]):
            evalInst(t[4])
            evalInst(t[3])


import ply.yacc as yacc

yacc.yacc()

#with open("test/file5.txt") as file:
#    s = file.read()

s = "y=7+8;x=[5,8,10+20,y];"

yacc.parse(s)
