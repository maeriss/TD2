# Avant le lancement

Le fichier "wordlist.txt" doit impérativement se trouver dans le même dossier que le fichier "BIP39.py" pour que ce dernier fonctionne.

## BIP 39

Un menu est proposé au lancement :\
    1. "Créer une seed mnémonique". L'utilisateur n'a rien à faire de particulier, la seed sera générée toute seule\
    2. "Importer une seed". L'utilisateur devra rentrer dans la console le mnémonic qu'il souhaite vérifier, sous la forme des 12 mots séparés par un espace. À partir de ce mnémonique, l'entropie est retrouvée te le checksum recalculé. On vérifie ensuite si ce checksum recalculé correspond bien à celui donné par l'utilisateur à travers le mnémonic.



## BIP 32

Avant de lancer le BIP32, assurez vous d'avoir la librairie ECPy, sinon l'installer (pip install ECPy).\

Lorsqu'on vous demande d'entrer votre mnémonic, celui-ci n'est pas vérifié. Il faut le faire au préalable à l'aide du BIP39 (option 2 : "importer une seed").
Il vous est proposé de rentrer une phrase secrète s'ajoutant au salt au moment de la génération de la root seed. Cette phrase secrète peut contenir n'importe quoi et est optionnelle (vous pouvez donc simplement appuyer sur entrée si vous ne souhaitez pas en ajouter)
