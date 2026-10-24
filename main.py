
from taquin import EF, showM, saisir_grille
from astar import astar


def main():
    # Saisie de l'état initial
    depart = saisir_grille()

    print("\nÉtat initial :")
    showM(depart)

    # Vérifier si le Taquin est déjà résolu
    if depart == EF:
        print("\nLe Taquin est déjà résolu !")
        return

    # Lancer l'algorithme A*
    print("\nRecherche de la solution avec A*...")
    solution = astar(depart)

    if solution is None:
        print("Aucune solution trouvée.")
        return

    # Afficher la solution
    print(f"\nSolution trouvée en {len(solution)} mouvement(s).")

    for numero, (grille, direction) in enumerate(solution, start=1):
        print(f"\nMouvement {numero} : déplacer 0 vers {direction}")
        showM([list(ligne) for ligne in grille])


if __name__ == "__main__":
    main()
