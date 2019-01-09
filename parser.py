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
    """ statement : TITLE
    | unordered_list
    | ordered_list
    | simple_style
    | code_sample
    | loop 
    | figure
    | special_character
    | TEXT
    | simple_eol
    | stat_error """
    carriage_return = "<br/>" if len(p) > 2 and not ("<h" in p[1] and ">" in p[1] and "</h" in p[1]) else ""
    p[0] = AST.TokenNode(f"{p[1]}{carriage_return}")

def p_inline_element(p):
    """ inline_element : simple_style
    | special_character
    | TEXT
    | stat_error """
    p[0] = p[1]

def p_simple_style(p):
    """ simple_style : bold_text
    | italic_text
    | crossed_text
    | underlined_text
    | simple_style TEXT """
    try:
        p[0] = p[1] + " " + p[2]
    except:
        p[0] = p[1]

def p_bold_text(p):
    """ bold_text : BOLD_IDENTIFIER simple_style BOLD_IDENTIFIER
    | BOLD_IDENTIFIER TEXT BOLD_IDENTIFIER"""
    p[0] = f"<span class='bold'>{p[2]}</span>"

def p_italic_text(p):
    """ italic_text : ITALIC_IDENTIFIER simple_style ITALIC_IDENTIFIER
    | ITALIC_IDENTIFIER TEXT ITALIC_IDENTIFIER"""
    p[0] = f"<span class='italic'>{p[2]}</span>"

def p_crossed_text(p):
    """ crossed_text : CROSSED_IDENTIFIER simple_style CROSSED_IDENTIFIER
    | CROSSED_IDENTIFIER TEXT CROSSED_IDENTIFIER"""
    p[0] = f"<span class='crossed'>{p[2]}</span>"

def p_underlined_text(p):
    """ underlined_text : UNDERLINED_IDENTIFIER simple_style UNDERLINED_IDENTIFIER
    | UNDERLINED_IDENTIFIER TEXT UNDERLINED_IDENTIFIER"""
    p[0] = f"<span class='underlined'>{p[2]}</span>"

def p_complex_text(p):
    """ complex_text : simple_style
    | TEXT
    | special_character
    | complex_text complex_text """
    try:
        p[0] = p[1].split("<br/>")[0] + p[2].split("<br/>")[0]
    except:
        p[0] = p[1].split("<br/>")[0]

def p_unordered_list(p):
    """ unordered_list : UNORDERED_LIST_IDENTIFIER complex_text EOL unordered_list
    | UNORDERED_LIST_IDENTIFIER complex_text EOL """
    try:
        p[0] = f"<ul><li>{p[2]}</li>{p[4][4:]}"
    except:
        p[0] = f"<ul><li>{p[2]}</li></ul>"

def p_ordered_list(p):
    """ ordered_list : ORDERED_LIST_INDEX complex_text EOL ordered_list
    | ORDERED_LIST_INDEX complex_text EOL """
    try:
        p[0] = f"<ol><li>{p[2]}</li>{p[4][4:]}"
    except:
        p[0] = f"<ol><li>{p[2]}</li></ol>"

def p_code_sample(p):
    """ code_sample : CODE_SAMPLE """
    code = p[1][1:] if p[1][:1] == "\n" else p[1]
    code = code[:-1] if code[-1:] == "\n" else code
    code = code.replace("\n", "<br/>")
    p[0] = f"<div class='code'>{code}</div>"

def p_loop(p):
    """ loop : LOOP EOL '{' EOL loop_content '}' 
    | LOOP EOL '{' EOL loop_content EOL '}' """
    try:
        args = p[1][9:-1].split("\"")
        elements = [args[1], args[3]]

        ol_list_identifier = ":index:."
        ul_list_identifier = "<ul>"

        global_prefix = "<ol>"  if p[5][:8]  == ol_list_identifier else ("<ul>"  if p[5][:4] == ul_list_identifier else "")
        global_suffix = "</ol>" if p[5][:8]  == ol_list_identifier else ("</ul>" if p[5][:4] == ul_list_identifier else "")
        local_prefix =  "<li>"  if p[5][:8]  == ol_list_identifier else ""
        local_suffix =  "</li>" if p[5][:8]  == ol_list_identifier else ""
        
        result = global_prefix

        for i in range(len(elements)):
            line = p[5][8:] if p[5][:8] == ol_list_identifier else (p[5][4:-5] if p[5][:4] == ul_list_identifier else p[5])
            line = line.replace(":index:", str(i))
            line = line.replace(":element:", elements[i])
            result += local_prefix + line + ("<br/>" if "<ul>" not in line and "<ol>" not in line and "<li>" not in line else "") + local_suffix

        p[0] = result + global_suffix
    except:
        p[0] = f"{p[1]}<br/>{p[3]}<br/>{p[5]}<br/>{(p[6] if p[6] == '}' else p[7])}"

def p_loop_content(p):
    """ loop_content : TEXT
    | TITLE
    | simple_style 
    | unordered_list 
    | special_character """
    p[0] = p[1]

def p_figure(p):
    """ figure : FIGURE """
    try:
        args = p[1][9:-1].split("\"")
        src = args[1]
        alt = args[3]

        result = "<div class='box'><div class='figure'>"
        result += f"<img src='{src}' alt='{alt}'/>"
        result += f"<div class='legende'>{alt}</div>"
        result += "</div></div>"

        try :
            shutil.copyfile(f"resources/{src}", f"output/{src}")
        except:
            print(f"File not found : resources/{src}")    

        p[0] = result
    except:
        p[0] = p[1]

def p_special_character(p):
    """ special_character : BOLD_IDENTIFIER
    | BOLD_IDENTIFIER inline_element
    | ITALIC_IDENTIFIER
    | ITALIC_IDENTIFIER inline_element
    | CROSSED_IDENTIFIER
    | CROSSED_IDENTIFIER inline_element
    | UNDERLINED_IDENTIFIER
    | UNDERLINED_IDENTIFIER inline_element
    | '{'
    | '{' inline_element
    | '}'
    | '}' inline_element
    | '_'
    | '_' inline_element
    | '~'
    | '~' inline_element """
    try:
        p[0] = f"{p[1]} {repr(p[2])[1:-1]}"
    except:
        p[0] = p[1]

def p_simple_eol(p):
    """ simple_eol : EOL """
    p[0] = "<br/>"

def p_stat_error(p):
    """ stat_error : error """
    print("Stat error")
    p[0] = ""

def p_error(p):
    print("Error", p)
    if p is not None:
        parser.errok()

def parse(program):
    return yacc.parse(program)

parser = yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys 
    	
    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog)

    print("result : ", result)

    HTMLWriter().writeResult("title - output file", "fr", result)