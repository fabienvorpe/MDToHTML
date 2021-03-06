import ply.yacc as yacc

from lex import tokens
import AST
from HTMLWriter import HTMLWriter
import shutil

# define programm (tree's root)
def p_programme_statement(p):
    """ programme : statement 
    | statement programme """
    try:
        p[0] = AST.ProgramNode([p[1]] + p[2].children) # handle recursivity
    except:
        p[0] = AST.ProgramNode(p[1])

# define statement (possible elements from root)
def p_statement(p):
    """ statement : title
    | simple_text
    | unordered_list
    | ordered_list
    | code_sample
    | loop
    | loop EOL
    | figure
    | simple_eol """
    p[0] = AST.TokenNode(f"{p[1]}")

# define title
def p_title(p):
    """ title : TITLE 
    | TITLE EOL """
    level = len(p[1].split()[0]) # get '#' suite and count to get title level
    nb_sharps = level
    if level > 6: # maximum title level in HTML is 6
        level = 6
    p[0] = f"<h{level}>{p[1][nb_sharps+1:]}</h{level}>"

# define text (styles and uninterpreted characters)
def p_simple_text(p):
    """ simple_text : simple_style
    | TEXT
    | special_character """
    p[0] = p[1]

# define recursive text
def p_complex_text(p):
    """ complex_text : simple_text
    | complex_text complex_text """
    try:
        p[0] = p[1] + p[2] # handle recursivity
    except:
        p[0] = p[1]

# define styles
def p_simple_style(p):
    """ simple_style : bold_text
    | italic_text
    | crossed_text
    | underlined_text
    | simple_style TEXT """
    try:
        p[0] = p[1] + " " + p[2] # handle recursivity - separate elements by a space
    except:
        p[0] = p[1]

# define bold style
def p_bold_text(p):
    """ bold_text : BOLD_IDENTIFIER simple_style BOLD_IDENTIFIER
    | BOLD_IDENTIFIER TEXT BOLD_IDENTIFIER"""
    p[0] = f"<span class='bold'>{p[2]}</span>"

# define italic style
def p_italic_text(p):
    """ italic_text : ITALIC_IDENTIFIER simple_style ITALIC_IDENTIFIER
    | ITALIC_IDENTIFIER TEXT ITALIC_IDENTIFIER"""
    p[0] = f"<span class='italic'>{p[2]}</span>"

# define crossed style
def p_crossed_text(p):
    """ crossed_text : CROSSED_IDENTIFIER simple_style CROSSED_IDENTIFIER
    | CROSSED_IDENTIFIER TEXT CROSSED_IDENTIFIER"""
    p[0] = f"<span class='crossed'>{p[2]}</span>"

# define underlined text
def p_underlined_text(p):
    """ underlined_text : UNDERLINED_IDENTIFIER simple_style UNDERLINED_IDENTIFIER
    | UNDERLINED_IDENTIFIER TEXT UNDERLINED_IDENTIFIER"""
    p[0] = f"<span class='underlined'>{p[2]}</span>"

# define unordered list with recursivity
def p_unordered_list(p):
    """ unordered_list : UNORDERED_LIST_IDENTIFIER complex_text EOL unordered_list
    | UNORDERED_LIST_IDENTIFIER complex_text
    | UNORDERED_LIST_IDENTIFIER complex_text EOL """
    try:
        p[0] = f"<ul><li>{p[2]}</li>{p[4][4:]}" # recursivity - more list elements following
    except:
        p[0] = f"<ul><li>{p[2]}</li></ul>" # last list element

# define ordered list with recursivity
def p_ordered_list(p):
    """ ordered_list : ORDERED_LIST_INDEX complex_text EOL ordered_list
    | ORDERED_LIST_INDEX complex_text 
    | ORDERED_LIST_INDEX complex_text EOL """
    try:
        p[0] = f"<ol><li>{p[2]}</li>{p[4][4:]}" # recursivity - more list elements following
    except:
        p[0] = f"<ol><li>{p[2]}</li></ol>" # last list element

# define code samples and do not interpret inside code
def p_code_sample(p):
    """ code_sample : CODE_SAMPLE 
    | CODE_SAMPLE EOL """
    # identify code sample's content
    code = p[1][1:] if p[1][:1] == "\n" else p[1]
    code = code[:-1] if code[-1:] == "\n" else code

    # replace special character by their HTML equivalent
    code = code.replace("\n", "<br/>")
    code = code.replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")

    p[0] = f"<div class='code'>{code}</div>"

# define loops and interpret content
def p_loop(p):
    """ loop : LOOP EOL '{' EOL loop_content '}' 
    | LOOP EOL '{' EOL loop_content EOL '}' """
    try:
        # identify loop's arguments
        args = p[1][9:-1].split("\"")
        elements = [args[i] for i in range(len(args)) if i%2==1]

        # surround by lists HTML tags if the loop's containing lists
        ol_list_identifier = ":index:."
        ul_list_identifier = "<ul>"

        global_prefix = "<ol>"  if p[5][:8]  == ol_list_identifier else ("<ul>"  if p[5][:4] == ul_list_identifier else "")
        global_suffix = "</ol>" if p[5][:8]  == ol_list_identifier else ("</ul>" if p[5][:4] == ul_list_identifier else "")
        local_prefix =  "<li>"  if p[5][:8]  == ol_list_identifier else ""
        local_suffix =  "</li>" if p[5][:8]  == ol_list_identifier else ""
        
        result = global_prefix

        # repeat loop's content
        for i in range(len(elements)):
            line = p[5][8:] if p[5][:8] == ol_list_identifier else (p[5][4:-5] if p[5][:4] == ul_list_identifier else p[5])
            line = line.replace(":index:", str(i))
            line = line.replace(":element:", elements[i])
            result += local_prefix + line + ("<br/>" if "<ul>" not in line and "<ol>" not in line and "<li>" not in line else "") + local_suffix

        p[0] = result + global_suffix
    except:
        p[0] = f"{p[1]}<br/>{p[3]}<br/>{p[5]}<br/>{(p[6] if p[6] == '}' else p[7])}" # return raw text (loop's not interpreted)

# define what can be found in a loop
def p_loop_content(p):
    """ loop_content : title
    | simple_text
    | unordered_list """
    p[0] = p[1]

# define a figure, copy the source image in the output folder
def p_figure(p):
    """ figure : FIGURE 
    | FIGURE EOL """
    try:
        # identify figure's arguments
        args = p[1][9:-1].split("\"")
        src = args[1]
        alt = args[3]

        # create image's HTML tags
        result = "<div class='box'><div class='figure'>"
        result += f"<img src='img/{src}' alt='{alt}'/>"
        result += f"<div class='legende'>{alt}</div>"
        result += "</div></div>"

        try :
            shutil.copyfile(f"resources/{src}", f"generated/img/{src}") # copy image to the output folder
        except:
            print(f"File not found : resources/{src}")    

        p[0] = result
    except:
        p[0] = p[1] # return raw text (figure's not interpreted)

# define special characters to be interpreted as raw text
def p_special_character(p):
    """ special_character : BOLD_IDENTIFIER
    | BOLD_IDENTIFIER simple_text
    | ITALIC_IDENTIFIER
    | ITALIC_IDENTIFIER simple_text
    | CROSSED_IDENTIFIER
    | CROSSED_IDENTIFIER simple_text
    | UNDERLINED_IDENTIFIER
    | UNDERLINED_IDENTIFIER simple_text
    | '{'
    | '{' simple_text
    | '}'
    | '}' simple_text
    | '_'
    | '_' simple_text
    | '~'
    | '~' simple_text """
    try:
        p[0] = f"{p[1]} {repr(p[2])[1:-1]}" # handle recursivity
    except:
        p[0] = p[1]

# define end of line
def p_simple_eol(p):
    """ simple_eol : EOL """
    p[0] = "<br/>"

# handle errors
def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Error at EOF")

# parse the programme
def parse(program):
    return yacc.parse(program)

parser = yacc.yacc(outputdir="generated")

if __name__ == "__main__":
    import sys 
    	
    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog)

    filename = ".".join(sys.argv[1].split(".")[0:-1])
    filename = filename.split("\\")[-1]
    HTMLWriter().writeResult(filename, "fr", result)