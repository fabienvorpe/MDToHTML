import ply.lex as lex

reserved_words = (
)

tokens = (
	'TITLE',
	'TEXT',
	'EOL',
	'ORDERED_LIST_INDEX',
	'BOLD_TEXT',
	# 'UNORDERED_LIST_ELEMENT',
	# 'ORDERED_LIST_ELEMENT',
) # + tuple(map(lambda s:s.upper(),reserved_words))

literals = '*'

def t_TEXT(t):
	r"[A-Za-z]+"
	return t

def t_TITLE(t):
	r"\#+[ ].+"
	title_level = len(t.value.split()[0])
	nb_sharps = title_level
	if title_level > 6:
		title_level = 6
	t.value = f"<h{title_level}>{t.value[nb_sharps+1:]}</h{title_level}>"
	return t

def t_ORDERED_LIST_INDEX(t):
	r"\d+.+"
	t.value = t.value[len(t.value.split()[0])+1:]
	return t

def t_BOLD_TEXT(t):
	r"\*\*.+\*\*"
	t.value = t.value[2:-2]
	return t

def t_EOL(t):
	r"\n"
	return t

# def t_newline(t):
# 	r'\n+'
# 	t.lexer.lineno += len(t.value)

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
