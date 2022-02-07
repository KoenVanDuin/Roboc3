# -*-coding:Latin-1 -*
"""
Ce module contient la classe 'case' et les exceptions.
"""
import af

af.afInfo = False

cases = [] # On met toutes les cases dans une liste.
# Comme �a un peut parcourir les cases avec une boucle.

class Case:
    """
    Cettes classe repr�sente un objets sur la carte.
    Elle n'a que quelques instances qu'on peut voir en dessous
    du corps de la classe.
    """
    
    def __init__(self,symbole,signe,desc):
        """
        Le constructeur des cases.
        'symbole' est le signe qu'on utilise
        pour afficher la case.
        'signes' est une liste de symbloles
        par lequel on peut repr�senter une case
        quand on fait une carte par le biais d'un fichier.
        Il y a aussi une description � afficher.
        """
        self.symbole = symbole
        signes = [signe,symbole[0],symbole[1]]
        signes = [s.lower() for s in signes]
        self.signes = signes
        self.desc = desc
        cases.append(self)
        # Je veux pouvoir utiliser le symbole d'affichage
        # quand je cr�e un fichier de carte.
        
        
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
# J'ai d�cid� ici comment l'afficher:
robot = "XX"

# Voici toutes les exceptions que j'ai eu besoin de d�finir.

class ObsException(Exception):
    """
    Exception lev�e quand on trouve un objet sur le chemin
    qui fait s'arr�ter le robot.
    """
    def __init__(self,objet=bar,mot="",xyObs=None):
        """
        Pour bien traiter l'exception, on a besoin de savoir
        devant quel objet le robot s'arr�te, et o� l'objet
        se trouve, quand il s'agit d'une barricade.
        """
        self.objet = objet
        self.mot = mot
        self.xyObs = xyObs

class FinException(Exception):
    """
    Exception lev�e quand le jeu doit se terminer.
    C'est le cas lorsque le joueur gagne, perd,
    ou choisit lui-m�me d'arr�ter de jouer.
    """

    def __init__(self,gagne = False, mot = "", supp = False):
        """
        Quand on l�ve l'exception.
        'mot' est ce qu'on va afficher au joueur.
        'gagne' indique si le joueur a gagn� ou non.
        'supp' indique s'il faut supprimer les progr�s.
        """
        self.gagne = gagne
        self.mot = mot
        self.supp = supp

# Cr�er une AgisException ici.
class AgisException(Exception):
    """
    Exception lev�e quand on demande au robot
    de faire quelque chose qui n'est pas possible,
    par exemple construire un mur sur une dalle.
    """

    def __init__(self,caseAn = dalle,caseNou = dalle):
        # TODO: Mettre une bonne cha�ne d'aide.
        self.caseAn = caseAn
        self.caseNou = caseNou
        
if __name__ == "__main__":
    print("Il n'y a pas eu d'erreur en lan�ant le fichier 'case'.")


    
