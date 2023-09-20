import random

class MapGenerator:
    def __init__(self, width, height):
        print('ici')
        self.width = width
        self.height = height
        self.map = []

    def generate_map(self):
        # Génére la carte aléatoire
        for _ in range(self.height):
            row = ''.join(random.choice(['1', '1', '1', '_', '_']) for _ in range(self.width))
            self.map.append(row)

        # Placer le personnage (P) sur la première ligne
        self.map[0] = 'P' + self.map[0][1:]

    def save_map(self, filename):
        # Enregistrer la carte dans le fichier
        with open(filename, 'w') as f:
            for row in self.map:
                f.write(row + '\n')