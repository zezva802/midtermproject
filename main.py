import os.path
import sys

import pygame
from scripts.entities import PhysicsEntity
from scripts.tilemap import Tilemap
from scripts.utils import load_image, load_images, load_bg, load_bgs
from scripts.clouds import Backgrounds
from pytmx.util_pygame import load_pygame


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('tamashi')
        self.screen = pygame.display.set_mode((1280, 720))
        self.display = pygame.Surface((320, 180))
        self.tmx_data = load_pygame('data/lvl.tmx')
        self.movement = [False, False]
        self.assets = {
            'player': load_bg('entities/player.png'),

            'backgrounds': load_bgs('bg'),
            'background': load_image('current.png')
        }

        self.bgs = Backgrounds(self.assets['backgrounds'])
        self.background = pygame.transform.scale(self.assets['background'], (320, 180))
        self.player = PhysicsEntity(self, 'player', (50, 50), (8, 29))
        self.tilemap = Tilemap(self, tile_size=(16, 16))
        self.clock = pygame.time.Clock()
        self.scroll = [0, 0]

    def run(self):
        while True:

            self.display.fill((255, 255, 255))

            self.display.blit(self.background, (0, 0))

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30 - 1
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.bgs.render(self.display, offset=render_scroll)
            self.tilemap.render(self.display, offset=render_scroll)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            screen_scaled = pygame.transform.scale(self.display, self.screen.get_size())
            self.screen.blit(screen_scaled, (0, 0))
            pygame.display.update()

            self.clock.tick(60)


Game().run()
