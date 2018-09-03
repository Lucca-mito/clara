# Types
texto = str
real = float

# Functions
booleano = bool
mapa = map

def mostra(msg):
    if isinstance(msg, bool):
        if msg: print "verdadeiro"
        else: print "falso"
    elif isinstance(msg, float):
    	print str(msg).replace('.', ',')
    else: print msg

def tamanho(*args):
    if len(args) == 1:
        arg = args[0]
        if isinstance(arg, int) or isinstance(arg, float):
            return abs(x)
        else: return len(arg)
    else: return len(args)

def procura(string, sub):
    return string.find(sub)

def separa(str, separator):
    return str.split(separator)

def junta(iterable, string):
    return string.join(iterable)

def substitui(string, old, new):
    return string.replace(old, new)
