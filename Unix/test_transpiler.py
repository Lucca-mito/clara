#coding: utf-8
import unittest
from subprocess import check_output
from transpiler import transpile

def test(self, source, expected):
    transpiled = transpile(source)
    fout = open('unittest_playground.py', 'w')
    fout.write(transpiled.encode('utf-8'))
    fout.close()
    output = check_output(['python', 'unittest_playground.py'])[:-1] # Remove trailing newline
    self.assertEqual(output, expected)

# Unit testing for the Clara transpiler.
class TranspilerTDD(unittest.TestCase):
    def test_output(self):
        test(self,
        'mostra "Olá, mundo!"',
        'Olá, mundo!')

    def test_assignment_without_accent(self):
        test(self,
        'meu_nome eh "Lucca". mostra meu_nome',
        'Lucca')

    def test_assignment_with_accent(self):
        test(self,
        'meu_nome é "Lucca". mostra meu_nome',
        'Lucca')

    def test_multiple_assignment(self):
        test(self,
            ('numeros são 1, 2, 3\n'
             'um, dois, tres são numeros\n'
             'mostra tres, dois, um'),
        '3 2 1')

    def test_excludes_strings(self):
        test(self,
        'mostra "mostra quem você é!"',
        'mostra quem você é!')

    def test_equality_operator(self):
        test(self,
        'mostra 1 + 1 = 2',
        'True')

    def test_inequality_operator(self):
        test(self,
        'mostra 1 + 1 =/= 2',
        'False')

    def test_remainder_operator(self):
        test(self,
        'mostra 10 resto 3',
        '1')

    def test_percentage_operator(self):
        test(self,
        'mostra 25% de 30',
        '7.5')

    def test_if_else(self):
        test(self,
            ('se 3 + 4 não for 5: mostra "Faz sentido"\n'
             'senão: mostra "Algo de errado não está certo..."'),
        'Faz sentido')

    def test_question_mark_and_exclamation_mark_operators(self):
        test(self,
            ('ta_chovendo é verdadeiro\n'
             'função corre():\n'
             '    mostra "Tô correndo!"\n'
             'ta_chovendo? corre!'),
        'Tô correndo!')

    def test_function_with_parameters(self):
        test(self,
            ('função f(x):\n'
             '    retorna 2 * x\n'
             'mostra f(5)'),
        '10')

    def test_function_without_parameters(self):
        test(self,
            ('função late:\n'
             '    mostra "Au, au!"\n'
             'late!'),
        'Au, au!')

    def test_classes_and_object_properties(self):
        test(self,
            ('um cao é um objeto:\n'
             '    que recebe(nome):\n'
             '        nome dele é nome\n'
             'meu_cao é um cao("Stark")\n'
             'mostra nome do meu_cao'),
        'Stark')

    def test_method_calling(self):
        test(self,
            ('um cao é um objeto:\n'
             '    que late: mostra "Au, au!"\n'
             'meu_cao é um cao()\n'
             'meu_cao late!'),
        'Au, au!')

    def test_inheritance(self):
        test(self,
            ('um animal é um objeto:\n'
             '    que fala:\n'
             '        mostra nome dele + " diz " + som dele + "!"\n'
             'um gato é um animal:\n'
             '    que recebe(nome):\n'
             '        nome dele é nome\n'
             '        som dele é "miau"\n'
             'meu_gato é um gato("Snowy")\n'
             'meu_gato fala!'),
        'Snowy diz miau!')

if __name__ == '__main__':
    unittest.main()
