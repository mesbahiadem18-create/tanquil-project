
from heapq import heappush, heappop
from itertools import count

from taquin import EF, showM, saisir_grille


def h(M):
    """Heuristique Manhattan."""
    positions = {}

    for i in range(3):
        for j in range(3):
            positions[EF[i][j]] = (i, j)

    distance = 0

    for i in range(3):
        for j in range(3):
            valeur = M[i][j]

            if valeur != 0:
                li, col = positions[valeur]
                distance += abs(i - li) + abs(j - col)

    return distance


def voisins(M):
    """Génère les états voisins sans modifier M."""
    position = next(
        (i, j)
        for i in range(3)
        for j in range(3)
        if M[i][j] == 0
    )

    i, j = position

    for direction, (ni, nj) in {
        "up": (i - 1, j),
        "down": (i + 1, j),
        "left": (i, j - 1),
        "right": (i, j + 1),
    }.items():

        if 0 <= ni < 3 and 0 <= nj < 3:
            nouveau = [ligne[:] for ligne in M]
            nouveau[i][j], nouveau[ni][nj] = (
                nouveau[ni][nj],
                nouveau[i][j],
            )
            yield nouveau, direction


def astar(depart):
    depart = tuple(tuple(ligne) for ligne in depart)
    but = tuple(tuple(ligne) for ligne in EF)

    compteur = count()
    file = []
    heappush(file, (h(depart), next(compteur), depart))

    g_score = {depart: 0}
    parents = {depart: None}

    while file:
        _, _, courant = heappop(file)

        if courant == but:
            chemin = []

            while parents[courant] is not None:
                precedent, direction = parents[courant]
                chemin.append((courant, direction))
                courant = precedent

            return list(reversed(chemin))

        M = [list(ligne) for ligne in courant]

        for grille, direction in voisins(M):
            voisin = tuple(tuple(ligne) for ligne in grille)
            nouveau_g = g_score[courant] + 1

            if nouveau_g < g_score.get(voisin, float("inf")):
                g_score[voisin] = nouveau_g
                parents[voisin] = (courant, direction)

                f = nouveau_g + h(voisin)
                heappush(file, (f, next(compteur), voisin))

    return None
