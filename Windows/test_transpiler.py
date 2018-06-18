#coding: utf-8
import unittest
from transpiler import transpile

# Unit testing for the Clara transpiler.
class TranspilerTDD(unittest.TestCase):
    def test_adds_encoding(self):
        source   = ''
        expected = '#coding: utf-8\n'
        self.assertEqual(expected, transpile(source))

    def test_period_to_semicolon(self):
        source   =  'something.'
        expected = ('#coding: utf-8\n'
                    'something;')
        self.assertEqual(expected, transpile(source))

    def test_assignment_without_accent(self):
        source   =  'minha_idade eh 17'
        expected = ('#coding: utf-8\n'
                    'minha_idade = 17')
        self.assertEqual(expected, transpile(source))

#    def test_assignment_with_accent(self):
#        source   =  'minha_idade é 17'
#        expected = ('#coding: utf-8\n'
#                    'minha_idade = 17')
#        self.assertEqual(expected, transpile(source))

    def test_array_assignment(self):
        source   = ('numeros sao 1, 2, 3\n'
                    'um, dois, tres sao numeros')
        expected = ('#coding: utf-8\n'
                    'numeros = 1, 2, 3\n'
                    'um, dois, tres = numeros')
        self.assertEqual(expected, transpile(source))

    def test_excludes_strings(self):
        source   =  '"mostra quem vc eh!"'
        expected = ('#coding: utf-8\n'
                    '"mostra quem vc eh!"')
        self.assertEqual(expected, transpile(source))

    def test_supports_escaped_quotes(self):
        source   =  'mostra "\\"Não perca a cabeça\\" - Robespierre"'
        expected = ('#coding: utf-8\n'
                    'print "\\"Não perca a cabeça\\" - Robespierre"')
        self.assertEqual(expected, transpile(source))

    def test_equality_operator(self):
        source   =  'a = b'
        expected = ('#coding: utf-8\n'
                    'a == b')
        self.assertEqual(expected, transpile(source))

    def test_inequality_operator(self):
        source   =  'a =/= b'
        expected = ('#coding: utf-8\n'
                    'a != b')
        self.assertEqual(expected, transpile(source))

    def test_function_definition(self):
        source   = ('funcao f(x):\n'
                    '    retorna 2*x')
        expected = ('#coding: utf-8\n'
                    'def f(x):\n'
                    '    return 2*x')
        self.assertEqual(expected, transpile(source))

    def test_property_access(self):
        source   =  'propriedade do objeto'
        expected = ('#coding: utf-8\n'
                    'objeto.propriedade')
        self.assertEqual(expected, transpile(source))

if __name__ == '__main__':
    unittest.main()
