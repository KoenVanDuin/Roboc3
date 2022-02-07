# -*-coding:Latin-1 -*
import re
import af
# La largeur et la hauteur de cartes.
# Il vaut mieux ne pas y toucher.
haut = 20 
large = 20
Max = max(large,haut)

af.afInfo = False

pCard = [] # On va y mettre les points cardinaux.
 
class PointC:
    """
    Les points cardinaux.
    Les seules instances sont N, S, E, O.
    """
    
    def __init__(self,nom,lettre,decale):
        self.nom = nom 
        self.lettre = lettre 
        self.decale = decale
        pCard.append(self)

    def __repr__(self):
        return self.lettre.upper()

# Les fonctions ci-dessous expliquent au python
# comment faire un pas dans un sens donné.
# Il serviront comme attributs aux points cardinaux.

def decaleNord(xyRobot):
    x,y = xyRobot
    return (x,y+1)

def decaleSud(xyRobot):
    x,y = xyRobot
    return (x,y-1)

def decaleOuest(xyRobot):
    x,y = xyRobot
    return (x-1,y)

def decaleEst(xyRobot):
    x,y = xyRobot
    return (x+1,y)

# Ici je crée tous les points cardinaux.
N = PointC("au nord","N",decaleNord)
S = PointC("au sud","S",decaleSud)
O = PointC("à l'ouest","O",decaleOuest)
E = PointC("à l'est","E",decaleEst)

pCardL = [pC.lettre.lower() for pC in pCard]

def saisiePermise(chaine):
    """
    Avec cette fonction on regarde si une saisie est traitable.
    C'est le cas si elle est de la forme N345453, par exemple.
    Les saisies 'Q' et 'H' sont aussi traitable.
    ATTENTION: Je n'utilise plus cette fonction !!
    """
    # Si la chaine ne comporte qu'une de ces lettres, on est tranquille.
    if chaine.lower() in pCardL + ['q','h']:
        return True
    # Si ce n'est pas le cas, et si len(chaine) = 0,1
    # La saisie n'est pas traitable.
    if len(chaine) < 2:
        return False
    pC = chaine[0]  # On découpe la saisie
    entier = chaine[1:]
    try: # Si on ne peut pas faire ces conversions la saisie est pourrie.
        entier = int(entier)
        pC = pC.lower()
    except ValueError:
        return False
    if pC not in pCardL:
        return False
    # Le premier caractère doit être un point cardinal.
    return True
    # Si toutes ces conditions sont remplies, la saisie est traitable.

# Le code qui suit vérifie si la saisie est bonne.

exDep = "^[neso][0-9]*$" # REGEX de déplacement.
exAct = "^[pm][neso]$" # REGEX d'action.
comDep = re.compile(exDep)
comAct = re.compile(exAct)

def saisiePermise(chaine):
    chaine = chaine.lower()
    if chaine in ["h","q"]:
        return True
    if comDep.search(chaine):
        return True
    if comAct.search(chaine):
        return True
    else:
        return False

if __name__ == "__main__":
    
    print("Ici j'essaie saisiePermise.\n\n")
    print("D'abord j'essaie les commandes de déplacement.")
    lijst = ["n","o","s","e","N","O1","H","H1","Q","Q5","S5","n99"]
    lijst += ["4N1","N23","O999","o","o15","schaap","n4n"]
    for elt in lijst:
        mot = "saisiePermise({}) = {}."
        print(mot.format(elt,saisiePermise(elt)))
        print("")
    print("\nEnsuite j'essaie les autres commandes.")
    print("Je commence par quelques unes devraient renvoyer True.\n")
    lijst = []
    lijsti = ["p","m","P","M"]
    lijstj = ["n","e","s","o","N","E","S","O"]
    for i in lijsti:
        for j in lijstj:
            lijst.append(i+j)
    for elt in lijst:
        mot = "saisiePermise({}) = {}."
        print(mot.format(elt,saisiePermise(elt)))
        print("")
    print("Ensuite quelques unes qui devraient renvoyer False.")
    lijst = ["aap","378","dd02","NN","OO","geen inspiratie meer"]
    for elt in lijst:
        mot = "saisiePermise({}) = {}."
        print(mot.format(elt,saisiePermise(elt)))
        print("")
    print("Fin des essais.")
# TODO: supprimer la vieille version de saisiePermise.
# TODO: remplacer la saisie par des fenêtres.

        
        
