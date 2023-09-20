import random

class MapGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = []

    def generate_map(self):
        # Génère la carte avec les bordures
        for _ in range(self.height):
            if _ == 0 or _ == self.height - 1:
                # Première et dernière ligne sont des bordures
                row = '_' * self.width
            elif _ == 1:
                # Deuxième ligne avec le personnage (P)
                row = 'P' + '_' * (self.width - 2) + '1'
            elif _ == self.height - 2:
                # Avant-dernière ligne avec des caractères 'X'
                row = 'X' * self.width
            else:
                # Lignes intérieures avec des caractères aléatoires
                row = '_' + '_' * (self.width - 2) + '_'
            self.map.append(row)

        # Place des groupes de "1" à différents endroits
        for _ in range(2, self.height - 2):  # Commence à la troisième ligne, laisse de l'espace en haut et en bas
            row = list(self.map[_])
            i = 1  # Commence après la bordure gauche
            while i < self.width - 1:
                if row[i] == '_':
                    if random.random() < 0.02:  # Probabilité de placer un groupe de "1"
                        group_size = random.randint(8, 16)  # Taille du groupe de "1"
                        for j in range(i, min(self.width - 1, i + group_size)):
                            row[j] = '1'
                        i += group_size
                    else:
                        i += 1  # Avance d'une case si pas de groupe
                else:
                    i += 1  # Avance d'une case si déjà '1'
            self.map[_] = ''.join(row)

    def save_map(self, filename):
        # Enregistre la carte dans le fichier
        with open(filename, 'w') as f:
            for row in self.map:
                f.write(row + '\n')