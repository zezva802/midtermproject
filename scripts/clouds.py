import random

import pygame.transform


# parallax ბექგრაუნდების მოძრაობა, რაც შორსაა ნაკლებად მოძრაობს, რაც ახლოს უფრო სწრაფად
class Background:
    def __init__(self, pos, img, speed):
        self.pos = list(pos)
        self.img = img
        self.speed = speed
        self.x = 0

    def render(self, surf, offset=(0, 0)):
        x = ((self.img.get_width() - offset[0]) % (
                surf.get_width() + self.img.get_width()) - self.img.get_width()) * self.speed
        y = self.pos[1] - offset[1]

        surf.blit(self.img, (x, y))


# კლასი ყველა ბექგრაუნდის ერთიანად ორგანიზებისთვის
class Backgrounds:
    def __init__(self, background_images):
        self.bgs = []

        scaled = [pygame.transform.scale(bg, (320, 180)) for bg in background_images]

        self.bgs.append(Background((0, 80), scaled[0], 0.15))
        self.bgs.append(Background((0, 80), scaled[1], 0.3))
        self.bgs.append(Background((0, 80), scaled[2], 0.8))

    def render(self, surf, offset=(0, 0)):
        for bg in self.bgs:
            bg.render(surf, offset=offset)
