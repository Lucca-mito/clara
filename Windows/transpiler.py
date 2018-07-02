#coding: utf-8
import re

reps = [
    # Remove extra spacing
    (ur'(?<=\S)  +'             , ' '             ),

    # Punctuation
    (ur'\.'                     , ';'             ),
    (ur'!'                      , '();'           ),

    # Comparison
    (ur'=/='                    , '!='            ),
    (ur'\bn[aã]o for\b'         , '!='            ),
    (ur'(?<![!])='              , '=='            ),
    (ur'\bfor\b'                , '=='            ),

    # Assignment
    (ur'\bé\b'                  , '='             ),
    (ur'\beh\b'                 , '='             ),
    (ur'\bs[aã]o\b'             , '='             ),

    # Operators
    (ur'% de'                   , '% *'           ),
    (ur'(\w+)%'                 , '(\\1/100.0)'   ),
    (ur'\bresto\b'              , '%'             ),
    (ur'\^'                     , '**'            ),

    # Booleans
    (ur'\bverdadeiro\b'         , 'True'          ),
    (ur'\bfalso\b'              , 'False'         ),
    (ur'~'                      , 'not '          ),
    (ur'\bn[aã]o\b'             , 'not'           ),
    (ur'\bou\b'                 , 'or'            ),
    (ur'\be\b'                  , 'and'           ),

    # Control flow
    (ur'(.+)\?'                 , 'if \\1:'       ),
    (ur'\bse\b'                 , 'if'            ),
    (ur'\bsen[aã]o\b'           , 'else'          ),
    (ur'\benquanto\b'           , 'while'         ),
    (ur'\b(pa?ra )?cada\b'      , 'for'           ),
    (ur'\bem\b'                 , 'in'            ),

    # Functions
    (ur'\bfun[cç][aã]o\b'       , 'def'           ),
    (ur'\bretorna\b'            , 'return'        ),
    (ur'def (\w+):'             , 'def \\1():'    ),

    # Properties and self
    (ur'\bdele\b'               , 'de ele'        ), # (1) nome dele -> nome de ele
    (ur'\bdela\b'               , 'de ela'        ), # (1) nome dela -> nome de ela
    (ur'\bel[ea]\b'             , 'self'          ), # (2) nome de ele -> nome de self
    (ur'(\w+) d[eoa] (\w+)'     , '\\2.\\1'       ), # (3) nome de self -> self.nome

    # Classes
    (ur'uma? (\w+) = uma? (\w+)', 'class \\1(\\2)'), # um cao eh um animal -> class cao(animal)
    (ur'= uma?'                 , '='             ), # meu_cao eh um cao() -> meu_cao = cao()
    (ur'[oO]bjeto'              , 'object'        ), # class cao(objeto) -> class cao(object)
    (ur'recebe\((.*)\)'         , '__init__(\\1)' ), # recebe(_nome) -> __init__(_nome)
    (ur'(?<!\w)que (\w+) *:'    , 'que \\1():'    ), # que late: -> que late():
    (ur'(?<!\w)que (.+\()'      , 'def \\1self, ' ), # que late(): -> def late(self):

    # I/O
    (ur'\bmostra\b'             , 'print'         ),
    (ur'\bentrada\b'            , 'input'         ),
];

def replace_methods(match):
    # Replace 'a b' with 'a.b' if a and b aren't keywords
    a = match.group(1)
    b = match.group(2)
    keywords = 'if else while for in and or not print def return class'.split()
    if a in keywords or b in keywords: return a + ' ' + b
    else: return a + '.' + b

def replace_multiple(source): # a convenience replacement function
    if not source: return "" # no need to process empty strings
    for rep in reps:
        source = re.sub(rep[0], rep[1], source, flags=re.UNICODE)
    # Replace methods: meu_gato mia() -> meu_gato.mia()
    source = re.sub('(\w+) (\w+)', replace_methods, source)
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

    # Since it's in Portuguese, we have to support non-ASCII characters
    return '#coding: utf-8\n' + transpiled

def make(filename): # Remove in the future, obviously
    fin = open(filename, 'r')
    source = fin.read()
    fout = open(filename.replace('.clara', '.py'), 'w')
    fout.write(transpile(source))
    fin.close()
    fout.close()

#make('teste.clara')
