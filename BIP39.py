import secrets
import hashlib
from binascii import unhexlify


#entropie aléatoire avec la librairie secrets, retournée en hexadecimal
def entropie():
    ent = secrets.token_hex(16)
    return ent


#conversion d'un hexadecimal en binaire (zfill rajoute des 0 devant si besoin en fonction de nbBits)
def hex_to_bin(nbHex, nbBits):
    nbBin = bin(int(nbHex,16))[2:].zfill(nbBits)
    return nbBin


def checksum(ent):
    #hacher l'entropie avec sha256
    entropie = unhexlify(ent)
    hache = hashlib.sha256(entropie).hexdigest()

    #convertit la sortie du hash en binaire
    hacheBin = hex_to_bin(hache,256)

    #récupère les 4 premiers bits du hash : c'est le checksum
    hacheBin = hacheBin[0:4]

    return hacheBin


#concatène l'entropie et le checksum (en binaire)
def concatenation(ent, checksum):
    #convertit l'entropie en binaire
    entropie = hex_to_bin(ent,128)
    #concatène
    seed = entropie + checksum
    return seed


#séparation des 132 bits en 12 segments de 11 bits
def split(seed):
    i=0
    segments = []
    for i in range(12):
        s = seed[i+10*i:i+10*(i+1)+1]
        segments.append(s)
    return segments


#récupération des mots correspondant à chaque bloc de 11 bits
def words(segments):
    #stockage de la liste des mots dans un tableau
    with open("wordlist.txt", "r") as f:
        wordlist = [w.strip() for w in f.readlines()]

    mnemonic = []
    for s in segments:
        #convertit chaque bloc en int
        index = int(s,2)
        #récupère le mot dans la wordlist avec l'index correspondant
        mnemonic.append(wordlist[index])
    return mnemonic


#pour un meilleur affichage du mnemonic
def affichage(tab):
    mnemonic = ''
    for elt in tab:
        mnemonic += elt
        mnemonic += ' '
    return mnemonic



if __name__ == "__main__":
    #entropie
    ent = entropie()
    #checksum à partir de l'entropie
    cs = checksum(ent)
    #concaténation de l'entropie et du checksum
    seed = concatenation(ent,cs)
    #séparation en blocs de 11 bits
    segments = split(seed)
    #récupération des mots et affichage
    mnemonic_tab = words(segments)
    print(affichage(mnemonic_tab))