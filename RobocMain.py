# -*-coding:Latin-1 -*
"""L'ex�cutable du jeu Roboc."""
import af
from pointsCardinaux import *
from carte import *
from case import *
from lecteurDeCartes import lisTout

af.afInfo = False
t = af.t

eltChoisi = ""

def comp(chaine1,chaine2):
    """
    Ceci est une fonction qui compare deux chaines.
    elle renvoie True si les chaines sont �gales
    � la casse et � l'espacement pr�s.
    """
    # TODO: � am�liorer avec une REGEX ou 
    #       � remplacer par un cadre.
    chaine1 = chaine1.lower().replace(" ","")
    af.info("chaine1  = {}".format(chaine1))
    chaine2 = chaine2.lower().replace(" ","")
    af.info("chaine2  = {}".format(chaine2))
    return chaine1 == chaine2

def dansListe(chaine, liste):
    """
    Avec cette fonction on regarde si une chaine
    est dans une liste � la casse et � l'espacement pr�s.
    """
    # TODO: Remplacer de la m�me fa�on que "comp".
    global eltChoisi
    for elt in liste:
        if comp(chaine,elt):
            eltChoisi = elt
            return True
    return False

def demarreJeu():
    """
    Cette fonction permettra de d�marrer le jeu.
    Elle lit les fichiers contenant les cartes.
    Ensuite elle demande au joueur de choisir une carte.
    La relecture r�currente des cartes permet de changer
    ces cartes pendant le je m�me.
    Les changements sont pris en compte au moment o� une
    nouvelle partie commence.
    """
    # Remplacer la saisie par une fen�tre avec deux boutons.
    dicDesCartes = lisTout()
    nCartes = len(dicDesCartes)
    if os.path.isfile("fichier.txt"):
        print("\nNous avons sauvegard� un jeu inachev�.")
        sleep(t)
        print("Si vous appuyez sur la touche ENTREE le jeu reprend.")
        sleep(t)
        print("Un nouveau jeu commence si vous saisissez quelque chose.")
        sleep(t)
        choix = input("Merci de choisir maintenant. ")
        af.info("Le joueur a saisie quelque chose.")
        if choix == "": #Si le joueur appuie sur ENTREE...
            with open('fichier.txt', 'rb') as docu:
                mon_depickler = pickle.Unpickler(docu)
                doolhof = mon_depickler.load()
            sleep(t)
            print("\nVous choisissez de reprendre le jeu inachev�.")
            sleep(t)
            print("Allons-y!")
            sleep(t)
            return doolhof   
    
    chaine = "Maintenant vous devez choisir l'une des {} cartes:"    
    print(chaine.format(nCartes))
    sleep(t)
    clefs = dicDesCartes.keys() # des cartes lues au d�but.
    # J'enl�ve ".txt" ici.
    cles = [nom[:len(nom)-4] for nom in clefs]
    af.menu(cles)
    global eltChoisi
    eltSaisi = ""
    while not dansListe(eltSaisi,cles):
        eltSaisi = input("Quel sera votre choix ? ")
    sleep(t)
    print("")    
    reponse = "Votre choix s'est port� sur {}."
    print(reponse.format(eltChoisi))
    sleep(t)
    print("Allons-y!\n")
    sleep(t) # On renvoie la carte choisie.
    choix = eltChoisi + ".txt"
    eltChoisi = ""
    return dicDesCartes[choix]

def explique1():
    """
    La fontion qu'on appelle juste apr�s l'affichage du titre.
    Elle sert � expliquer et � pr�senter le jeu.
    """
    af.dis("Bienvenu � Roboc, le meilleur jeu du monde!")
    af.ligne()
    sleep(t)
    af.dis("Vous dirigez un robot {} � travers un d�dale.",robot)
    phrase = "Le but du jeu est d'atteindre la sortie {}"
    af.dis(phrase,sortie.symbole)
    phrase = "Les portes {} peuvent �tre franchies."
    af.dis(phrase,porte.symbole)
    phrase = "Les barrricades {} peuvent �tre d�truites."
    af.dis(phrase,bar.symbole)
    
    phrase = "Evitez les murs {} et les puits {} cependant!"
    af.dis(phrase,mur.symbole,puit.symbole)
    af.dis("Quand vous tombez dans un puit vous n'en ressortirez jamais...")
    return

af.titre("Roboc")
explique1() # On explique au joueur le but du jeu. 

while True:
    print("")
    af.titre("Roboc")
    sleep(t)
    laby = demarreJeu()
    laby.joue()
