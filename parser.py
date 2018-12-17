import ply.yacc as yacc

from lex import tokens
import AST


def p_programme_statement(p):
    """ programme : statement 
    | statement programme """
    p[0] = AST.ProgramNode(p[1])

def p_statement(p):
    """ statement : TITLE EOL
    | TITLE
    | unordered_list
    | ordered_list
    | bold_text EOL 
    | bold_text
    | TEXT EOL
    | TEXT """
    print("statement", p[:])
    p[0] = AST.TokenNode(p[1])

def p_unordered_list(p):
    """ unordered_list : '*' TEXT EOL unordered_list
    | '*' TEXT EOL
    | '*' TEXT """
    try:
        p[0] = f"<ul><li>{p[2]}</li>{p[4][4:]}"
    except:
        p[0] = f"<ul><li>{p[2]}</li></ul>"

def p_ordered_list(p):
    """ ordered_list : ORDERED_LIST_INDEX EOL ordered_list
    | ORDERED_LIST_INDEX EOL
    | ORDERED_LIST_INDEX """
    try:
        p[0] = f"<ol><li>{p[1]}</li>{p[3][4:]}"
    except:
        p[0] = f"<ol><li>{p[1]}</li></ol>"

def p_bold_text(p):
    """ bold_text : BOLD_TEXT """
    p[0] = f"<span class='bold'>{p[1]}</span>"

def p_error(p):
    if p:
        print ("Syntax error in line %d" % p.lineno)
        yacc.errok()
    else:
        print ("Sytax error: unexpected end of file!")


precedence = (
    #('left', 'ADD_OP'),
)

def parse(program):
    return yacc.parse(program)

yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys 
    	
    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog)

    print("result", result)