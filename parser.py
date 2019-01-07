import ply.yacc as yacc

from lex import tokens
import AST
from HTMLWriter import HTMLWriter
import shutil



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
    | TEXT
    | loop 
    | loop EOL
    | figure
    | figure EOL """
    carriage_return = "<br/>" if len(p) > 2 else ""
    p[0] = AST.TokenNode(f"{p[1]}{carriage_return}")

def p_simple_style(p):
    """ simple_style : bold_text
    | italic_text
    | crossed_text
    | underlined_text
    | simple_style TEXT """
    print(p[1])
    try:
        p[0] = p[1] + p[2]
    except:
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

def p_loop(p):
    """ loop : LOOP '[' TEXT ']' EOL '{' EOL loop_content '}' 
    | LOOP '[' TEXT ']' EOL '{' EOL loop_content EOL '}' """

    print(p[8])

    elements = p[3].split(", ")
    ol_list_identifier = ":index:."
    ul_list_identifier = "<ul>"

    global_prefix = "<ol>"  if p[8][:8]  == ol_list_identifier else ("<ul>"  if p[8][:4] == ul_list_identifier else "")
    global_suffix = "</ol>" if p[8][:8]  == ol_list_identifier else ("</ul>" if p[8][:4] == ul_list_identifier else "")
    local_prefix =  "<li>"  if p[8][:8]  == ol_list_identifier else ""
    local_suffix =  "</li>" if p[8][:8]  == ol_list_identifier else ""
    
    result = global_prefix

    for i in range(len(elements)):
        line = p[8][8:] if p[8][:8] == ol_list_identifier else (p[8][4:-5] if p[8][:4] == ul_list_identifier else p[8])
        line = line.replace(":index:", str(i))
        line = line.replace(":element:", elements[i])
        result += local_prefix + line + ("<br/>" if "<ul>" not in line and "<ol>" not in line and "<li>" not in line else "") + local_suffix

    p[0] = result + global_suffix

def p_loop_content(p):
    """ loop_content : TEXT
    | TITLE
    | simple_style 
    | unordered_list """
    p[0] = p[1]

def p_figure(p):
    """ figure : FIGURE '(' TEXT ')' EOL
    | FIGURE '(' TEXT ')' """

    args = p[3].split(", ")

    print(p[:])

    args[0] = args[0][1:-1]
    args[1] = args[1][1:-1]

    result = "<div class='box'><div class='figure'>"
    result += f"<img src='{args[0]}' alt='{args[1]}'/>"
    result += f"<div class='legende'>{args[1]}</div>"
    result += "</div></div>"

    try :
        shutil.copyfile(f"resources/{args[0]}", f"output/{args[0]}")
    except:
        print(f"File not found : resources/{args[0]}")    

    p[0] = result

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