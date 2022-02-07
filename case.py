# -*-coding:Latin-1 -*
"""
Ce module contient la classe 'case' et les exceptions.
"""
import af

af.afInfo = False

cases = [] # On met toutes les cases dans une liste.
# Comme ça un peut parcourir les cases avec une boucle.

class Case:
    """
    Cettes classe représente un objets sur la carte.
    Elle n'a que quelques instances qu'on peut voir en dessous
    du corps de la classe.
    """
    
    def __init__(self,symbole,signe,desc):
        """
        Le constructeur des cases.
        'symbole' est le signe qu'on utilise
        pour afficher la case.
        'signes' est une liste de symbloles
        par lequel on peut représenter une case
        quand on fait une carte par le biais d'un fichier.
        Il y a aussi une description à afficher.
        """
        self.symbole = symbole
        signes = [signe,symbole[0],symbole[1]]
        signes = [s.lower() for s in signes]
        self.signes = signes
        self.desc = desc
        cases.append(self)
        # Je veux pouvoir utiliser le symbole d'affichage
        # quand je crée un fichier de carte.
        
        
    def __repr__(self):
        return self.symbole

    def __eq__(self,autre):
        return self.symbole == autre.symbole

# Toutes les instances.
mur = Case("##","o","un mur")
dalle = Case("  ","d","une dalle")
sortie = Case("||","u","une sortie")
puit = Case("()","p","un puit")
bar = Case("++","B","une barricade")
porte = Case("..","P","une porte")
# Robot n'est pas une case, dans ce code.
# J'ai décidé ici comment l'afficher:
robot = "XX"

# Voici toutes les exceptions que j'ai eu besoin de définir.

class ObsException(Exception):
    """
    Exception levée quand on trouve un objet sur le chemin
    qui fait s'arrêter le robot.
    """
    def __init__(self,objet=bar,mot="",xyObs=None):
        """
        Pour bien traiter l'exception, on a besoin de savoir
        devant quel objet le robot s'arrête, et où l'objet
        se trouve, quand il s'agit d'une barricade.
        """
        self.objet = objet
        self.mot = mot
        self.xyObs = xyObs

class FinException(Exception):
    """
    Exception levée quand le jeu doit se terminer.
    C'est le cas lorsque le joueur gagne, perd,
    ou choisit lui-même d'arrêter de jouer.
    """

    def __init__(self,gagne = False, mot = "", supp = False):
        """
        Quand on lève l'exception.
        'mot' est ce qu'on va afficher au joueur.
        'gagne' indique si le joueur a gagné ou non.
        'supp' indique s'il faut supprimer les progrès.
        """
        self.gagne = gagne
        self.mot = mot
        self.supp = supp

# Créer une AgisException ici.
class AgisException(Exception):
    """
    Exception levée quand on demande au robot
    de faire quelque chose qui n'est pas possible,
    par exemple construire un mur sur une dalle.
    """

    def __init__(self,caseAn = dalle,caseNou = dalle):
        # TODO: Mettre une bonne chaîne d'aide.
        self.caseAn = caseAn
        self.caseNou = caseNou
        
if __name__ == "__main__":
    print("Il n'y a pas eu d'erreur en lançant le fichier 'case'.")


    
