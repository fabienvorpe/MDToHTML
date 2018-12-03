import ply.lex as lex

reserved_words = (
)

tokens = (
	'TITLE',
	'TEXT',
	'EOF',
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

# def t_UNORDERED_LIST_ELEMENT(t):
# 	r"\*[ ].+"
# 	t.value = f"<li>{t.value[2:]}</li>"
# 	return t

# def t_ORDERED_LIST_ELEMENT(t):
# 	r"[0-9]+\.[ ].+"
# 	t.value = f"<li>{t.value[3:]}</li>"
# 	return t

def t_EOF(t):
	r"\n+"
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
