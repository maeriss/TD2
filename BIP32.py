import hashlib
import ecpy
from ecpy.curves import Curve,Point

def keyStretching(mnemonic, passphrase = ""):
    mnemonic = mnemonic.encode('utf-8')
    salt = "mnemonic" + passphrase
    salt = salt.encode('utf-8')
    key = hashlib.pbkdf2_hmac('sha512', mnemonic, salt, 2048).hex()
    return key

def compressPubkey(public_key):
    x=public_key.x
    y=public_key.y
    if y>0:
        prefix="02"
    else:
        prefix="03"
    return prefix+hex(x)[2:]

def generatePublickey(private_key):
    cv = Curve.get_curve('secp256k1')
    #valeur génératrice définie dans secp256k1
    g="79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8"
    G=Point(int(g[:64],base=16),int(g[64:],base=16),cv)
    public_key=int(private_key,base=16)*G #opération mulitipliée sur l'objet Point d'une courbe elliptique
    compressed_public_key=compressPubkey(public_key)
    return compressed_public_key
    

if __name__ == "__main__":
    mnemonic = input("Veuillez saisir votre mnémonique : ")
    passphrase = input("(OPTIONNEL) Votre phrase secrète : ")
    key = keyStretching(mnemonic, passphrase)
    print(key)
    hash_key = hashlib.sha512(key.encode()).hexdigest()
    n = int(len(hash_key)/2)
    master_private_key = hash_key[0:n]
    master_chain_code = hash_key[n:]
    public_key=generatePublickey(master_private_key)
    print(len(master_private_key))
    print(public_key)
    print(len(public_key))
    
