import ply.lex as lex

reserved_words = (
)

tokens = (
	'TITLE1',
	'TEXT',
) # + tuple(map(lambda s:s.upper(),reserved_words))

literals = ''

def t_TITLE1(t):
	r"\# .+\n"
	t = t[2:-2] 
	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
	print ("Illegal character '%s'" % repr(t.value[0]))
	t.lexer.skip(1)

lex.lex()

if __name__ == "__main__":
	import sys
	prog = open(sys.argv[1]).read()

	lex.input(prog)

	while 1:
		tok = lex.token()
		if not tok: 
			break
		print ("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))
