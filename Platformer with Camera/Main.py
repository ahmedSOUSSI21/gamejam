from src.cam import *
from src.maploader import MapLoader
from src.block import Block
from src.player import Player
import pygame

from pygame.locals import *
import sys
import random

sys.path.append('src')


pygame.init()


class Game():
    def __init__(self):

        pygame.display.set_caption('Platformer')

        self.clock = pygame.time.Clock()
        self.last_tick = pygame.time.get_ticks()
        self.screen_res = [750, 500]

        self.font = pygame.font.SysFont("Consolas", 55)
        self.screen = pygame.display.set_mode(
            self.screen_res, pygame.HWSURFACE, 32)

        self.Play()

    def Loop(self):
        # main game loop
        self.eventLoop()

        self.Tick()
        if(self.Draw()):
            return True
        pygame.display.update()
        return False

    def eventLoop(self):
        # the main event loop, detects keypresses
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    self.reset()
                    self.maploader.load(2)

                if event.key == K_SPACE:
                    self.player.jump()

            if event.type == USEREVENT:
                if self.counter > 0:
                    self.counter -= 1
                else:
                    self.reset()
            
            if event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x >= 0 and mouse_x <= 50 and mouse_y >=0 and mouse_y <= 50:
                    self.counter += 10



    def Tick(self):
        self.ttime = self.clock.tick()
        self.mpos = pygame.mouse.get_pos()
        self.keys_pressed = pygame.key.get_pressed()

    def reset(self):
        self.Play()

    def Draw(self):
        self.screen.fill((150, 150, 150))

        # Update layers (have to reverse list to blit properly)
        for l in self.maploader.layers[::-1]:
            self.screen.blit(l.image, self.camera.apply_layer(l))

        if(self.player.update(self.ttime / 1000.)):
            print("DEAD MAN ! ")
            return True
        self.camera.update(self.player)

        for e in self.entities:  # update blocks etc.
            self.screen.blit(e.image, self.camera.apply(e))

        # dispaly chrono
        score_text = self.font.render(str(self.counter), True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        return False

    def Play(self):
        pygame.time.set_timer(USEREVENT, 1000)
        self.counter = 10

        self.entities = pygame.sprite.Group()
        self.solids = pygame.sprite.Group()
        self.deathzones = pygame.sprite.Group()
        self.maploader = MapLoader(self)

        self.maploader.load(1)
        self.player = self.maploader.player
        self.camera = self.maploader.camera

        self.entities.add(self.solids)
        self.entities.add(self.deathzones)
        self.entities.add(self.player)

        self.clock.tick(60)
        while 1:
            if(self.Loop()):
                self.reset()


Game()
