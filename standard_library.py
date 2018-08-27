#import __builtin__

texto = str
real = float

def mostra(msg):
    if isinstance(msg, bool):
        if msg: print "verdadeiro"
        else: print "falso"
    elif isinstance(msg, float):
    	print str(msg).replace('.', ',')
    else: print msg