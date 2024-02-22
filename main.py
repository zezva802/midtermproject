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

        pygame.display.set_caption('tamashi')  # სათაური
        self.screen = pygame.display.set_mode((1280, 720))  # ფანჯრის შექმნა, ზომები
        self.display = pygame.Surface((320, 180))  # surface შექმნა, სადაც თამაში ხდება, ამ ზომებში არის რეალურად თამაში
        self.tmx_data = load_pygame('data/lvl.tmx')  # Tiled-ის საშუალებით level, map, tiles, გადმოტანა
        self.movement = [False, False]  # მოძრაობებისთვის
        self.assets = {
            'player': load_bg('entities/player.png'),

            'backgrounds': load_bgs('bg'),
            'background': load_image('current.png')
        }  # სურათების ლექსიკონში შენახვა

        self.bgs = Backgrounds(
            self.assets['backgrounds'])  # ბექგრაუნდის კლასის შექმნა, შაჭიროა parallax ეფექტის მისაღებად
        self.background = pygame.transform.scale(self.assets['background'],
                                                 (320, 180))  # მთავარი ფონი, გადაყვანილი სკალირებული ზომებში
        self.player = PhysicsEntity(self, 'player', (50, 50),
                                    (8, 29))  # მთავარი გმირის შექმნა, პოზიციებისა და ზომების მითითება
        self.tilemap = Tilemap(self, tile_size=(
        16, 16))  # ბლოკების კლასის შექმნა კუბიკის ზომების მითითება (defaultად თამაშში ვიყენებ 16*16ზე ბლოკებს)
        self.clock = pygame.time.Clock()  # საათის შექმნა (საჭიროა fpsის სარეგულიროდ
        self.scroll = [0, 0]  # სქროლის ცვლადი (საჭიროა კამერისთვის)

    def run(self):
        while True:

            self.display.fill((255, 255, 255))  # ყოველი იტერაციის დასაწყისში ე.წ refresh გაკეთება

            self.display.blit(self.background, (0, 0))  # ბექგრაუნდის გამოტანა
            # პლეიერსა და კამერას შორის კოორდინატების სხვაობის გამოთვლა და
            # დათვლა თუ რამდენით უნდა გადაიწიოს თამაშის თითოეულმა ელემენტმა კამერის ეფექტის მისაღებად
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30 - 1
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))  # საბოლოო ცვლადი

            self.bgs.render(self.display,
                            offset=render_scroll)  # მთავარი ბაქგრაუნდის შემდეგ უფრო ახლოს მყოფი მაგ, მთების, გორაკების გამოტანა
            self.tilemap.render(self.display, offset=render_scroll)  # ტურის ბლოკების გამოტანა

            self.player.update(self.tilemap,
                               (self.movement[1] - self.movement[0], 0))  # მთავარი გმირის პოზიციების განახლება
            self.player.render(self.display, offset=render_scroll)  # მთავარი გმირის თამაშში გამოტანა

            # ღილაკების დაჭერის მიხედვით თამაშის ცვლილება
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
            # თამაშის ზედაპირის გამოტანა უფრო მაღალ ეკრანის ზედაპირზე
            screen_scaled = pygame.transform.scale(self.display, self.screen.get_size())
            self.screen.blit(screen_scaled, (0, 0))
            pygame.display.update()
            # fps
            self.clock.tick(60)


# თამაშის კლასის დაწყება
Game().run()
