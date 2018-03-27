# coding: utf-8
import re
import io

f = io.open('clara', mode='r', encoding='utf-8')
#f = open('clara', 'r')
original = f.read()

transpiled = original

reps = [
    # Punctuation
    (ur'\b\.\b'        , ';'     ),
    (ur'\b!\b'         , '();'   ),

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
    (ur'\bou\b'        , 'ou'    ),
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
for rep in reps:
    pattern, translated = rep;

    # Excludes stuff between double quotes. Don't worry about it.
    pattern = r'(?!\B"[^"]*)' + pattern + r'(?![^"]*"\B)'

    # Excludes stuff between single quotes. Don't worry about it either.
    pattern = r"(?!\B'[^']*)" + pattern + r"(?![^']*'\B)"

    # Replaces every [pattern] with [translated] in [transpiled]
    transpiled = re.sub(pattern, translated, transpiled, flags=re.UNICODE)

open('transpilado', 'w').write(transpiled.encode('utf8'))
f.close()
