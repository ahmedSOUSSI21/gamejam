import pygame
from pygame.locals import *

class Block(pygame.sprite.Sprite):
    def __init__(self, game, pos, deathzone=False):
        pygame.sprite.Sprite.__init__(self)
        self.deathzone = deathzone
        self.game = game
        
        if deathzone:
            self.game.deathzones.add(self)
        else:
            self.game.solids.add(self)

        self.image = pygame.Surface([25,25])
        self.image.fill((255,0,15))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self):
        pass
