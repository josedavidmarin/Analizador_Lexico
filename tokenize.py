import re

token_specification = [
    ('CONST', r'\bconst\b'),
    ('VAR', r'\bvar\b'),
    ('PRINT', r'\bprint\b'),
    ('RETURN', r'\breturn\b'),
    ('BREAK', r'\bbreak\b'),
    ('CONTINUE', r'\bcontinue\b'),
    ('IF', r'\bif\b'),
    ('ELSE', r'\belse\b'),
    ('WHILE', r'\bwhile\b'),
    ('FUNC', r'\bfunc\b'),
    ('IMPORT', r'\bimport\b'),
    ('TRUE', r'\btrue\b'),
    ('FALSE', r'\bfalse\b'),
    ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('FLOAT', r'\d+\.\d*|\.\d+'),
    ('INTEGER', r'\d+'),
    ('CHAR', r'\'([^\\']|\\.)\''),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('TIMES', r'\*'),
    ('DIVIDE', r'/'),
    ('LT', r'<'),
    ('LE', r'<='),
    ('GT', r'>'),
    ('GE', r'>='),
    ('EQ', r'=='),
    ('NE', r'!='),
    ('LAND', r'&&'),
    ('LOR', r'\|\|'),
    ('GROW', r'\^'),
    ('ASSIGN', r'='),
    ('SEMI', r';'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('COMMA', r','),
    ('DEREF', r'`'),
    ('COMMENT_SINGLE', r'//.*'),
    ('COMMENT_MULTI', r'/\*[\s\S]*?\*/'),
    ('NEWLINE', r'\n'),
    ('SKIP', r'[ \t]+'),
    ('MISMATCH', r'.'),
]

token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)

def tokenize(code):
    tokens = []
    line_number = 1
    for match in re.finditer(token_regex, code):
        kind = match.lastgroup
        value = match.group(kind)
        if kind == 'NEWLINE':
            line_number += 1
        elif kind == 'SKIP' or kind == 'COMMENT_SINGLE' or kind == 'COMMENT_MULTI':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Error en la línea {line_number}: Carácter ilegal {value!r}')
        else:
            tokens.append((kind, value, line_number))
    return tokens
