import unittest
from tokenize import tokenize

class TestGoxLexer(unittest.TestCase):
    
    def test_keywords(self):
        code = "const var print return if else while func"
        expected_tokens = [
            ('CONST', 'const', 1),
            ('VAR', 'var', 1),
            ('PRINT', 'print', 1),
            ('RETURN', 'return', 1),
            ('IF', 'if', 1),
            ('ELSE', 'else', 1),
            ('WHILE', 'while', 1),
            ('FUNC', 'func', 1)
        ]
        self.assertEqual(tokenize(code), expected_tokens)
    
    def test_identifiers(self):
        code = "x var_1 _private"
        expected_tokens = [
            ('ID', 'x', 1),
            ('ID', 'var_1', 1),
            ('ID', '_private', 1)
        ]
        self.assertEqual(tokenize(code), expected_tokens)
    
    def test_numbers(self):
        code = "123 45.67 .89"
        expected_tokens = [
            ('INTEGER', '123', 1),
            ('FLOAT', '45.67', 1),
            ('FLOAT', '.89', 1)
        ]
        self.assertEqual(tokenize(code), expected_tokens)
    
    def test_characters(self):
        code = "'a' '\n' '\x41' ' '"
        expected_tokens = [
            ('CHAR', "'a'", 1),
            ('CHAR', "'\n'", 1),
            ('CHAR', "'\x41'", 1),
            ('CHAR', "' '", 1)
        ]
        self.assertEqual(tokenize(code), expected_tokens)
    
    def test_operators(self):
        code = "+ - * / < <= > >= == != && || ^"
        expected_tokens = [
            ('PLUS', '+', 1),
            ('MINUS', '-', 1),
            ('TIMES', '*', 1),
            ('DIVIDE', '/', 1),
            ('LT', '<', 1),
            ('LE', '<=', 1),
            ('GT', '>', 1),
            ('GE', '>=', 1),
            ('EQ', '==', 1),
            ('NE', '!=', 1),
            ('LAND', '&&', 1),
            ('LOR', '||', 1),
            ('GROW', '^', 1)
        ]
        self.assertEqual(tokenize(code), expected_tokens)
    
    def test_symbols(self):
        code = "= ; ( ) { } , `"
        expected_tokens = [
            ('ASSIGN', '=', 1),
            ('SEMI', ';', 1),
            ('LPAREN', '(', 1),
            ('RPAREN', ')', 1),
            ('LBRACE', '{', 1),
            ('RBRACE', '}', 1),
            ('COMMA', ',', 1),
            ('DEREF', '`', 1)
        ]
        self.assertEqual(tokenize(code), expected_tokens)
    
    def test_comments(self):
        code = "// Esto es un comentario\nvar x = 10; /* comentario largo */"
        expected_tokens = [
            ('VAR', 'var', 2),
            ('ID', 'x', 2),
            ('ASSIGN', '=', 2),
            ('INTEGER', '10', 2),
            ('SEMI', ';', 2)
        ]
        self.assertEqual(tokenize(code), expected_tokens)
    
    def test_invalid_characters(self):
        code = "var x = @"
        with self.assertRaises(RuntimeError) as context:
            tokenize(code)
        self.assertIn("Carácter ilegal '@'", str(context.exception))

if __name__ == '__main__':
    unittest.main()
