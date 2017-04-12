import ply.lex as lex

tokens = [
    'LE',
    'GE',
    'EQ',
    'NE',
    'AND',
    'OR',
    'TOK_ID',
    'TOK_NUMBER',
    'TOK_STRING',
    # 'TOK_USE',
    'TOK_ERROR'
]


reserved = {
    "module"   : 'TOK_MODULE',
    "function" : 'TOK_FUNCTION',
    "if"       : 'TOK_IF',
    "else"     : 'TOK_ELSE',
    "let"      : 'TOK_LET',
    "assert"   : 'TOK_ASSERT',
    "echo"	   : 'TOK_ECHO',
    "for"      : 'TOK_FOR',
    "each"	   : 'TOK_EACH',
    "true"     : 'TOK_TRUE',
    "false"	   : 'TOK_FALSE',
    "undef"	   : 'TOK_UNDEF'
}

tokens = tokens + list(reserved.values())

# Regular expression rules for simple tokens
literals = ['=', '+', '-', '*', '/', '(', ')', '{', '}', ',', '.', ';', '[', ']', ':']


t_LE = r'<='
t_GE = r">="
t_EQ = r"=="
t_NE = r"!="
t_AND = r"&&"
t_OR = r"\|\|"

t_TOK_STRING = r"\".* \""  # /n not allowed



def  t_TOK_NUMBER(token):
    r"\d*\.\d+([Ee][+-]?\d+)?|\d+\.\d*([Ee][+-]?\d}+)|\d+([Ee][+-]?\d+)?"
    return token

# Define a rule so we can track line numbers
def t_newline(token):
    r'\n+'
    token.lexer.lineno += len(token.value)

def t_TOK_ID(token):
    r"\$?[a-zA-Z0-9_]+"
    token.type = reserved.get(token.value,'TOK_ID')    # Check for reserved words
    return token


# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_TOK_ERROR(token):
    r'(?u).+'
    return token


# Error handling rule
def t_error(token):
    print "Illegal character '%s'" % token.value[0]
    token.lexer.skip(1)



# Build the lexer
lexer = lex.lex()

def getTokens(data):
    lexer.input(data)
    code = []
    while True:
        tok = lexer.token()
        if not tok: break  # No more input
        code.append(tok.type)  # print tok.type, tok.value, tok.line, tok.lexpos
    return code







