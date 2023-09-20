import pygame
from pygame.locals import *
import os, sys
sys.path.append('src')

class Block(pygame.sprite.Sprite):
    def __init__(self, game, pos, deathzone=False):
        pygame.sprite.Sprite.__init__(self)
        self.deathzone = deathzone
        self.game = game
        
        if deathzone:
            self.game.deathzones.add(self)
            self.image = pygame.image.load(os.path.join("Sprites", "deathblock.png"))
        else:
            self.game.solids.add(self)
            self.image = pygame.image.load(os.path.join("Sprites", "block.png"))
        self.image = pygame.transform.scale(self.image, (25, 25))
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self):
        pass
