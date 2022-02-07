# -*-coding:Latin-1 -*
"""
Ce module contient pratiquement toutes les fonctions d'affichage
dont j'ai eu besoin.
"""

import random
from time import sleep

t = 0.02 # Le temps d'arrêt qu'on met dans "sleep".
# Pour le jeu t  = 1 convient le mieux.
# t = 0.5 va bien quand on veut déboguer.

afInfo = False # indique si info(...) doit s'afficher ou non.

def info(chaine):
    """
    Cette fonction se contente d'afficher 'INFO:     [argument]',
    lorsque l'affichage a été activé grâce à 'afficheInfo = True'.
    Elle sert à pallier à des dysfonctionnements d'autre fonctions.
    """
    if afInfo:
        print("INFO:     {}".format(chaine))

def ligne(car = "-",longueur = 50):
    """
    Cette fonction sert à afficher des lignes.
    Elle peut rendre l'affichage plus lisible.
    """
    lijn = "\n"
    for k in range(longueur):
        lijn += car
    lijn += "\n"
    print(lijn)

def titre(leTitre, car = "/",longueur = 50):
    """
    Une fonction qui affiche un titre assez joliment.
    """
    dePartEtDautre = "".center(longueur,car)
    print(dePartEtDautre)
    leTitre = "   {}   ".format(leTitre.upper())
    print(leTitre.center(longueur,car))
    print(dePartEtDautre + "\n")

def menu(liste, lengte = 25):
    """Permet d'affichier un petit menu."""
    print("".center(lengte,"_"))
    for elt in liste:
        print("|" + str(elt).center(lengte-2) + "|")
        sleep(t)
    print("".center(lengte,"-"))

def espace():
    """
    Cette fonction sert à laisser un peu d'espace vide
    entre les affichages.
    Comme ça le joueur voit le jeu uniquement au stade où il est.
    """
    espace = ""
    for k in range(50): 
        espace += "\n"
    print(espace)        

# Ici je ferai des visages pour la fonction qui va suivre.

# D'abord je fais "des morceaux de visages."
lYeux = [":","="]
bouches = {}
bouches[True] = [")","D","]","0"]
bouches[False] = ["<","(","[","0"]

# Ici j'assemble ces morceaux.
visages = {}
for gagne in [True, False]:
    visages[gagne] = []
    for yeux in lYeux:
        for bouche in bouches[gagne]:
            visages[gagne].append(yeux+bouche)

def jeuFini(gagne, nombre = 20, longueur = 8):
    """
    Une fonction d'affichage qu'on utilise à la fin du jeu.
    Si le joueur a gagné, on l'applaudit.
    Si le joueur a perdu, on le plaint.
    'gagne' est un booléen qui indique si le joueur gagne.
    """
    chaine = ""
    for ligne in range(nombre):
        if ligne % 2 == 0:
            chaine += "   "
        for compteur in range(longueur):
            chaine += random.choice(visages[gagne]) + "      "
        chaine += "\n\n"
    print(chaine)
    sleep(t)
    if gagne:
        print("Félicitations!")
    else:
        print("Quel dommage!")

def dis(chaine, *listeFormat):
    """
    Cette fonction affiche des chaines formatés.
    """
    aAfficher = chaine.format(*listeFormat)
    print(aAfficher)
    sleep(t)
    
if __name__ == "__main__":

    print("Il n'y pas eu d'erreurs en lançant ce fichier.")
    sleep(0.5)


    

	
