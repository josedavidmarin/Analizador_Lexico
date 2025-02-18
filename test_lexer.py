import unittest
from lexer import tokenize, Token

class TestTokenizer(unittest.TestCase):
    def test_simple_tokens(self):
        text = "var x = 42; print(x);"
        tokens = [tok for tok in tokenize(text)]
        
        expected_tokens = [
            Token(type='VAR', value='var', lineno=1),
            Token(type='ID', value='x', lineno=1),
            Token(type='ASSIGN', value='=', lineno=1),
            Token(type='INTEGER', value='42', lineno=1),
            Token(type='SEMI', value=';', lineno=1),
            Token(type='PRINT', value='print', lineno=1),
            Token(type='LPAREN', value='(', lineno=1),
            Token(type='ID', value='x', lineno=1),
            Token(type='RPAREN', value=')', lineno=1),
            Token(type='SEMI', value=';', lineno=1),
        ]
        
        self.assertEqual(tokens, expected_tokens)

    def test_floats(self):
        text = "var x = 123.456; var y = 123.; var z = .456;"
        tokens = [tok for tok in tokenize(text)]
        
        expected_tokens = [
            Token(type='VAR', value='var', lineno=1),
            Token(type='ID', value='x', lineno=1),
            Token(type='ASSIGN', value='=', lineno=1),
            Token(type='FLOAT', value='123.456', lineno=1),
            Token(type='SEMI', value=';', lineno=1),
            Token(type='VAR', value='var', lineno=1),
            Token(type='ID', value='y', lineno=1),
            Token(type='ASSIGN', value='=', lineno=1),
            Token(type='FLOAT', value='123.', lineno=1),
            Token(type='SEMI', value=';', lineno=1),
            Token(type='VAR', value='var', lineno=1),
            Token(type='ID', value='z', lineno=1),
            Token(type='ASSIGN', value='=', lineno=1),
            Token(type='FLOAT', value='.456', lineno=1),
            Token(type='SEMI', value=';', lineno=1),
        ]
        
        self.assertEqual(tokens, expected_tokens)

    def test_comments(self):
        text = """
        // Este es un comentario de una línea
        var x = 42; /* Este es un comentario
        de múltiples líneas */
        """
        tokens = [tok for tok in tokenize(text)]
        
        expected_tokens = [
            Token(type='VAR', value='var', lineno=2),
            Token(type='ID', value='x', lineno=2),
            Token(type='ASSIGN', value='=', lineno=2),
            Token(type='INTEGER', value='42', lineno=2),
            Token(type='SEMI', value=';', lineno=2),
        ]
        
        self.assertEqual(tokens, expected_tokens)

    def test_char_literals(self):
        text = "var x = 'a'; var y = '\\n'; var z = '\\x41';"
        tokens = [tok for tok in tokenize(text)]
        
        expected_tokens = [
            Token(type='VAR', value='var', lineno=1),
            Token(type='ID', value='x', lineno=1),
            Token(type='ASSIGN', value='=', lineno=1),
            Token(type='CHAR', value='a', lineno=1),
            Token(type='SEMI', value=';', lineno=1),
            Token(type='VAR', value='var', lineno=1),
            Token(type='ID', value='y', lineno=1),
            Token(type='ASSIGN', value='=', lineno=1),
            Token(type='CHAR', value='\\n', lineno=1),
            Token(type='SEMI', value=';', lineno=1),
            Token(type='VAR', value='var', lineno=1),
            Token(type='ID', value='z', lineno=1),
            Token(type='ASSIGN', value='=', lineno=1),
            Token(type='CHAR', value='\\x41', lineno=1),
            Token(type='SEMI', value=';', lineno=1),
        ]
        
        self.assertEqual(tokens, expected_tokens)

    def test_keywords(self):
        text = "const var print return break continue if else while func import true false"
        tokens = [tok for tok in tokenize(text)]
        
        expected_tokens = [
            Token(type='CONST', value='const', lineno=1),
            Token(type='VAR', value='var', lineno=1),
            Token(type='PRINT', value='print', lineno=1),
            Token(type='RETURN', value='return', lineno=1),
            Token(type='BREAK', value='break', lineno=1),
            Token(type='CONTINUE', value='continue', lineno=1),
            Token(type='IF', value='if', lineno=1),
            Token(type='ELSE', value='else', lineno=1),
            Token(type='WHILE', value='while', lineno=1),
            Token(type='FUNC', value='func', lineno=1),
            Token(type='IMPORT', value='import', lineno=1),
            Token(type='TRUE', value='true', lineno=1),
            Token(type='FALSE', value='false', lineno=1),
        ]
        
        self.assertEqual(tokens, expected_tokens)


    def test_gox_code(self):
        text = """
        /* Programa que factoriza un número en sus números primos */

        func mod(a int, b int) int {
            return a - (a/b) * b;
        }

        func isprime(n int) bool {
            if n < 2 {
                return false;
            }
            var i int = 2;
            while i * i <= n {
                if n % i == 0 {
                    return false;
                }
                i = i + 1;
            }
            return true;
        }

        func factorize(n int) int {
            var factor int = 2;
        }
        """
        tokens = list(tokenize(text))

        expected_tokens = [
            # Comentario de múltiples líneas (ignorado)
            # Función `mod`
            Token(type='FUNC', value='func', lineno=3),
            Token(type='ID', value='mod', lineno=3),
            Token(type='LPAREN', value='(', lineno=3),
            Token(type='ID', value='a', lineno=3),
            Token(type='ID', value='int', lineno=3),
            Token(type='COMMA', value=',', lineno=3),
            Token(type='ID', value='b', lineno=3),
            Token(type='ID', value='int', lineno=3),
            Token(type='RPAREN', value=')', lineno=3),
            Token(type='ID', value='int', lineno=3),
            Token(type='LBRACE', value='{', lineno=3),
            Token(type='RETURN', value='return', lineno=4),
            Token(type='ID', value='a', lineno=4),
            Token(type='MINUS', value='-', lineno=4),
            Token(type='LPAREN', value='(', lineno=4),
            Token(type='ID', value='a', lineno=4),
            Token(type='DIVIDE', value='/', lineno=4),
            Token(type='ID', value='b', lineno=4),
            Token(type='RPAREN', value=')', lineno=4),
            Token(type='TIMES', value='*', lineno=4),
            Token(type='ID', value='b', lineno=4),
            Token(type='SEMI', value=';', lineno=4),
            Token(type='RBRACE', value='}', lineno=5),
            # Función `isprime`
            Token(type='FUNC', value='func', lineno=7),
            Token(type='ID', value='isprime', lineno=7),
            Token(type='LPAREN', value='(', lineno=7),
            Token(type='ID', value='n', lineno=7),
            Token(type='ID', value='int', lineno=7),
            Token(type='RPAREN', value=')', lineno=7),
            Token(type='ID', value='bool', lineno=7),
            Token(type='LBRACE', value='{', lineno=7),
            Token(type='IF', value='if', lineno=8),
            Token(type='ID', value='n', lineno=8),
            Token(type='LT', value='<', lineno=8),
            Token(type='INTEGER', value='2', lineno=8),
            Token(type='LBRACE', value='{', lineno=8),
            Token(type='RETURN', value='return', lineno=9),
            Token(type='FALSE', value='false', lineno=9),
            Token(type='SEMI', value=';', lineno=9),
            Token(type='RBRACE', value='}', lineno=10),
            Token(type='VAR', value='var', lineno=11),
            Token(type='ID', value='i', lineno=11),
            Token(type='ID', value='int', lineno=11),
            Token(type='ASSIGN', value='=', lineno=11),
            Token(type='INTEGER', value='2', lineno=11),
            Token(type='SEMI', value=';', lineno=11),
            Token(type='WHILE', value='while', lineno=12),
            Token(type='ID', value='i', lineno=12),
            Token(type='TIMES', value='*', lineno=12),
            Token(type='ID', value='i', lineno=12),
            Token(type='LE', value='<=', lineno=12),
            Token(type='ID', value='n', lineno=12),
            Token(type='LBRACE', value='{', lineno=12),
            Token(type='IF', value='if', lineno=13),
            Token(type='ID', value='n', lineno=13),
            Token(type='MOD', value='%', lineno=13),
            Token(type='ID', value='i', lineno=13),
            Token(type='EQ', value='==', lineno=13),
            Token(type='INTEGER', value='0', lineno=13),
            Token(type='LBRACE', value='{', lineno=13),
            Token(type='RETURN', value='return', lineno=14),
            Token(type='FALSE', value='false', lineno=14),
            Token(type='SEMI', value=';', lineno=14),
            Token(type='RBRACE', value='}', lineno=15),
            Token(type='ID', value='i', lineno=16),
            Token(type='ASSIGN', value='=', lineno=16),
            Token(type='ID', value='i', lineno=16),
            Token(type='PLUS', value='+', lineno=16),
            Token(type='INTEGER', value='1', lineno=16),
            Token(type='SEMI', value=';', lineno=16),
            Token(type='RBRACE', value='}', lineno=17),
            Token(type='RETURN', value='return', lineno=18),
            Token(type='TRUE', value='true', lineno=18),
            Token(type='SEMI', value=';', lineno=18),
            Token(type='RBRACE', value='}', lineno=19),
            # Función `factorize`
            Token(type='FUNC', value='func', lineno=21),
            Token(type='ID', value='factorize', lineno=21),
            Token(type='LPAREN', value='(', lineno=21),
            Token(type='ID', value='n', lineno=21),
            Token(type='ID', value='int', lineno=21),
            Token(type='RPAREN', value=')', lineno=21),
            Token(type='ID', value='int', lineno=21),
            Token(type='LBRACE', value='{', lineno=21),
            Token(type='VAR', value='var', lineno=22),
            Token(type='ID', value='factor', lineno=22),
            Token(type='ID', value='int', lineno=22),
            Token(type='ASSIGN', value='=', lineno=22),
            Token(type='INTEGER', value='2', lineno=22),
            Token(type='SEMI', value=';', lineno=22),
            Token(type='RBRACE', value='}', lineno=23),
        ]

        self.assertEqual(tokens, expected_tokens)


if __name__ == '__main__':
    unittest.main()
