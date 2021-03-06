#coding: utf-8
import sys
import re
import StringIO

reps = [
    # Remove extra spacing
    (r'(?<=\S)  +'             , ' '                ),

    # Punctuation
    (r'(\w+) ?\.\.\. ?(\w+)'   , 'range(\\1, \\2+1)'),
    (r'\.'                     , ';'                ),
    (r'(\d+),(\d+)'            , '(\\1.\\2)'        ),
    (r'!'                      , '();'              ),

    # Comparison
    (r'=/='                    , '!='               ),
    (r'\bn(a|ã)o for\b'        , '!='               ),
    (r'(?<![!])='              , '=='               ),
    (r'\bfor\b'                , '=='               ),

    # Assignment
    (r' é '                    , ' = '              ), # \b is weird with accented characters
    (r'\beh\b'                 , '='                ),
    (r'\bs(a|ã)o\b'            , '='                ),

    # Operators
    (r'\baumenta\b'            , '+='               ),
    (r'\bdiminui\b'            , '-='               ),
    (r'% de'                   , '% *'              ),
    (r'\)%'                    , ')/100.0'          ),
    (r'(\w+)%'                 , '(\\1/100.0)'      ),
    (r'\bresto\b'              , '%'                ),
    (r'\^'                     , '**'               ),
    (r'\|(.+?)\|'              , 'tamanho(\\1)'     ),
    (r'\bl(e|ê)\b (\w+)'       , '\\2 = raw_input()'),

    # Booleans
    (r'\bverdadeiro\b'         , 'True'             ),
    (r'\bfalso\b'              , 'False'            ),
    (r'~'                      , 'not '             ),
    (r'\bn(a|ã)o\b'            , 'not'              ),
    (r'\bou\b'                 , 'or'               ),
    (r'\be\b'                  , 'and'              ),

    # Control flow
    (r'(.+)\?'                 , 'if \\1:'          ),
    (r'\bse\b'                 , 'if'               ),
    (r'\bsen(a|ã)o\b'          , 'else'             ),
    (r'\benquanto\b'           , 'while'            ),
    (r'\b(pa?ra )?cada\b'      , 'for'              ),
    (r'\bem\b'                 , 'in'               ),
    (r'\bsai\b'                , 'break'            ),
    (r'\bcontinua\b'           , 'continue'         ),

    # Functions
    (r'\bfun(c|ç)(a|ã)o\b'     , 'def'              ),
    (r'\bretorna\b'            , 'return'           ),
    (r'def (\w+):'             , 'def \\1():'       ),

    # Properties and 'self'
    (r'\bdele\b'               , 'de ele'           ), # (1) nome dele -> nome de ele
    (r'\bdela\b'               , 'de ela'           ), # (1) nome dela -> nome de ela
    (r'\bel(e|a)\b'            , 'self'             ), # (2) nome de ele -> nome de self
    (r'(\w+) d(e|o|a) (\w+)'   , '\\3.\\1'          ), # (3) nome de self -> self.nome

    # Translate list methods, as the native types can't be extended
    (r'adiciona'               , 'append'           ),
    (r'insere'                 , 'insert'           ),
    (r'remove'                 , 'pop'              ),
    (r'indice'                 , 'index'            ),

    # Classes
    (r'uma? (\w+) = uma? (\w+)', 'class \\1(\\2)'   ), # um cao eh um animal -> class cao(animal)
    (r'= uma?'                 , '='                ), # meu_cao eh um cao() -> meu_cao = cao()
    (r'\b[cC]oisa\b'           , 'object'           ), # class cao(objeto) -> class cao(object)
    (r'recebe ?\((.*)\)'       , '__init__(\\1)'    ), # recebe (nome) -> __init__ (nome)
    (r'(?<!\w)que (\w+) ?:'    , 'que \\1():'       ), # que late: -> que late():
    (r'(?<!\w)que (.+\()'      , 'def \\1self, '    ), # que late(): -> def late(self):
];

def replace_methods(match):
    # Replace 'a b' with 'a.b' if a and b aren't keywords
    a = match.group(1)
    b = match.group(2)
    keywords = 'if else while for in and or not print def return class'.split()
    if a in keywords or b in keywords: return a + ' '
    else: return a + '.'

def replace_multiple(source):
    if not source: return "" # No need to process empty strings
    for rep in reps:
        source = re.sub(rep[0], rep[1], source, flags=re.UNICODE)
    # Replace methods: meu_gato mia() -> meu_gato.mia()
    source = re.sub('(\w+) (?=(\w+))', replace_methods, source)
    return source

def transpile(source):
    # A pattern to match strings between quotes
    QUOTED_STRING = re.compile("(\\\\?[\"']).*?\\1")

    result = []  # a store for the result pieces
    head = 0  # a search head reference
    for match in QUOTED_STRING.finditer(source):
        # process everything until the current quoted match and add it to the result
        result.append(replace_multiple(source[head:match.start()]))
        result.append(match.group(0))  # add the quoted match verbatim to the result
        head = match.end()  # move the search head to the end of the quoted match
    if head < len(source):  # if the search head is not at the end of the string
        # process the rest of the string and add it to the result
        result.append(replace_multiple(source[head:]))

    # Join back the result pieces
    transpiled = ''.join(result)

    # Support non-ASCII characters and the Clara standard library
    return '#coding: utf-8\nfrom standard_library import *\n' + transpiled

sys.stdin = StringIO.StringIO(sys.argv[2])
exec(transpile(sys.argv[1]))
