# Types
texto = str
real = float
booleano = bool

# Functions
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
            return abs(arg)
        else: return len(arg)
    else: return len(args)

def procura(iterable, member):
    if isinstance(iterable, str):
        return iterable.find(member)
    else:
        return iterable.index(member)

def separa(string, separator):
    return string.split(separator)

def junta(iterable, string):
    return string.join(iterable)

def adiciona(iterable, element):
    iterable.append(element)

def substitui(string, old, new):
    return string.replace(old, new)
