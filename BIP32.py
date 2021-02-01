import hashlib

#trouver la root seed
def keyStretching(mnemonic, passphrase = ""):
    mnemonic = mnemonic.encode('utf-8')
    #salt composé du mot constant "mnemonic" et d'une phrase secrete optionnelle
    salt = "mnemonic" + passphrase
    salt = salt.encode('utf-8')
    #dérivation de clé avec pbkdf2 sur 2048 itérations avec sha512
    key = hashlib.pbkdf2_hmac('sha512', mnemonic, salt, 2048).hex()
    return key



if __name__ == "__main__":
    #demande à l'utilisateur son mnémonique et une phrase secrète
    mnemonic = input("Veuillez saisir votre mnémonique : ")
    passphrase = input("(OPTIONNEL) Votre phrase secrète : ")
    key = keyStretching(mnemonic, passphrase)
    #hachage de la root seed avec sha512
    hash_key = hashlib.sha512(key.encode()).hexdigest()
    #séparation en 2 des 512 bits
    n = int(len(hash_key)/2)
    master_private_key = hash_key[0:n]
    master_chain_code = hash_key[n:]
    print(hash_key, master_private_key, master_chain_code)
