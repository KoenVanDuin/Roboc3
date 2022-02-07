# -*-coding:Latin-1 -*
"""
Avec ce module on lit des fichiers pour en faire des cartes.
"""
import af
from carte import *
from case import *
#from time import sleep
from pointsCardinaux import haut, large
from carte import Y
import os

os.chdir("LesCartes")
af.afInfo = False

##os.chdir("C:\\Users\\Koen\\Desktop\\Python3map\\Roboc3Final\\LesCartes")

def lisCarte(nomFichier):
    """
    Avec cette fonction un lit des fichiers contenants des cartes.
    On renvoie des objet du type "carte".
    Il est à noter que cette fonction laisse de côté tout ce qu'elle
    ne peut pas traiter, et tout ce qui sort du cadre des dimensions
    'large x haut'.
    """
    with open( nomFichier, 'r') as fichier:
        grille0 = {}
        for y in range(haut):
            ligne = fichier.readline()
            diff = len(ligne) - large - 1
            if diff > 0:
                af.info("Attention!")
                message = "On perd {} signes à ligne {}."
                af.info(message.format(diff,y+1))
            for x in range(len(ligne)):
                grille0[x,Y(y)] = ligne[x]
    #af.info("Nous avons récupéré et découpé le contenu du fichier.")
    #af.info("Maintenant il s'agit de le traiter.")
    grille = {}
    xyRobot = (0,0)
    for clef in grille0.keys():
        for case in cases:
            if grille0[clef].lower() in case.signes:
                grille[clef] = case
        if grille0[clef].lower() == "x":
            xyRobot = clef
    #af.info("La grille a été remplie.")
    laby = Carte(grille,xyRobot) # on crée la carte.
    return laby

def lisTout():
    """
    Cette fonction lit tout dans le répertoire lesCartes.
    Elle renvoie un dictionnaire de cartes:
    """
    dic = {}
    liste = os.listdir(".") # Les noms des cartes à lire.
    for nomCarte in liste:
        if nomCarte != "fichier.txt":
        # fichier n'est pas une carte à lire!
        # On y enregistre des jeux inachevés.
            dic[nomCarte] = lisCarte(nomCarte)
    return dic

if __name__ == "__main__":
    print("Il n'y a pas eu d'erreur en lançant ce fichier.")
