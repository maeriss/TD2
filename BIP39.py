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


#vérifie qu'une seed importée est valide ou non
def checkSeed(seed):
    #sépare les mots de la seed et les stocke dans une liste
    seed = seed.split()

    #stockage de la liste des mots dans un tableau
    with open("wordlist.txt", "r") as f:
        wordlist = [w.strip() for w in f.readlines()]

    #récupère l'index de chaque mot dans la wordlist et les stocke
    indexes = []
    for word in seed:
        if not word in wordlist:
            print(f"{word} n'est pas dans la liste")
            return False
        indexes.append(wordlist.index(word))

    #convertit les index en binaire (12 blocs de 11-bits)
    segments = []
    for index in indexes:
        segments.append(bin(index)[2:].zfill(11))


    #concatène tous les blocs de 11-bits
    concatenation = ''
    for s in segments :
        concatenation += s

    #séparation de l'entropie et du checksum
    entropie = concatenation[0:-4]
    cs = concatenation[-4:]

    #hache l'entropie avec sha256 pour récupérer le checksum théorique
    ent = hex(int(entropie, 2))[2:].zfill(32)
    theoric_checksum = checksum(ent)

    #regarde si le checksum de la seed et celui théorique sont les mêmes
    return cs==theoric_checksum



if __name__ == "__main__":
    print("Que voulez-vous faire ?")
    option = input('1 Créer une seed en mnémonique\n2 importer une seed\n')

    if option == '1':
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

    elif option == '2':
        #demande à l'utilisateur la seed qu'il veut importer et vérifier
        seed_import = input("Veuillez rentrer votre seed (12 mots séparés par un espace) : ")
        #check la seed
        validSeed = checkSeed(seed_import)
        if validSeed:
            print("Votre seed mnémonic est valide")
        else:
            print("Votre seed mnémonic n'est pas valide")
