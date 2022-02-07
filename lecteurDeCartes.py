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
    Il est � noter que cette fonction laisse de c�t� tout ce qu'elle
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
                message = "On perd {} signes � ligne {}."
                af.info(message.format(diff,y+1))
            for x in range(len(ligne)):
                grille0[x,Y(y)] = ligne[x]
    #af.info("Nous avons r�cup�r� et d�coup� le contenu du fichier.")
    #af.info("Maintenant il s'agit de le traiter.")
    grille = {}
    xyRobot = (0,0)
    for clef in grille0.keys():
        for case in cases:
            if grille0[clef].lower() in case.signes:
                grille[clef] = case
        if grille0[clef].lower() == "x":
            xyRobot = clef
    #af.info("La grille a �t� remplie.")
    laby = Carte(grille,xyRobot) # on cr�e la carte.
    return laby

def lisTout():
    """
    Cette fonction lit tout dans le r�pertoire lesCartes.
    Elle renvoie un dictionnaire de cartes:
    """
    dic = {}
    liste = os.listdir(".") # Les noms des cartes � lire.
    for nomCarte in liste:
        if nomCarte != "fichier.txt":
        # fichier n'est pas une carte � lire!
        # On y enregistre des jeux inachev�s.
            dic[nomCarte] = lisCarte(nomCarte)
    return dic

if __name__ == "__main__":
    print("Il n'y a pas eu d'erreur en lan�ant ce fichier.")
