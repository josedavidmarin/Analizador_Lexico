'''
El papel del Analizador Léxico es convertir texto dentro 
de símbolos reconocidos.

El Analizador de GOX es requerido para reconocer los 
siguientes símbolos. Los nombres sugeridos para el token 
está al lado izquierdo. La coincidencia de texto está a la
derecha.

Palabras Reservadas:
    CONST       : 'const'
    VAR         : 'var'
    PRINT       : 'print'
    RETURN      : 'return'
    BREAK       : 'break'
    CONTINUE    : 'continue'
    IF          : 'if'
    ELSE        : 'else'
    WHILE       : 'while'
    FUNC        : 'func'
    IMPORT      : 'import'
    TRUE        : 'true'
    FALSE       : 'false'

Identificadores:
    ID          : Texto que comienza con una letra y
                    seguido de letras y dígitos.
                  Ejemplos: 'a', 'abc', 'a1', 'a1b2c3'
                  '_abc', 'a_b_c'

Literales:
    INTEGER     : 123 (decimales)

    FLOAT       : 123.456
                : 123.
                : .456  

    CHAR        : 'a'   (carácter simple - byte)
                : '\n'  (carácter de escape)
                : '\x41' (carácter hexadecimal)
                : '\''  (comilla simple)

    STRING      : "hola" (cadena de caracteres)

Operadores:
    PLUS        : '+'
    MINUS       : '-'
    TIMES       : '*'
    DIVIDE      : '/'
    LT          : '<'
    LE          : '<=' 
    GT          : '>'
    GE          : '>='
    EQ          : '=='
    NE          : '!='
    LAND        : '&&'
    LOR         : '||'
    GROW        : '^'

Símbolos Misceláneos:
    ASSIGN      : '='           
    SEMI        : ';'
    LPAREN      : '('
    RPAREN      : ')'
    LBRACE      : '{'
    RBRACE      : '}'
    COMMA       : ','
    DEREF       : '`'

Comentarios: Para ser ignorados
    //          : Comentario de una línea
    /* ... */   : Comentario de múltiples líneas

Errores: Su analizador léxico debe reconocer opcionalmente
y reportar los siguientes errores:

    lineno: Carácter ilegal 'c'
    lineno: Carácter no terminado 'c
    lineno: Comentario no terminado
'''
from dataclasses import dataclass
import re

# Expresiones regulares para identificar tokens
NAME_PAT = re.compile(r'[a-zA-Z_]\w*')
INT_PAT = re.compile(r'\d+')
#FLOAT_PAT = re.compile(r'\d+\.\d*|\.\d+')  # Asegúrate de que esta línea esté correcta
FLOAT_PAT = re.compile(r'\d*\.\d+|\d+\.\d*')
STRING_PAT = re.compile(r'"(\\"|[^"])*"')  # Cadena de caracteres
CHAR_PAT = re.compile(r"'(\\'|\\[nrt]|\\x[0-9a-fA-F]{2}|[^\\])'")  # Caracteres con escape

# Operadores de dos caracteres
TWO_CHAR = {
    '<=': 'LE',
    '>=': 'GE',
    '==': 'EQ',
    '!=': 'NE',
    '&&': 'LAND',
    '||': 'LOR',
}

# Operadores de un carácter
ONE_CHAR = {
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'TIMES',
    '/': 'DIVIDE',
    '<': 'LT',
    '>': 'GT',
    '=': 'ASSIGN',
    ';': 'SEMI',
    '(': 'LPAREN',
    ')': 'RPAREN',
    '{': 'LBRACE',
    '}': 'RBRACE',
    ',': 'COMMA',
    '^': 'GROW',
    '`': 'DEREF',
    '%': 'MOD',
}

# Palabras reservadas
KEYWORDS = {
    'const': 'CONST',
    'var': 'VAR',
    'print': 'PRINT',
    'return': 'RETURN',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'func': 'FUNC',
    'import': 'IMPORT',
    'true': 'TRUE',
    'false': 'FALSE'
}

@dataclass
class Token:
    type: str
    value: str
    lineno: int

def tokenize(text):

    # Elimina espacios y saltos de línea iniciales para ajustar la numeración de líneas
    text = text.lstrip()

    index = 0  # Índice del texto 
    lineno = 1  # Contador de líneas

    while index < len(text):
        # Comentario de una línea
        if text[index:index+2] == '//':
            index += 2
            while index < len(text) and text[index] != '\n':
                index += 1
            if index < len(text) and text[index] == '\n':
                lineno += 1
                index += 1
            continue

        # Comentario de múltiples líneas
        elif text[index:index+2] == '/*':
            index += 2
            start_lineno = lineno  # Guardamos la línea donde empieza el comentario
            while index < len(text) - 1:
                if text[index] == '\n':
                    lineno += 1
                elif text[index:index+2] == '*/':  # Si encontramos el cierre
                    index += 2
                    break
                index += 1
            else:
                # Si el bucle termina sin encontrar '*/', el comentario no se cerró
                raise SyntaxError(f"Línea {start_lineno}: Error - Comentario no terminado")

        # Espacios en blanco
        if text[index] in ' \t':
            index += 1
            continue

        # Nueva línea
        elif text[index] == '\n':
            lineno += 1
            index += 1
            continue

        # Identificadores y palabras reservadas
        elif match := NAME_PAT.match(text, index):
            value = match.group()
            if value in KEYWORDS:
                yield Token(KEYWORDS[value], value, lineno)
            else:
                yield Token('ID', value, lineno)
            index = match.end()

        # Flotantes
        elif match := FLOAT_PAT.match(text, index):
            yield Token('FLOAT', match.group(), lineno)
            index = match.end()

        # Enteros
        elif match := INT_PAT.match(text, index):
            yield Token('INTEGER', match.group(), lineno)
            index = match.end()

        # Cadenas de caracteres
        elif match := STRING_PAT.match(text, index):
            yield Token('STRING', match.group(), lineno)
            index = match.end()

        # Caracteres
        elif match := CHAR_PAT.match(text, index):
            char_value = match.group()[1:-1]  # Elimina las comillas simples
            yield Token('CHAR', char_value, lineno)
            index = match.end()

        # Operadores de dos caracteres
        elif two_char := TWO_CHAR.get(text[index:index+2]):
            yield Token(two_char, text[index:index+2], lineno)
            index += 2

        # Operadores de un carácter
        elif one_char := ONE_CHAR.get(text[index]):
            yield Token(one_char, text[index], lineno)
            index += 1

        # Caracteres no reconocidos
        else:
            raise SyntaxError(f"Linea {lineno}: Error - Caracter ilegal '{text[index]}'")

def main(arg):
    if len(arg) != 2:
        raise SystemExit(f'Usage: {arg[0]} filename')
    with open(arg[1]) as file:
        for tok in tokenize(file.read()):
            print(tok)
    
if __name__ == '__main__':
    import sys
    main(sys.argv)
