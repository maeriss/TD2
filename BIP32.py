import hashlib
import pbkdf2


def keyStretching(mnemonic, passphrase = ""):
    mnemonic = mnemonic.encode('utf-8')
    salt = "mnemonic" + passphrase
    salt = salt.encode('utf-8')
    key = hashlib.pbkdf2_hmac('sha512', mnemonic, salt, 2048).hex()
    return key



if __name__ == "__main__":
    mnemonic = input("Veuillez saisir votre mnémonique : ")
    passphrase = input("(OPTIONNEL) Votre phrase secrète : ")
    key = keyStretching(mnemonic, passphrase)
    hash_key = hashlib.sha512(key.encode()).hexdigest()
    n = int(len(hash_key)/2)
    master_private_key = hash_key[0:n]
    master_chain_code = hash_key[n:]
    print(hash_key, master_private_key, master_chain_code)
