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

icon_image = pygame.image.load("Assets/Icon/icon_appli1.png")
pygame.display.set_icon(icon_image)
screen = pygame.display.set_mode((800, 600))


class Game():
    def __init__(self):

        pygame.display.set_caption('Avocat Rush Extrême !')
        pygame.mixer.init()
        self.death_sound = pygame.mixer.Sound("./Assets/death.wav")
        self.death_sound.set_volume(0.8)
        width = 90  # Largeur de la carte

        height = 20  # Hauteur de la carte
        map_generator = MapGenerator(width, height)
        map_generator.generate_map()
        map_generator.save_map('Maps/map6/level.map')
        self.map_number = 1

        pygame.display.set_caption('Avocat Rush Extrême !')

        self.clock = pygame.time.Clock()
        self.last_tick = pygame.time.get_ticks()
        self.screen_res = [750, 500]

        self.font = pygame.font.Font(
            "Assets/Fonts/pixel_operator/PixelOperatorSC-Bold.ttf", 55)

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

                if event.key == K_SPACE or event.key == K_z:
                    self.player.jump()

                # Vérifie si la touche "Esc" (code K_ESCAPE) est enfoncée
                if event.key == K_ESCAPE:
                    self.GoToMainMenu()  # Appel de la méthode pour revenir au menu

            if event.type == USEREVENT:
                if self.counter > 0.01:
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
        if self.map_number > 6:
            self.WinMenu()
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
        if self.counter < 0.01:
            score_text = self.font.render(
                str(round(self.counter, 2)), True, '#F40325')
        elif self.counter < 3 and self.counter > 0.01:
            score_text = self.font.render(
                str(round(self.counter, 2)), True, '#F67C07')
        else:
            score_text = self.font.render(
                str(round(self.counter, 2)), True, '#F5D63D')
            score_text = self.font.render(str(round(self.counter, 2)), True, (245, 214, 61))  # Couleur du texte

            shadow_score_text = self.font.render(str(round(self.counter, 2)), True, (0, 0, 0))  # Couleur de l'ombre

            # Obtene les rectangles pour les deux textes
            score_text_rect = score_text.get_rect()
            shadow_score_text_rect = shadow_score_text.get_rect()

            # Positionne le texte des secondes et son ombre
            x = 10  
            y = 10 
            score_text_rect.topleft = (x, y)  # Position du texte des secondes
            shadow_score_text_rect.topleft = (x + 3, y + 3)  # Position de l'ombre (légèrement décalée)

            # Blitte d'abord l'ombre, puis le texte des secondes
            self.screen.blit(shadow_score_text, shadow_score_text_rect)
            self.screen.blit(score_text, score_text_rect)

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
        self.victory_sound.set_volume(0.9)
        self.fire_sound = pygame.mixer.Sound("./Assets/fire.wav")
        self.fire_sound.set_volume(0.2)
        self.fire_sound.play()
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
        self.counter = 10.0  # le chronomètre se rafraichit
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
        self.Menu()  # Appele la méthode du menu principal pour afficher le menu

    def Menu(self):

        self.button_sound = pygame.mixer.Sound("./Assets/button.wav")

        background_image = pygame.image.load("./Assets/menu_bg.jpg")
        screen_size = self.screen.get_size()
        background_image = pygame.transform.scale(
            background_image, screen_size)
        pygame.mixer.music.load("Assets/intro.wav")  # charge musique d'intro
        pygame.mixer.music.play(-1)

        cinzel_font = pygame.font.Font(
            "Assets/Fonts/static/Cinzel-Regular.ttf", 40)
        
        # Chargement de l'image "temp.png"
        temp_image = pygame.image.load("Assets/temp.png")

        # Position de l'image "temp.png" à gauche
        temp_rect = temp_image.get_rect()
        temp_rect.topleft = (10, 10)  # Ajuste les coordonnées selon votre préférence

        while True:
            self.screen.blit(background_image, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()
            title_text = cinzel_font.render(
                "Avocat Rush Extrême !", True, (255, 255, 255))
            title_rect = title_text.get_rect(
                center=(self.screen_res[0] // 2, 50))
            self.screen.blit(title_text, title_rect)

            # Crée une surface pour l'ombre en noir en utilisant une position légèrement décalée
            shadow_text = cinzel_font.render(
                "Avocat Rush Extrême !", True, (0, 0, 0))
            shadow_rect = shadow_text.get_rect(
                center=(self.screen_res[0] // 2 + 3, 50 + 3))  # Légèrement décalée

            title_rect = title_text.get_rect(
                center=(self.screen_res[0] // 2, 50))

            # Blit l'ombre d'abord, puis le texte principal
            self.screen.blit(shadow_text, shadow_rect)
            self.screen.blit(title_text, title_rect)
            BUTTON_RECT = pygame.image.load("./Sprites/ButtonRect.png")
            BUTTON_RECT = pygame.transform.scale(BUTTON_RECT, (230, 100))

            # Applique l'effet d'ombre aux éléments de texte
            MENU_TEXT = self.font.render("MAIN MENU", True, (255, 255, 255))
            shadow_menu_text = self.font.render("MAIN MENU", True, (0, 0, 0))
            shadow_menu_rect = shadow_menu_text.get_rect(
                center=(self.screen_res[0] // 2 + 3, 100 + 3))
            menu_rect = MENU_TEXT.get_rect(
                center=(self.screen_res[0] // 2, 100))

            PLAY_BUTTON = Button(image=BUTTON_RECT, pos=(screen_size[0]/2, screen_size[1]/2 - 50),
                                 text_input="Play", font=self.font, base_color="White", hovering_color="#fecb88",
                                 button_size=(200, 60))
            play_text = self.font.render("Play", True, (255, 255, 255))
            shadow_play_text = self.font.render("Play", True, (0, 0, 0))
            shadow_play_rect = shadow_play_text.get_rect(
                center=(screen_size[0]/2 + 3, screen_size[1]/2 - 50 + 3))
            play_rect = play_text.get_rect(
                center=(screen_size[0]/2, screen_size[1]/2 - 50))

            OPTION_BUTTON = Button(image=BUTTON_RECT, pos=(screen_size[0]/2, screen_size[1]/2 + 60),

                                   text_input="Option", font=self.font, base_color="White", hovering_color="#fecb88",
                                   button_size=(200, 60))
            option_text = self.font.render("Option", True, (255, 255, 255))
            shadow_option_text = self.font.render("Option", True, (0, 0, 0))
            shadow_option_rect = shadow_option_text.get_rect(
                center=(screen_size[0]/2 + 3, screen_size[1]/2 + 60 + 3))
            option_rect = option_text.get_rect(
                center=(screen_size[0]/2, screen_size[1]/2 + 60))

            QUIT_BUTTON = Button(image=BUTTON_RECT, pos=(screen_size[0]/2, screen_size[1]/2 + 170),
                                 text_input="Quit", font=self.font, base_color="White", hovering_color="#fecb88",
                                 button_size=(200, 60))
            quit_text = self.font.render("Quit", True, (255, 255, 255))
            shadow_quit_text = self.font.render("Quit", True, (0, 0, 0))
            shadow_quit_rect = shadow_quit_text.get_rect(
                center=(screen_size[0]/2 + 3, screen_size[1]/2 + 170 + 3))
            quit_rect = quit_text.get_rect(
                center=(screen_size[0]/2, screen_size[1]/2 + 170))

            # Blit l'effet d'ombre d'abord, puis le texte principal
            self.screen.blit(shadow_menu_text, shadow_menu_rect)
            self.screen.blit(MENU_TEXT, menu_rect)

            self.screen.blit(shadow_play_text, shadow_play_rect)
            self.screen.blit(play_text, play_rect)

            self.screen.blit(shadow_option_text, shadow_option_rect)
            self.screen.blit(option_text, option_rect)

            self.screen.blit(shadow_quit_text, shadow_quit_rect)
            self.screen.blit(quit_text, quit_rect)

            #self.screen.blit(MENU_TEXT, menu_rect)

            for button in [PLAY_BUTTON, QUIT_BUTTON, OPTION_BUTTON]:
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

    def WinMenu(self):
        self.button_sound = pygame.mixer.Sound("./Assets/button.wav")
        background_image = pygame.image.load("./Assets/Win_bg.jpg")
        screen_size = self.screen.get_size()
        background_image = pygame.transform.scale(
            background_image, screen_size)
        pygame.mixer.music.play(-1)
        while True:
            self.screen.blit(background_image, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.font.render("You Won !", True, "#fec377")
            MENU_RECT = MENU_TEXT.get_rect(center=(screen_size[0]/2, 50))

            BUTTON_RECT = pygame.image.load("./Sprites/ButtonRect.png")
            BUTTON_RECT = pygame.transform.scale(BUTTON_RECT, (250, 100))

            PLAY_BUTTON = Button(image=BUTTON_RECT, pos=(screen_size[0]/2, screen_size[1]/2 - 50),
                                 text_input="PLAY AGAIN", font=self.font, base_color="White", hovering_color="#fecb88")
            QUIT_BUTTON = Button(image=BUTTON_RECT, pos=(screen_size[0]/2, screen_size[1]/2 + 100),
                                 text_input="QUIT", font=self.font, base_color="White", hovering_color="#fecb88")

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
                        self.map_number = 1
                        self.Play()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.mixer.music.stop()  # Arrête musique d'introduction
                        self.button_sound.play()

                        pygame.quit()
                        sys.exit()

            pygame.display.update()


Game()
