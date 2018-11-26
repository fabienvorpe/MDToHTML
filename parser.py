import ply.yacc as yacc

from lex import tokens
import AST


def p_programme_statement(p):
    ''' programme : statement '''
    p[0] = AST.ProgramNode(p[1])

def p_statement(p):
    """ statement : TITLE1 """ # est ce que on add le tag html dans l'interpreteur ou on peut pas retrouver le type du token dan sl'interpreteur ???
    p[0] = AST.TokenNode(p[1])

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