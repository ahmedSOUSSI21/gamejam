from .cam import *
from .player import Player
from .block import Block
from pygame.locals import *
import pygame
import os
import sys
sys.path.append('src')


class MapLoader():
    def __init__(self, game):
        self.game = game
        self.layers = []

    def complex_camera(self, camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        l, t, _, _ = -l+375, -t+250, w, h

        # stop scrolling at the left edge
        l = min(0, l)
        l = max(-(camera.width-750), l)   # stop scrolling at the right edge
        t = max(-(camera.height-550), t)  # stop scrolling at the bottom
        t = min(0, t)                           # stop scrolling at the top
        return pygame.Rect(l, t, w, h)

    def load(self, map_num):
        '''Loads the map from a text file, also initiates the camera'''

        path = os.path.join("Maps", "map{}".format(map_num), "level.map")
        with open(path) as f:
            map_txt = f.read()

        col = 0
        row = 0
        level = map_txt.split('\n')
        for line in level:
            for char in line:
                if char == 'P':
                    self.player = Player(self.game, [col, row])

                elif char == '1':
                    block = Block(self.game, [col, row])
                elif char == 'X':
                    block = Block(self.game, [col, row], deathzone=True)
                elif char == 'W':
                    block = Block(self.game, [col, row], win_flag=True)
                elif char == '2':
                    block = Block(self.game, [col, row], bug=True)
                elif char == '_':
                    pass

                col += 25
            row += 25
            col = 0

        self.game.entities.add(self.game.solids)

        total_level_width = len(level[0])*25
        total_level_height = (len(level) - 3)*25
        self.camera = Camera(self.complex_camera,
                             total_level_width, total_level_height)
        self.createLayers(map_num, total_level_width, total_level_height)

    def createLayers(self, map_num, total_level_width, total_level_height):
        '''function to load map layers, rects and then
        create layer objects and load them into the camera class'''

        map_num = str(map_num)
        imgs = os.listdir(os.path.join(
            "Maps", "map{}".format(map_num), "layers"))
        for index in range(1, len(imgs)):
            image = pygame.image.load(os.path.join("Maps", "map{}".format(
                map_num), "layers", "%i.png" % (index))).convert_alpha()
            image = pygame.transform.scale(image, (total_level_width, total_level_height))
            layer = Layer(index, image)
            self.layers.append(layer)
            self.layers.append(layer)
