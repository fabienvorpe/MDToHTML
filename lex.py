import ply.lex as lex

reserved_words = (
)

tokens = (
	'TITLE',
	'TEXT',
	'EOL',
	'ORDERED_LIST_INDEX',
	'CODE_SAMPLE',
	'BOLD_IDENTIFIER',
	'ITALIC_IDENTIFIER',
	'CROSSED_IDENTIFIER',
	'UNDERLINED_IDENTIFIER',
) # + tuple(map(lambda s:s.upper(),reserved_words))

literals = '-'

def t_TEXT(t):
	r"[A-Za-z ]+"
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
	r"\d+\."
	return t

def t_BOLD_IDENTIFIER(t):
	r"\*\*"
	return t

def t_ITALIC_IDENTIFIER(t):
	r"\*"
	return t

def t_CROSSED_IDENTIFIER(t):
	r"\~\~"
	return t

def t_UNDERLINED_IDENTIFIER(t):
	r"\_\_"
	return t

def t_CODE_SAMPLE(t):
	r"```[\s\S][^(```)]+```"
	t.value = t.value[3:-3]
	return t

def t_EOL(t):
	r"\n"
	return t

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
