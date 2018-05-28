#coding: utf-8
import re

reps = [
        # Punctuation
        (ur'\.'                , ';'      ),
        (ur'!'                 , '();'    ),

        # Comparison
        (ur'=/='               , '!='     ),
        (ur'(?<![!])='         , '=='     ),
        (ur'\bfor\b'           , '=='     ),

        # Assignment
        (ur'\bé\b'             , '='      ),
        (ur'\beh\b'            , '='      ),
        (ur'\bs(a|ã)o\b'       , '='      ),

        # Booleans
        (ur'\bverdadeiro\b'    , 'True'   ),
        (ur'\bfalso\b'         , 'False'  ),
        (ur'~'                 , 'not '   ),
        (ur'\bn(a|ã)o\b'       , 'not'    ),
        (ur'\bou\b'            , 'or'     ),
        (ur'\be\b'             , 'and'    ),

        # Control flow
        (ur'\bse\b'            , 'if'    ),
        (ur'\bsen(a|ã)o\b'     , 'else'  ),
        (ur'\benquanto\b'      , 'while' ),
        (ur'\bcada\b'          , 'for'   ),
        (ur'\bem\b'            , 'in'    ),

        # Functions
        (ur'\bfun(c|ç)(a|ã)o\b', 'def'   ),
        (ur'\bretorna\b'       , 'return'),

        # I/O
        (ur'\bmostra\b'        , 'print' ),
        (ur'\bentrada\b'       , 'input' ),
    ];


def replace_multiple(source): # a convenience replacement function
    if not source: return "" # no need to process empty strings
    for rep in reps:
        source = re.sub(rep[0], rep[1], source, flags=re.UNICODE)
    return source

def transpile(source):
    # A pattern to match strings between quotes
    QUOTED_STRING = re.compile("(\\\\?[\"']).*?\\1")

    # Unix: To match accented characters, the source must be converted to a Unicode object
    source = unicode(source, "utf-8")

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
    transpiled = "".join(result)

    # Since it's in Portuguese, we have to support non-ASCII characters
    return "#coding: utf-8\n" + transpiled

def make(filename):
    fin = open(filename, 'r')
    source = fin.read()
    fout = open(filename.replace('.clara', '.py'), 'w')
    fout.write(transpile(source).encode('utf-8'))
    fin.close()
    fout.close()

#make('teste.clara')
