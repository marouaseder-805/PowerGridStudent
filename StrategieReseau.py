from Terrain import Terrain, Case

class StrategieReseau:
    def configurer(self, t: Terrain) -> tuple[int, dict[int, tuple[int, int]], list[int]]:
        return -1, {}, []


class StrategieReseauManuelle(StrategieReseau):
    def configurer(self, t: Terrain) -> tuple[int, dict[int, tuple[int, int]], list[int]]:
        # RÉSEAU MANUEL = même principe que AUTO pour l’instant
        noeuds = {}
        arcs = []

        # trouver entrée
        entree = None
        for y, ligne in enumerate(t.cases):
            for x, case in enumerate(ligne):
                if case == Case.ENTREE:
                    entree = (x, y)
                    break
            if entree:
                break

        if not entree:
            return -1, {}, []

        noeuds[0] = entree
        nid = 1

        # ajouter un noeud par client
        for y, ligne in enumerate(t.cases):
            for x, case in enumerate(ligne):
                if case == Case.CLIENT:
                    noeuds[nid] = (x, y)
                    arcs.append((0, nid))
                    nid += 1

        return 0, noeuds, arcs


class StrategieReseauAuto(StrategieReseau):
    def configurer(self, t: Terrain) -> tuple[int, dict[int, tuple[int, int]], list[int]]:
        noeuds = {}
        arcs = []

        entree = None
        for y, ligne in enumerate(t.cases):
            for x, case in enumerate(ligne):
                if case == Case.ENTREE:
                    entree = (y, x)
                    break
            if entree:
                break

        if not entree:
            return -1, {}, []

        noeuds[0] = entree
        nid = 1

        for y, ligne in enumerate(t.cases):
            for x, case in enumerate(ligne):
                if case == Case.CLIENT:
                    noeuds[nid] = (y, x)
                    arcs.append((0, nid))
                    nid += 1

        return 0, noeuds, arcs

