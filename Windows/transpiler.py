#coding: utf-8
import re

reps = [
        # Punctuation
        (ur'\.'            , ';'     ),
        (ur'!'             , '();'   ),

        # Comparison
        (ur'='             , '=='    ),
        (ur'\bfor\b'       , '=='    ),

        # Assignment
        (ur'\bé\b'         , '='     ),
        (ur'\beh\b'        , '='     ),
        (ur'\bsão\b'       , '='     ),
        (ur'\bsao\b'       , '='     ),

        # Booleans
        (ur'\bverdadeiro\b', 'True'  ),
        (ur'\bfalso\b'     , 'False' ),
        (ur'~'             , 'not '  ),
        (ur'\bnão\b'       , 'not'   ),
        (ur'\bnao\b'       , 'not'   ),
        (ur'\bou\b'        , 'or'    ),
        (ur'\be\b'         , 'and'   ),

        # Control flow
        (ur'\bse\b'        , 'if'    ),
        (ur'\bsenão\b'     , 'else'  ),
        (ur'\bsenao\b'     , 'else'  ),
        (ur'\benquanto\b'  , 'while' ),
        (ur'\bcada\b'      , 'for'   ),
        (ur'\bem\b'        , 'in'    ),

        # Functions
        (ur'\bfunção\b'    , 'def'   ),
        (ur'\bfunçao\b'    , 'def'   ),
        (ur'\bfuncão\b'    , 'def'   ),
        (ur'\bfuncao\b'    , 'def'   ),
        (ur'\bretorna\b'   , 'return'),

        # I/O
        (ur'\bmostra\b'    , 'print' ),
        (ur'\bentrada\b'   , 'input' ),
    ];


def replace_multiple(source): # a convenience replacement function
    if not source: return "" # no need to process empty strings
    for rep in reps:
        source = re.sub(rep[0], rep[1], source, flags=re.UNICODE)
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
    transpiled = "".join(result)

    # Since it's in Portuguese, we have to support non-ASCII characters
    return "#coding: utf-8\n" + transpiled

# fin = open('teste.clara', 'r')
# source = fin.read()
# fout = open('teste.py', 'w')
# fout.write(transpile(source))
# fout.close()
