import ply.yacc as yacc

from lex import tokens
import AST
nbLi = 0


def p_programme_statement(p):
    """ programme : statement 
    | statement programme """
    p[0] = AST.ProgramNode(p[1])

def p_statement(p):
    """ statement : TITLE EOL
    | first_unordered_list """
    p[0] = AST.TokenNode(p[1])

def p_first_unordered_list(p):
    """ first_unordered_list : '*' TEXT EOL first_unordered_list
    | '*' TEXT EOL """
    try:
        print("++", p)
        nbLi += 1
        p[0] = f"<li>{p[2]}</li>{p[3]}"
        nbLi -= 1

        if nbLi == 0:
            p[0] = "<ul>" + p[0]

        print(p[0])

    except:
        print("--", p)
        p[0] = f"<li>{p[2]}</li></ul>"

def p_unordered_list(p):
    """ unordered_list : '*' TEXT EOL unordered_list
    | '*' TEXT EOL """
    print("--", p)
    try:
        p[0] = f"<li>{p[2]}</li>{p[3]}"
    except:
        p[0] = f"<li>{p[2]}</li></ul>"

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

    print(result)