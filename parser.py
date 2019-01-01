import ply.yacc as yacc

from lex import tokens
import AST
from HTMLWriter import HTMLWriter


def p_programme_statement(p):
    """ programme : statement 
    | statement programme """
    try:
        p[0] = AST.ProgramNode([p[1]]+p[2].children)
    except:
        p[0] = AST.ProgramNode(p[1])

def p_statement(p):
    """ statement : TITLE EOL
    | TITLE
    | unordered_list
    | ordered_list
    | bold_text
    | italic_text
    | crossed_text
    | underlined_text
    | code_sample
    | TEXT EOL
    | TEXT """
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
    """ bold_text : BOLD_TEXT 
    | BOLD_TEXT EOL"""
    carriage_return = "<br/>" if len(p) > 2 else ""
    p[0] = f"<span class='bold'>{p[1]}</span>{carriage_return}"

def p_italic_text(p):
    """ italic_text : ITALIC_TEXT 
    | ITALIC_TEXT EOL"""
    carriage_return = "<br/>" if len(p) > 2 else ""
    p[0] = f"<span class='italic'>{p[1]}</span>{carriage_return}"

def p_crossed_text(p):
    """ crossed_text : CROSSED_TEXT 
    | CROSSED_TEXT EOL"""
    carriage_return = "<br/>" if len(p) > 2 else ""
    p[0] = f"<span class='crossed'>{p[1]}</span>{carriage_return}"

def p_underlined_text(p):
    """ underlined_text : UNDERLINED_TEXT 
    | UNDERLINED_TEXT EOL"""
    carriage_return = "<br/>" if len(p) > 2 else ""
    p[0] = f"<span class='underlined'>{p[1]}</span>{carriage_return}"

def p_code_sample(p):
    """ code_sample : CODE_SAMPLE 
    | CODE_SAMPLE EOL"""
    carriage_return = "<br/>" if len(p) > 2 else ""
    code = p[1][1:] if p[1][:1] == "\n" else p[1]
    code = code[:-1] if code[-1:] == "\n" else code
    code = code.replace("\n", "<br/>")
    p[0] = f"<span class='code'>{code}</span>{carriage_return}"

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

    print("result : ", result)

    HTMLWriter().writeResult("title - output file", result)