# Get the token map from the lexer.  This is required.

from parsing import Earley_Parser, findRoot

# Get the token map from the lexer.  This is required.
from tokenization import tokens, literals, lexer

import ply.lex as lex
import sys
sys.path.insert(0, "../..")


grammar= {
    "nonterminals" : [ "P", "input", "statement", "inner_input", "assignment", "module_instantiation",
                       "ifelse_statement" , "if_statement", "child_statements", "child_statement",
                       "module_id", "single_module_instantiation", "expr",
                       "expr_or_empty", "list_comprehension_elements",
                       "list_comprehension_elements_p", "list_comprehension_elements_or_expr",
                       "optional_commas", "vector_expr", "arguments_decl",
                       "argument_decl", "arguments_call", "argument_call"],
    "terminals" : tokens + literals,
    "start" : "P",
    "rules" : {
                "P" : "input",
                # "input" :  ["" , "TOK_USE input" , "statement input"],
                "input" :  [ "statement input", ''],

                "statement" : [';', '{ inner_input }', 'module_instantiation' , 'assignment' ,
                              'TOK_MODULE TOK_ID ( arguments_decl optional_commas ) statement',
                              'TOK_FUNCTION TOK_ID ( arguments_decl optional_commas ) = expr ;'],

                "inner_input" : ['TOK_USE input' ,  'statement input'],
                "assignment" : ['TOK_ID = expr ;'],
                "module_instantiation" : ['! module_instantiation',
                                          '# module_instantiation',
                                          '% module_instantiation',
                                          '* module_instantiation',
                                          'single_module_instantiation child_statement',
                                          'ifelse_statement'],

                "ifelse_statement" : ['if_statement' , 'if_statement TOK_ELSE  child_statement'],

                "if_statement" : ['TOK_IF ( expr ) child_statement'],

                "child_statements" : ['child_statements child_statement', 'child_statements assignment', ''],

                "child_statement" : [';', '{ child_statements }', 'module_instantiation'],

                "module_id" : ['TOK_ID' ,'TOK_FOR', 'TOK_LET','TOK_ASSERT','TOK_ECHO','TOK_EACH'],

                "single_module_instantiation" :  ['module_id ( arguments_call )'],

                "expr" : ['TOK_TRUE',
                          'TOK_FALSE',
                          'TOK_UNDEF',
                          'TOK_ID',
                          'expr . TOK_ID',
                          'TOK_STRING',
                          'TOK_NUMBER',
                          '[ expr : expr ]',
                          '[ expr : expr : expr ]',
                          '[ optional_commas ]',
                          '[ vector_expr optional_commas ]',
                          'expr * expr',
                          'expr / expr',
                          'expr % expr',
                          'expr + expr',
                          'expr - expr',
                          'expr < expr',
                          'expr LE expr',
                          'expr EQ expr',
                          'expr NE expr',
                          'expr GE expr',
                          'expr > expr',
                          'expr AND expr',
                          'expr OR expr',
                          '+ expr',
                          '- expr',
                          '! expr',
                          '( expr )',
                          'expr ? expr : expr',
                          'expr [ expr ]',
                          'TOK_ID ( arguments_call )',
                          'TOK_LET ( arguments_call ) expr %prec LET',
                          'TOK_ASSERT ( arguments_call ) expr_or_empty %prec LOW_PRIO_LEFT',
                          'TOK_ECHO ( arguments_call ) expr_or_empty %prec LOW_PRIO_LEFT'],

                "expr_or_empty" : ['%prec LOW_PRIO_LEFT' , 'expr %prec HIGH_PRIO_LEFT'],

                "list_comprehension_elements" : ['TOK_LET ( arguments_call ) list_comprehension_elements_p',
                                                 'TOK_EACH list_comprehension_elements_or_expr',
                                                 'TOK_FOR ( arguments_call ) list_comprehension_elements_or_expr',
                                                 'TOK_FOR ( arguments_call ; expr ; arguments_call ) list_comprehension_elements_or_expr',
                                                 'TOK_IF ( expr ) list_comprehension_elements_or_expr',
                                                 'TOK_IF ( expr ) list_comprehension_elements_or_expr TOK_ELSE list_comprehension_elements_or_expr'],

                "list_comprehension_elements_p" : ['list_comprehension_elements', '( list_comprehension_elements )'],

                "list_comprehension_elements_or_expr" : ['list_comprehension_elements_p', 'expr'],

                "optional_commas" : [', optional_commas', ''],

                "vector_expr" : ['expr', 'list_comprehension_elements', 'vector_expr , optional_commas list_comprehension_elements_or_expr'],

                "arguments_decl" : ['', 'argument_decl', 'arguments_decl , optional_commas argument_decl'],

                "argument_decl" : ['TOK_ID' , 'TOK_ID = expr'],

                "arguments_call" :  [ 'argument_call', 'arguments_call , optional_commas argument_call', ''],

                "argument_call" : ['expr', 'TOK_ID = expr' ]

              }
}


data7 = '''
seed=42;
random_vect=rands(5,15,4,seed);
echo( "Random Vector: ",random_vect);
sphere(r=5);
for(i=[0:3]) {
 rotate(360*i/4) {
   translate([10+random_vect[i],0,0])
     sphere(r=random_vect[i]/2);
 }
}
'''

# Give the lexer some input
# print data1
lexer.input(data7)

code = []

# lex.py provides an external interface in the form of a token() function that returns the next valid token on the input stream.
# yacc.py calls this repeatedly to retrieve tokens and invoke grammar rules.
# The tokens returned by lexer.token() are instances of LexToken.
# This object has attributes tok.type, tok.value, tok.lineno, and tok.lexpos. The following code shows an example of accessing these attributes:

while True:
    tok = lexer.token()
    if not tok: break      # No more input
    # print tok.value
    code.append( tok.type)  # print tok.type, tok.value, tok.line, tok.lexpos

input = code
chart = Earley_Parser(grammar, input)
print chart, '\n'
root = findRoot(chart, input, grammar)
print "root: ", root


def printTree(state):
    if state[4] == ():
        return
    else:
        for ptr in state[4]:
            print state[0], ' -> ', state[1]
            printTree(chart[ptr[0]][ptr[1]])


def printSideways(state):
    print state[1]
    if state[4] != ():
        n = len(state[4])
        for i in range(n-1, -1, -1 ):
            printSideways(chart[state[4][i][0]][state[4][i][1]])

print "Derivatives: "
printTree(root)

# from simple_tree import Node
# def buildTree(state, node):
#     if state[4] == ():
#         pass
#     else:
#         for ptr in state[4]:
#             child = Node(chart[ptr[0]][ptr[1]][0])
#             node.addkid(child)
#             buildTree(chart[ptr[0]][ptr[1]], child)
#
#
# rootNode = Node("start",[])
# buildTree(root, rootNode)
#
#
# for child in rootNode.get_children():
#     for chichild in child.get_children():
#         print "parent is: ", chichild.get_label()
#         for chichichild in chichild.get_children():
#             print chichichild.get_label()




