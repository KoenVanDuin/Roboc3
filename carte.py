# -*-coding:Latin-1 -*
"""
Ce module contient la classe 'carte',
les méthodes pour travailler avec des cartes,
celles pour qui permettent au robot de se déplacer,
et celles qui font le lien entre la saisie du joueur
et le déplacement du robot. 
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
    Cette fonction est utilisé quand je joueur entre "H".
    Elle explique comment se déplacer sur la carte.
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
    print("Saisissez 'Q' pour arrêter le jeu.\n")
    sleep(3*t)

def Y(y):
    """
    Ceci est un petit changement de coordonnées.
    On en a besoin pour que l'affichage de la carte
    se fasse dans le bon sens.
    """
    return haut-1-y

class Carte:    
    """
    Cette classe modélise des cartes.
    Elle prend aussi en compte l'état du jeu,  c.-à-d
    le nombre de coups et l'endroit ou se trouve le robot.
    """

    def ajusteGrille(self):
        """
        Ceci est une fonction qui "ajuste" des grilles:
        Elle prend en argument un dictionnaire.
        Elle en renvoie un autre qui est à même de servir comme carte.
        Elle a une certaine robustesse vis-à-vis des erreurs
        qu'il peut y avoir dans le dictionnaire entré.
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
            #af.info("On en crée une du coup")
            nouvelleGrille[large-1,haut-1] = sortie
        self.grille = nouvelleGrille
        
    def __init__(self,grille = {}, xyRobot = (0,0)):
        """
        On construit une carte à partir d'un dictionnaire.
        On le l'épure au moyen d'ajusteGrille.
        """
        self.grille = grille
        self.ajusteGrille()  # On "nettoie" le dictionnaire. 
        self.coups = 1 # le nombre de coups joués.
        # Pour gérer des bêtises de l'utilisateur:        
        if self[xyRobot] in [mur, puit]: 
            af.info("Attention!") 
            af.info("On libère la case d'où le joueur doit partir.")
        if self[xyRobot] == sortie:
            x,y = xyRobot
            xyRobot = (x+1,y)
        self[xyRobot] = dalle
        self.xyRobot = xyRobot 
        # Je sais que ce bidouillage est assez moche,
        # mais je tiens à pouvoir facilement modifier des cartes
        # sans trop m'inquiéter du fonctionnement du code.
        
    def __repr__(self):
        """Cette méthode "convertit" une carte en chaîne."""
        #af.info("On est dans le corps de __repr__")
        chaine = ""
        for k in range(large+1):
            chaine += "__" # La barrière au nord du dédale.
        chaine += "\n"
        for y in range(haut):
            chaine += "|" # La barrière à l'ouest du dédale.
            # On affiche une "bande" de la carte.
            for x in range(large): 
                if self.xyRobot == (x,Y(y)): 
                    chaine += robot
                if self.xyRobot != (x,Y(y)): 
                    chaine += self[x,Y(y)].symbole
            chaine += "|" # la barrière à l'est.
            # Ceci qui une espèce de tableau de bord.
            # Il sera affiché tout au long du jeu,
            # à droite de la carte.
            if Y(y) == 0:
                ajout = "\t Vous êtez le robot,'{}'."
                chaine += ajout.format(robot)
            if Y(y) == 1:
                ajout = "\t Filez vers la sortie! '{}' !!"
                chaine += ajout.format(sortie.symbole)
            if Y(y) == 2:
                messageCoups = "\t Vous jouez coup numéro {}."
                chaine += messageCoups.format(self.coups)
            if Y(y) == 3:
                chaine += "\t Entrez H pour avoir de l'aide."
            chaine += "\n"
        for k in range(large+1):
            chaine += "--" # la barrière au sud.
        return chaine
    
    def __getitem__(self,xy):
        """Avec cette méthode on récupère l'objet qui se trouve sur une case."""
        return self.grille[xy]

    def __setitem__(self,xy,valeur):
        """Avec cette méthode un change l'objet qui se trouve sur une case."""
        x,y = xy
        self.grille[(x,y)] = valeur

    def bouge(self,pC,distance):
        """
        Cette méthode travaille en coulisse quand le joueur joue un coup.
        Quand le robot doit faire plusieurs pas, il les fait un par un.
        Quand il rencontre une case autre que "dalle", une exception est levée.
        Celle-ci est attrapé et traité dans le fichier principal.
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
                        mot = "Vous êtes parvenu à la sortie!"
                        raise FinException(True,mot,True)
                    if self[xyN] == bar:
                        mot = "détruisons-la!"
                        raise ObsException(bar,mot,xyN)
                    self.xyRobot = xyN
                    print(self)
                    sleep(t*0.5)
                    af.espace()

    def agis(self,pC,act):
        """
        Grâce à cette méthode un joueur peut ménager une ouverture
        ou construire un mur.
        Si le robot ne peut pas faire ce qu'on lui demande,
        on lui interdit de le faire au moyen d'une exception.
        """
        # On récupère les coordonnées de la case à remplacer.
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
                # en dehors de la carte. Il faut lui interdire ça.
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
        Le jeu se déroule en appelant cette méthode jusqu'à la fin du jeu.
        Elle affiche la carte à chaque coup et demande des saisies.
        """
        # On sauvegarde le jeu au début de chaque coup. 
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
        # À la fin de cette boucle 'sens' contient une saisie valable.
        self.traiteSaisie(sens)
    
    def traiteSaisie(self,chaine):
        """
        Si la saisie est traitable, on la traite avec cette fonction.
        Quand la saisie sert à faire bouger le robot, on applique bouge.
        Quand le joueur veut quitter le jeu, ou a besoin d'explications,
        on traite la saisie sans passer par cette méthode.
        """
        chaine = chaine.lower()
        if chaine == "h": # Quand l'utilisateur a besoin d'aide,
            explique2()   # on affiche des explications.
            return
        if chaine == "q": # Dans ce cas-ci le jeu s'interrompt.
            mot = "Vous arrêtez de jouer!"
            raise FinException(False,mot,False)
        if chaine in pCardL:
            chaine = chaine + "1"
        # Maintenant on n'a plus qu'à traiter
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
        Cette fonction prend en entrée une carte.
        Grâce a cette fonction, le joueur joue jusqu'à ce qu'il
        tombe dans un puit, atteigne une sortie, ou entre "Q".
        """
        while True:
            try: # Le robot essaie d'obéir au joueur...
                self.joueUnCoup()
            except ObsException as e:
                print(self)
                print("On se heurte à {}".format(e.objet.desc))
                sleep(t)
                print(e.mot)
                if e.objet == bar: # On détruit la barricade.
                    self[e.xyObs] = dalle 
                sleep(t)
            except AgisException as e:
                af.info("On attrape une AgisException.")
                mot = "L'ordre reçu n'a pas été appliqué:\n"
                mot = "On ne peut pas remplacer {} par {} !"
                # Améliorer l'affichage. Il faut mettre les mots,
                # pas les symboles.
                print(mot.format(e.caseAn,e.caseNou))
            except FinException as e:
                if e.supp: # Quand le joueur gagne ou perd...
                    os.remove("fichier.txt")  
                af.jeuFini(e.gagne)
                sleep(t)
                print(e.mot)
                sleep(t)
                print("Le jeu est terminé.")
                break                 
        # Ce bout du code représente la fin du jeu.
        # On attend que joueur soit prêt à rejouer.
        af.ligne()
        input("Appuyez sur la touche ENTREE pour rejouer au Roboc.\n")
        af.espace()
        sleep(t)

if __name__ == "__main__":
    print("Il n'y a pas eu d'erreur en lançant 'carte'.")
    af.info("La fonction 'info' est activée.")

# TODO: éviter qu'une AgisException soit levée quand
#       rien ne nous empêche d'agir.
