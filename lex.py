import ply.lex as lex

tokens = (
	'TITLE',
	'TEXT',
	'EOL',
	'UNORDERED_LIST_IDENTIFIER',
	'ORDERED_LIST_INDEX',
	'CODE_SAMPLE',
	'BOLD_IDENTIFIER',
	'ITALIC_IDENTIFIER',
	'CROSSED_IDENTIFIER',
	'UNDERLINED_IDENTIFIER',
	'LOOP',
	'FIGURE',
)

literals = '{}_~'

def t_TITLE(t):
	r"\#+[ ].+"
	return t

def t_UNORDERED_LIST_IDENTIFIER(t):
	r"(- )"
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
	r"```[\s\S][^```]+```"
	t.value = t.value[3:-3]
	return t

def t_EOL(t):
	r"\n"
	return t

def t_LOOP(t):
	r"(!boucle!\[.+\])"
	return t

def t_FIGURE(t):
	r"(!figure!\[.+\])"
	return t

def t_TEXT(t):
	r"[^(\n)(\*\*)(\*)(\~\~)(\_\_)(\{)(\})]+"
	return t

t_ignore  = ' \t'

def t_error(t):
	print("Unknown token: ", t)
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
