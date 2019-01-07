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
    | simple_style
    | simple_style EOL
    | code_sample
    | TEXT EOL
    | TEXT """
    carriage_return = "<br/>" if len(p) > 2 else ""
    p[0] = AST.TokenNode(f"{p[1]}{carriage_return}")

def p_simple_style(p):
    """ simple_style : bold_text
    | italic_text
    | crossed_text
    | underlined_text """
    p[0] = p[1]

def p_unordered_list(p):
    """ unordered_list : '-' TEXT EOL unordered_list
    | '-' simple_style EOL unordered_list
    | '-' TEXT EOL
    | '-' simple_style EOL
    | '-' TEXT
    | '-' simple_style """
    try:
        p[0] = f"<ul><li>{p[2]}</li>{p[4][4:]}"
    except:
        p[0] = f"<ul><li>{p[2]}</li></ul>"

def p_ordered_list(p):
    """ ordered_list : ORDERED_LIST_INDEX TEXT EOL ordered_list
    | ORDERED_LIST_INDEX simple_style EOL ordered_list
    | ORDERED_LIST_INDEX TEXT EOL
    | ORDERED_LIST_INDEX simple_style EOL
    | ORDERED_LIST_INDEX TEXT
    | ORDERED_LIST_INDEX simple_style """
    try:
        p[0] = f"<ol><li>{p[2]}</li>{p[4][4:]}"
    except:
        p[0] = f"<ol><li>{p[2]}</li></ol>"

def p_bold_text(p):
    """ bold_text : BOLD_IDENTIFIER TEXT BOLD_IDENTIFIER
    | BOLD_IDENTIFIER simple_style BOLD_IDENTIFIER"""
    p[0] = f"<span class='bold'>{p[2]}</span>"

def p_italic_text(p):
    """ italic_text : ITALIC_IDENTIFIER TEXT ITALIC_IDENTIFIER
    | ITALIC_IDENTIFIER simple_style ITALIC_IDENTIFIER"""
    p[0] = f"<span class='italic'>{p[2]}</span>"

def p_crossed_text(p):
    """ crossed_text : CROSSED_IDENTIFIER TEXT CROSSED_IDENTIFIER
    | CROSSED_IDENTIFIER simple_style CROSSED_IDENTIFIER"""
    p[0] = f"<span class='crossed'>{p[2]}</span>"

def p_underlined_text(p):
    """ underlined_text : UNDERLINED_IDENTIFIER TEXT UNDERLINED_IDENTIFIER
    | UNDERLINED_IDENTIFIER simple_style UNDERLINED_IDENTIFIER"""
    p[0] = f"<span class='underlined'>{p[2]}</span>"

def p_code_sample(p):
    """ code_sample : CODE_SAMPLE 
    | CODE_SAMPLE EOL"""
    carriage_return = "<br/>" if len(p) > 2 else ""
    code = p[1][1:] if p[1][:1] == "\n" else p[1]
    code = code[:-1] if code[-1:] == "\n" else code
    code = code.replace("\n", "<br/>")
    p[0] = f"<div class='code'>{code}</div>{carriage_return}"

def p_error(p):
    if p:
        print ("Syntax error in line %d" % p.lineno)
        # yacc.errok()
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

    HTMLWriter().writeResult("title - output file", "fr", result)