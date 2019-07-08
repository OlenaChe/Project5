Le programme Pur Beurre est destiné à chercher des substituts plus sains 
aux produits réguliers et à créer une liste des aliments sains 
selon le choix d’utilisateur.

Pour démarrer le programme l'utilisateur doit :
- installer MySQL,
- renommer un fichier "template.txt" en "private.py",
- remplacer le texte entre guillemets par les valeurs pertinentes 
  (HOST, USER, PASSWORD),
- lancer un fichier "pb_app.py" dans le Terminal.

Après le démarrage du programme l’utilisateur voit les instructions étape par étape.

Tout d’abord, l’utilisateur doit choisir une de deux options :
- Si vous utilisez l'application 'Pur Beurre' la première fois tapez '0'
(Dans ce cas, la base de données sera mise à jour)
- Sinon, tapez '1'
(L’utilisateur continue de compléter sa liste des produits sains)

Sur l’étape suivant le programme propose trois options :
1 - Quel aliment souhaitez-vous remplacer ? (L'utilisateur doit appuyer le chiffre « 1 »)
2 - Retrouver mes aliments substitués (L'utilisateur doit appuyer le chiffre « 2 »)
Q - Quitter - (L'utilisateur doit appuyer un lettre « Q »)

Option 1 (l’utilisateur tape « 1 ») :

1.1 L’utilisateur sélectionne la catégorie du produit de la liste 
en entrant un chiffre qui corresponde à cette catégorie + « entrée ».

1.2 L’utilisateur sélectionne le produit de la liste des produits de cette catégorie 
en entrant le chiffre qui corresponde à ce produit + « entrée ».

1.3 Le programme propose des substituts avec ses nutri-scores. 
L'utilisateur choix un de ces aliments en entrant le chiffre qui corresponde à ce produit + « entrée ».

1.4 Le programme affiche le nom du produit choisi, sa description, 
un lien vers la page d'Open Food Facts concernant 
cet aliment, son nutri-score, sa catégorie, et des magasins où on peut l'acheter.

1.5 Le programme propose à enregistrer le résultat de la recherche. 
L’utilisateur appuie « Y » s’il veut enregistrer le résultat, sinon il doit appuyer « N ».

1.6 Le programme relance l'étape 2 en proposant à l'utilisateur à choisir une de trois options.

Option 2 (l’utilisateur tape « 2 »)
 
2.1 Le programme affiche la liste des produits enregistrés

2.2 Le programme relance l'étape 2 en proposant à l'utilisateur à choisir une de trois options.

Option 3 (l’utilisateur tape « 3 ») 
Le programme se termine. 

Fonctionnalités :
Pour réaliser les fonctionnalités du programme on a créé les classes suivantes :
1) class Data_OFF pour récupérer les informations d’Open Food Facts en utilisant le library request
2) class Data_PB pour créer notre base de donné avec MySql
3) classe Display_data pour réaliser l’interaction de l’utilisateur avec la BdD
4) classe Saved_data pour afficher les résultats de requête.