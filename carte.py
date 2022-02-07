# -*-coding:Latin-1 -*
"""
Ce module contient la classe 'carte',
les m�thodes pour travailler avec des cartes,
celles pour qui permettent au robot de se d�placer,
et celles qui font le lien entre la saisie du joueur
et le d�placement du robot. 
"""
import af # le module contenant les fonctions d'affichage.
from pointsCardinaux import *
from case import *
from time import sleep
import pickle
import os

af.afInfo = True
t = af.t

def explique2():
    """
    Cette fonction est utilis� quand je joueur entre "H".
    Elle explique comment se d�placer sur la carte.
    """
    sleep(t)
    print("")
    af.dis("Vous avez saisi 'H', revoici donc l'explication du jeu: ")
    instr = "S5aisissez '{}' pour aller {}."
    for pC in pCard:
        af.dis(instr,pC.lettre,pC.nom)
    af.dis("Si vous saisissez une direction suivi d'un nombre,")
    af.dis("vous faites d'un coup autant de pas dans ce sens.")
    af.dis("Par exemple, en entrant N3 vous faites trois pas vers le nord.")
    print("Saisissez 'Q' pour arr�ter le jeu.\n")
    sleep(3*t)

def Y(y):
    """
    Ceci est un petit changement de coordonn�es.
    On en a besoin pour que l'affichage de la carte
    se fasse dans le bon sens.
    """
    return haut-1-y

class Carte:    
    """
    Cette classe mod�lise des cartes.
    Elle prend aussi en compte l'�tat du jeu,  c.-�-d
    le nombre de coups et l'endroit ou se trouve le robot.
    """

    def ajusteGrille(self):
        """
        Ceci est une fonction qui "ajuste" des grilles:
        Elle prend en argument un dictionnaire.
        Elle en renvoie un autre qui est � m�me de servir comme carte.
        Elle a une certaine robustesse vis-�-vis des erreurs
        qu'il peut y avoir dans le dictionnaire entr�.
        """
        af.info("On est dans le corps d'ajusteGrille.")
        nouvelleGrille = {}
        for y in range(haut):
            for x in range(large):
                if (x,y) in self.grille.keys():
                    if isinstance(self[x,y],Case):
                        nouvelleGrille[x,y] = self[x,y]
                    if not isinstance(self[x,y],Case):
                        if self[x,y] != "X":
                            af.info("Attention! Il y a une case mal remplie!")
                        nouvelleGrille[x,y] = dalle    
                if (x,y) not in self.grille.keys():
                    #af.info("On remplit une case vide.")
                    nouvelleGrille[x,y] = dalle
        if sortie not in nouvelleGrille.values():
            #af.info("Il n'y a pas de sortie sur la carte!")
            #af.info("On en cr�e une du coup")
            nouvelleGrille[large-1,haut-1] = sortie
        self.grille = nouvelleGrille
        
    def __init__(self,grille = {}, xyRobot = (0,0)):
        """
        On construit une carte � partir d'un dictionnaire.
        On le l'�pure au moyen d'ajusteGrille.
        """
        self.grille = grille
        self.ajusteGrille()  # On "nettoie" le dictionnaire. 
        self.coups = 1 # le nombre de coups jou�s.
        # Pour g�rer des b�tises de l'utilisateur:        
        if self[xyRobot] in [mur, puit]: 
            af.info("Attention!") 
            af.info("On lib�re la case d'o� le joueur doit partir.")
        if self[xyRobot] == sortie:
            x,y = xyRobot
            xyRobot = (x+1,y)
        self[xyRobot] = dalle
        self.xyRobot = xyRobot 
        # Je sais que ce bidouillage est assez moche,
        # mais je tiens � pouvoir facilement modifier des cartes
        # sans trop m'inqui�ter du fonctionnement du code.
        
    def __repr__(self):
        """Cette m�thode "convertit" une carte en cha�ne."""
        #af.info("On est dans le corps de __repr__")
        chaine = ""
        for k in range(large+1):
            chaine += "__" # La barri�re au nord du d�dale.
        chaine += "\n"
        for y in range(haut):
            chaine += "|" # La barri�re � l'ouest du d�dale.
            # On affiche une "bande" de la carte.
            for x in range(large): 
                if self.xyRobot == (x,Y(y)): 
                    chaine += robot
                if self.xyRobot != (x,Y(y)): 
                    chaine += self[x,Y(y)].symbole
            chaine += "|" # la barri�re � l'est.
            # Ceci qui une esp�ce de tableau de bord.
            # Il sera affich� tout au long du jeu,
            # � droite de la carte.
            if Y(y) == 0:
                ajout = "\t Vous �tez le robot,'{}'."
                chaine += ajout.format(robot)
            if Y(y) == 1:
                ajout = "\t Filez vers la sortie! '{}' !!"
                chaine += ajout.format(sortie.symbole)
            if Y(y) == 2:
                messageCoups = "\t Vous jouez coup num�ro {}."
                chaine += messageCoups.format(self.coups)
            if Y(y) == 3:
                chaine += "\t Entrez H pour avoir de l'aide."
            chaine += "\n"
        for k in range(large+1):
            chaine += "--" # la barri�re au sud.
        return chaine
    
    def __getitem__(self,xy):
        """Avec cette m�thode on r�cup�re l'objet qui se trouve sur une case."""
        return self.grille[xy]

    def __setitem__(self,xy,valeur):
        """Avec cette m�thode un change l'objet qui se trouve sur une case."""
        x,y = xy
        self.grille[(x,y)] = valeur

    def bouge(self,pC,distance):
        """
        Cette m�thode travaille en coulisse quand le joueur joue un coup.
        Quand le robot doit faire plusieurs pas, il les fait un par un.
        Quand il rencontre une case autre que "dalle", une exception est lev�e.
        Celle-ci est attrap� et trait� dans le fichier principal.
        """
        for wS in pCard:
            if pC == wS.lettre.lower():
                for k in range(distance):
                    xyN = wS.decale(self.xyRobot) #xyN = xyNouveau
                    mot = "On ne peut pas aller plus loin."
                    exc = ObsException(mur,mot)
                    if xyN not in self.grille.keys():
                        raise exc
                    if self[xyN] == mur:
                        raise exc
                    if self[xyN] == puit:
                        mot = "Vous tombez dans un puit!"
                        raise FinException(False,mot,True)
                    if self[xyN] == sortie:
                        mot = "Vous �tes parvenu � la sortie!"
                        raise FinException(True,mot,True)
                    if self[xyN] == bar:
                        mot = "d�truisons-la!"
                        raise ObsException(bar,mot,xyN)
                    self.xyRobot = xyN
                    print(self)
                    sleep(t*0.5)
                    af.espace()

    def agis(self,pC,act):
        """
        Gr�ce � cette m�thode un joueur peut m�nager une ouverture
        ou construire un mur.
        Si le robot ne peut pas faire ce qu'on lui demande,
        on lui interdit de le faire au moyen d'une exception.
        """
        # On r�cup�re les coordonn�es de la case � remplacer.
        x,y = pC.decale(self.xyRobot)
        if act == "p": #Si le joueur veut percer une porte...
            try:
                if self[x,y] == mur: # et s'il y a un mur
                    af.info("On perce une porte !")
                    self[x,y] = porte
                else: # Sinon, on interdit de percer une porte.
                    raise AgisException(self[x,y].desc,porte.desc)
            except KeyError:
                # Dans ce cas le joeur essaie modifier quelque chose
                # en dehors de la carte. Il faut lui interdire �a.
                raise AgisException("un paroi",descNou)
        elif act == "m":
            try: # Les commentaires ci-dessus s'appliquent.
                if self[x,y] == porte: 
                    af.info("On reconstruit un mur !")
                    self[x,y] = mur
                else:
                    raise AgisException(self[x,y].desc,mur.desc)
            except KeyError:
                raise AgisException("un paroi",descNou)
        # TODO: Remplacer les 'try' par des 'if not in keys()'?
        
    def joueUnCoup(self):
        """
        Le jeu se d�roule en appelant cette m�thode jusqu'� la fin du jeu.
        Elle affiche la carte � chaque coup et demande des saisies.
        """
        # On sauvegarde le jeu au d�but de chaque coup. 
        with open('fichier.txt', 'wb') as docu:
            mon_pickler = pickle.Pickler(docu)
            mon_pickler.dump(self)
        af.espace()
        print(self)
        sens = "" # La variable qui va contenir la saisie du joueur.
        while not saisiePermise(sens):
            sens = input("Dans quel sens veux-tu envoyer le robot?")
            sens = sens.upper()
        af.espace()
        # � la fin de cette boucle 'sens' contient une saisie valable.
        self.traiteSaisie(sens)
    
    def traiteSaisie(self,chaine):
        """
        Si la saisie est traitable, on la traite avec cette fonction.
        Quand la saisie sert � faire bouger le robot, on applique bouge.
        Quand le joueur veut quitter le jeu, ou a besoin d'explications,
        on traite la saisie sans passer par cette m�thode.
        """
        chaine = chaine.lower()
        if chaine == "h": # Quand l'utilisateur a besoin d'aide,
            explique2()   # on affiche des explications.
            return
        if chaine == "q": # Dans ce cas-ci le jeu s'interrompt.
            mot = "Vous arr�tez de jouer!"
            raise FinException(False,mot,False)
        if chaine in pCardL:
            chaine = chaine + "1"
        # Maintenant on n'a plus qu'� traiter
        # les saisies de la forme "N12."
        # et celles de la forme "pE"
        # On coupe la saisie en deux et on applique 'bouge.'
        if chaine[0] in ["p","m"]:
            # Le robot doir agir, me semble-t-il.
            act = chaine[0]
            pC = chaine[1]
            self.agis(eval(pC.upper()),act)
            self.coups += 1
        if chaine[0] in ["n","e","s","o"]:            
            pC = chaine[0]
            distance = int(chaine[1:])
            self.bouge(pC,distance)
            self.coups += 1

    def joue(self):
        """
        Cette fonction prend en entr�e une carte.
        Gr�ce a cette fonction, le joueur joue jusqu'� ce qu'il
        tombe dans un puit, atteigne une sortie, ou entre "Q".
        """
        while True:
            try: # Le robot essaie d'ob�ir au joueur...
                self.joueUnCoup()
            except ObsException as e:
                print(self)
                print("On se heurte � {}".format(e.objet.desc))
                sleep(t)
                print(e.mot)
                if e.objet == bar: # On d�truit la barricade.
                    self[e.xyObs] = dalle 
                sleep(t)
            except AgisException as e:
                af.info("On attrape une AgisException.")
                mot = "L'ordre re�u n'a pas �t� appliqu�:\n"
                mot = "On ne peut pas remplacer {} par {} !"
                # Am�liorer l'affichage. Il faut mettre les mots,
                # pas les symboles.
                print(mot.format(e.caseAn,e.caseNou))
            except FinException as e:
                if e.supp: # Quand le joueur gagne ou perd...
                    os.remove("fichier.txt")  
                af.jeuFini(e.gagne)
                sleep(t)
                print(e.mot)
                sleep(t)
                print("Le jeu est termin�.")
                break                 
        # Ce bout du code repr�sente la fin du jeu.
        # On attend que joueur soit pr�t � rejouer.
        af.ligne()
        input("Appuyez sur la touche ENTREE pour rejouer au Roboc.\n")
        af.espace()
        sleep(t)

if __name__ == "__main__":
    print("Il n'y a pas eu d'erreur en lan�ant 'carte'.")
    af.info("La fonction 'info' est activ�e.")

# TODO: �viter qu'une AgisException soit lev�e quand
#       rien ne nous emp�che d'agir.
