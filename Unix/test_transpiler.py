import unittest
from transpiler import transpile

# Unit testing for the Clara transpiler.
class TranspilerTDD(unittest.TestCase):
    def test_adds_encoding(self):
        source = ""
        result = transpile(source);
        expected = "#coding: utf-8\n"
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
