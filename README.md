# SE202 Dépôt Git

Bienvenue sur le gitLab de Erwan CHERIAUX !

# Step 1

Nous réalisons un compilateur écrit en Python3.4 pour du code Tiger ayant pour cible une architecture ARM.
La première étape consiste à ajouter les opérateurs binaires et de comparaisons dans la liste des tokens.
On réalise également des tests pour vérifier leurs bonnes implémentations: règle des priorités conformes.

De plus, on implémente la construction if/then/else.
Pour tester if/then/else entrez la commande:

./tiger.py -e -E"if 0 then 2 else 3"

La structure if/then/else fonctionne. Cependant, la composition if/then n'est pas géré.

L'étape 1 est validé après plusieurs tentative car le code est soumis a de nombreux tests unitaires lors du push sur le dépot git distant.

# Step 2

Il s'agit ici d'implémenter les déclaration de variables et de fonction, gérer le type INT, les commentaires et le moins unaire. Enfin, il faut veiller à ce que la sémentique soit réspecté tel que l'utilisation de variable déclaré en amont.
