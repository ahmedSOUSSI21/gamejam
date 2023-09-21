from src.cam import *
from Maps.map_generateur import MapGenerator
from src.maploader import MapLoader
from src.block import Block
from src.player import Player
import pygame

from pygame.locals import *
import sys
import random
from src.button import Button

sys.path.append('src')


pygame.init()


class Game():
    def __init__(self):

        pygame.display.set_caption('Avocat Rush Extrême !')
        pygame.mixer.init()
        self.death_sound = pygame.mixer.Sound("./Assets/death.wav")

        width = 90  # Largeur de la carte

        height = 20  # Hauteur de la carte
        map_generator = MapGenerator(width, height)
        map_generator.generate_map()
        map_generator.save_map('Maps/map2/level.map')
        self.map_number = 1

        pygame.display.set_caption('Platformer')

        self.clock = pygame.time.Clock()
        self.last_tick = pygame.time.get_ticks()
        self.screen_res = [750, 500]

        self.font = pygame.font.SysFont("Impact", 55)
        self.screen = pygame.display.set_mode(
            self.screen_res, pygame.HWSURFACE, 32)

        self.Menu()

    def Loop(self):
        # main game loop
        self.eventLoop()

        self.Tick()
        value = self.Draw()
        if value == "DEAD":
            return "DEAD"
        elif value == "WIN":
            return "WIN"

        pygame.display.update()
        return ""

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

                # Vérifie si la touche "Esc" (code K_ESCAPE) est enfoncée
                if event.key == K_ESCAPE:
                    self.GoToMainMenu()  # Appel de la méthode pour revenir au menu

            if event.type == USEREVENT:
                if self.counter > 0:
                    self.counter -= 0.01
                else:
                    self.death_sound.play()
                    self.reset()

            if event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x >= 0 and mouse_x <= 50 and mouse_y >= 0 and mouse_y <= 50:
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

        value = self.player.update(self.ttime / 1000.)
        if value == "DEAD":
            print("DEAD MAN ! ")
            return "DEAD"
        elif value == "WIN":
            print("WIN")
            return "WIN"

        self.camera.update(self.player)

        for e in self.entities:  # update blocks etc.
            self.screen.blit(e.image, self.camera.apply(e))

        # dispaly chrono
        score_text = self.font.render(
            str(round(self.counter, 2)), True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        return ""

    def Play(self):
        pygame.time.set_timer(USEREVENT, 10)
        self.counter = 10.0

        self.entities = pygame.sprite.Group()
        self.solids = pygame.sprite.Group()
        self.win_flags = pygame.sprite.Group()
        self.deathzones = pygame.sprite.Group()
        self.maploader = MapLoader(self)

        self.maploader.load(self.map_number)
        self.player = self.maploader.player
        self.camera = self.maploader.camera

        self.entities.add(self.solids)
        self.entities.add(self.deathzones)
        self.entities.add(self.player)
        self.entities.add(self.win_flags)

        self.victory_sound = pygame.mixer.Sound("./Assets/victory.wav")

        self.clock.tick(60)
        while 1:
            value = self.Loop()
            if value == "DEAD":
                self.death_sound.play()
                self.reset()
            elif value == "WIN":
                self.victory_sound.play()
                self.map_number += 1
                self.reset()

                break

    def GoToMainMenu(self):
        self.counter = 10.0  # Réinitialisez le chronomètre si nécessaire
        self.entities.empty()
        self.solids.empty()
        self.win_flags.empty()
        self.deathzones.empty()
        self.maploader = MapLoader(self)
        self.maploader.load(1)
        self.player = self.maploader.player
        self.camera = self.maploader.camera
        self.entities.add(self.solids)
        self.entities.add(self.deathzones)
        self.entities.add(self.player)
        self.entities.add(self.win_flags)
        self.state = "menu"  # Définissez l'état sur "menu" pour revenir au menu principal
        self.Menu()  # Appelez la méthode du menu principal pour afficher le menu

    def Menu(self):

        self.button_sound = pygame.mixer.Sound("./Assets/button.wav")

        background_image = pygame.image.load("./Sprites/menu_background.png")
        screen_size = self.screen.get_size()
        background_image = pygame.transform.scale(
            background_image, screen_size)

        while True:
            self.screen.blit(background_image, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.font.render("MAIN MENU", True, "#111253")
            MENU_RECT = MENU_TEXT.get_rect(center=(screen_size[0]/2, 50))

            PLAY_BUTTON = Button(image=pygame.image.load("./Sprites/ButtonRect.png"), pos=(screen_size[0]/2, screen_size[1]/2 - 50),
                                 text_input="PLAY", font=self.font, base_color="White", hovering_color="#6db7f5")
            QUIT_BUTTON = Button(image=pygame.image.load("./Sprites/ButtonRect.png"), pos=(screen_size[0]/2, screen_size[1]/2 + 100),
                                 text_input="QUIT", font=self.font, base_color="White", hovering_color="#6db7f5")

            self.screen.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.button_sound.play()
                        pygame.mixer.music.stop()  # Arrête musique d'introduction
                        self.Play()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.button_sound.play()
                        pygame.mixer.music.stop()  # Arrêtela musique d'intro

                        pygame.quit()
                        sys.exit()

            pygame.display.update()


Game()
