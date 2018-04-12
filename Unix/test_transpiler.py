import unittest
from transpiler import transpile

# Unit testing for the Clara transpiler.
class TranspilerTDD(unittest.TestCase):
    def test_adds_encoding(self):
        source = ""
        result = transpile(source);
        expected = "#coding: utf-8\n"
        self.assertEqual(result, expected)

    def test_period_to_semicolon(self):
        source = "something."
        expected = (
            "#coding: utf-8\n"
            "something;"
        )
        self.assertEqual(transpile(source), expected)
        
    def test_assignment_without_accent(self):
        source = "minha_idade eh 17"
        expected = (
            "#coding: utf-8\n"
            "minha_idade = 17"
        )
        self.assertEqual(transpile(source), expected)

if __name__ == '__main__':
    unittest.main()
