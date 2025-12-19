
from Terrain import Terrain, Case
from StrategieReseau import StrategieReseau, StrategieReseauAuto

class Reseau:
    def __init__(self):
        self.strat = StrategieReseauAuto()
        self.noeuds = {}
        self.arcs = []

        self.noeud_entree = -1

    def definir_entree(self, n: int) -> None:
        if n in self.noeuds.keys():
            self.noeud_entree = n
        else:
            self.noeud_entree = -1


    def ajouter_arc(self, n1: int, n2: int) -> None:
        if n1 > n2:
            tmp = n2
            n2 = n1
            n1 = tmp
        if n1 not in self.noeuds.keys() or n2 not in self.noeuds.keys():
            return
        if (n1, n2) not in self.arcs:
            self.arcs.append((n1, n2))

    def set_strategie(self, strat: StrategieReseau):
        self.strat = strat

    def valider_reseau(self) -> bool:
        if self.noeud_entree == -1:
            return False

        visites = set()
        a_faire = [self.noeud_entree]

        while a_faire:
            n = a_faire.pop()
            if n not in visites:
                visites.add(n)
                for (a, b) in self.arcs:
                    if a == n and b not in visites:
                        a_faire.append(b)
                    elif b == n and a not in visites:
                     a_faire.append(a)

        return len(visites) == len(self.noeuds)
    def ajouter_noeud(self, n: int, coords: tuple[int, int]):
        if n >= 0:
            self.noeuds[n] = coords


    def valider_distribution(self, t: Terrain) -> bool:
    # Le réseau doit déjà être valide
        if not self.valider_reseau():
            return False

    # Parcours du réseau depuis le noeud d'entrée
        visites = set()
        pile = [self.noeud_entree]

        while pile:
            n = pile.pop()
            if n not in visites:
                visites.add(n)
                for a, b in self.arcs:
                    if a == n and b not in visites:
                        pile.append(b)
                    elif b == n and a not in visites:
                        pile.append(a)

    # Vérifier que chaque client est sur un noeud atteignable
        for li in range(len(t.cases)):
            for co in range(len(t.cases[li])):
                if t.cases[li][co] == Case.CLIENT:
                    trouve = False
                    for nid, (nx, ny) in self.noeuds.items():
                        if nid in visites and nx == li and ny == co:
                            trouve = True
                            break
                    if not trouve:
                        return False

        return True









    def configurer(self, t: Terrain):
        self.noeud_entree, self.noeuds, self.arcs  = self.strat.configurer(t)

    def afficher(self) -> None:
        for ligne in self.cases:
            for case in ligne:
                if case == Case.VIDE:
                    print("~", end="")
                elif case == Case.CLIENT:
                    print("C", end="")
                elif case == Case.ENTREE:
                    print("E", end="")
                elif case == Case.OBSTACLE:
                    print("X", end="")
            print()


    def afficher_avec_terrain(self, t: Terrain) -> None:
        for ligne, l in enumerate(t.cases):
            for colonne, c in enumerate(l):
                if (ligne, colonne) not in self.noeuds.values():
                    if c == Case.OBSTACLE:
                        print("X", end="")
                    if c == Case.CLIENT:
                        print("C", end="")
                    if c == Case.VIDE:
                        print("~", end="")
                    if c == Case.ENTREE:
                        print("E", end="")
                    else:
                        print(" ", end="")
                else:
                    if c == Case.OBSTACLE:
                        print("T", end="")
                    if c == Case.CLIENT:
                        print("C", end="")
                    if c == Case.VIDE:
                        print("+", end="")
                    if c == Case.ENTREE:
                        print("E", end="")
                    else:
                        print(" ", end="")
            print()

    def calculer_cout(self, t: Terrain) -> float:
        cout = 0
        for _ in self.arcs:
            cout += 1.5
        for n in self.noeuds.values():
            if t[n[0]][n[1]] == Case.OBSTACLE:
                cout += 2
            else:
                cout += 1
        return cout
