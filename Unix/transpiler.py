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
    (ur'\bn(a|ã)o for\b'        , '!='            ),
    (ur'(?<![!])='              , '=='            ),
    (ur'\bfor\b'                , '=='            ),

    # Assignment
    (ur'\bé\b'                  , '='             ),
    (ur'\beh\b'                 , '='             ),
    (ur'\bs(a|ã)o\b'            , '='             ),

    # Operators
    (ur'% de'                   , '% *'           ),
    (ur'(\w+)%'                 , '(\\1/100.0)'   ),
    (ur'\bresto\b'              , '%'             ),
    (ur'\^'                     , '**'            ),

    # Booleans
    (ur'\bverdadeiro\b'         , 'True'          ),
    (ur'\bfalso\b'              , 'False'         ),
    (ur'~'                      , 'not '          ),
    (ur'\bn(a|ã)o\b'            , 'not'           ),
    (ur'\bou\b'                 , 'or'            ),
    (ur'\be\b'                  , 'and'           ),

    # Control flow
    (ur'(.+)\?'                 , 'if \\1:'       ),
    (ur'\bse\b'                 , 'if'            ),
    (ur'\bsen(a|ã)o\b'          , 'else'          ),
    (ur'\benquanto\b'           , 'while'         ),
    (ur'\b(pa*ra )*cada\b'      , 'for'           ),
    (ur'\bem\b'                 , 'in'            ),

    # Functions
    (ur'\bfun(c|ç)(a|ã)o\b'     , 'def'           ),
    (ur'\bretorna\b'            , 'return'        ),
    (ur'def (\w+):'             , 'def \\1():'    ),

    # OOP
    (ur'(\w+) d(e|o|a) (\w+)'   , '\\3.\\1'       ), # nome do obj -> obj.nome
    (ur'(\w+) del(e|a)'         , 'self.\\1'      ), # nome dele -> self.nome
    (ur'uma* (\w+) = uma* (\w+)', 'class \\1(\\2)'), # um cao eh um animal -> class cao(animal)
    (ur'= uma*'                 , '='             ), # meu_cao eh um cao() -> meu_cao = cao()
    (ur'(o|O)bjeto'             , 'object'        ), # class cao(objeto) -> class cao(object)
    (ur'recebe\((.*)\)'         , '__init__(\\1)' ), # recebe(_nome) -> __init__(_nome)
    (ur'que (\w+) *:'           , 'que \\1():'    ), # que late: -> que late():
    (ur'que (.+\()'             , 'def \\1self, ' ), # que late(): -> def late(self):

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

def replace_multiple(source):
    if not source: return "" # No need to process empty strings
    for rep in reps:
        source = re.sub(rep[0], rep[1], source, flags=re.UNICODE)
    # Replace methods: meu_gato mia() -> meu_gato.mia()
    source = re.sub('(\w+) (\w+)', replace_methods, source)
    return source

def transpile(source):
    # A pattern to match strings between quotes
    QUOTED_STRING = re.compile("(\\\\?[\"']).*?\\1")

    # Unix: To match accented characters, the source must be converted to a Unicode object
    source = unicode(source, 'utf-8')

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
    fout.write(transpile(source).encode('utf-8'))
    fin.close()
    fout.close()

make('teste.clara')
