import secrets
import hashlib


def entropy(nbBits):
    n = 0
    while(n != 128):
        a = secrets.randbits(nbBits)
        c = "{0:b}".format(a)
        n = len(c)
    return c

a = entropy(128)

def checksum(entropie):
    #hache l'entropie avec sha256
    m = hashlib.sha256(entropie.encode()).hexdigest()
    #convertit en bits (mais g est un string)
    g = "{0:8b}".format(int(m,16))

    #vérifie que g fait bien 256 bits, sinon on rajoute autant de 0 que nécessaire devant
    if len(g) != 256:
        g = g.zfill(256)

    #récupère les 4 premiers bits dans g
    g = g[0:4]
    return g

b = checksum(a)

def concatenation(entropie,cs):
    seed = entropie + cs
    return seed

seed = concatenation(a,b)
print("seed : ", seed)

def split(graine):
    i=0
    segments = []
    for i in range(12):
        s = graine[i+10*i:i+10*(i+1)+1]
        segments.append(s)
    return segments

segments = split(seed)
print(segments)

for s in segments :
    print(int(s,2))



def words(segments):
    with open("wordlist.txt", "r") as f:
        wordlist = [w.strip() for w in f.readlines()]
    mnemonic = []
    for s in segments:
        index = int(s,2)
        mnemonic.append(wordlist[index])
    return mnemonic

print(words(segments))
