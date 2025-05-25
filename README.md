# 2024_2025__p04_projet2_g11 
Louise Christophe, Eudocie de Khovrine, Marine Fraboulet

## Tetris
Jeu ayant pour objectif de remplir des lignes; des formes géométiques descendent et le joueur doit les placer de façon à remplir l'espace le plus efficassement possible.
Plus le joueur rempli des lignes, plus il gagne des points.


### Description  
Ce projet propose une implémentation du jeu Tetris, accompagnée d'une IA qui s'entraîne pour améliorer son efficacité dans le placement des pièces.

Idée Deep Learning :
L’IA analyse les décisions prises lors de multiples parties pour apprendre à choisir les placements optimaux. Elle attribue des coefficients aux actions (rotation, position) en fonction du résultat obtenu (lignes complétées, espace libre, etc.).


### Structure du Projet
**tetris_ia.py** : lancement du jeu (ia)   
**tetris_j.py** : lancement du jeu (joueur)    
**utils.py** : gestion du json    
**tools.py** : fonction boutton    
**menu.py** : lancement du menu permettant de choisir le mode de jeu   
**bordures.json** : dictionnaire permettant de stocker les entrainements de l'ia  
**pieces.py** : éfinition des pièces, rotations et couleurs   


### Fonctionnalités
- Mode joueur humain 
- Mode IA 
- Système de score 
- Affichage coloré des pièces 
- Détection de lignes complètes et suppression 
- Mouvements et rotations des pièces 
- Entraînement et analyse de l’IA 

### Prérequis
Python 3.x


### Installation
1. Clonez le repository :   
```
git clone https://github.com/Eudo08/2024_2025_projet3_gp11_frab_chris_khov_belhad  
cd 2024_2025_projet3_gp11_frab_chris_khov_belhad
```
2. Assurez-vous que Python est installé. Vous pouvez le télécharger depuis [python.org](python.org).


### Utilisation
1. Lancez le script :  
```
python menu.py
```


### Modules et fonctions 
- #### Initialisation de base : fixation des variables comme taille de la fenêtre, les couleurs disponibles, et pour l'IA les variables alpha, gamma et epsilon de la Q_table 
- #### initialisation de la grille : création et dessin d'une grille
- #### affichage : affichage des pièces fixées, des carreaux dans le grille, etc  
- #### paramètres et fonctions d'aide : fonctions secondaires utiles pour les boucles principales. Cela peut être des fonctions de calcul, de vérification des collisons, etc
- #### boucle principale du jeu : boucle qui fait tourner le jeu et appelle les fonction secondaires et d'affichage. Dans l'IA, il y a une 2ème boucle, qui recommence une partie à chaque fin de jeu
- #### game over (uniquement mode joueur) : affichage et gestion d'une fin de partie


### Contribution

**[Louise Christophe](https://github.com/louisechristophe), [Eudocie de Khovrine](https://github.com/Eudo08), [Marine Fraboulet](https://github.com/MAMARINEEE)**, [WaelBelhaddad](https://github.com/WaelBELHADDAD) : Développement et ajout des fonctionnalités, des validations et des conversions entre bases, ainsi que l'amélioration de la structure générale.  
**ChatGPT** : Assistance pour les corrections de code et structuration du README.

### Licence
Ce projet est sous licence MIT.


