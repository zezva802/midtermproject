import os

import pygame

BASE_IMG_PATH = 'data/images/'


# დამხმარე კლასები სურათების ფაილებიდან შემოსატანად
def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()

    return img


def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images


def load_bg(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()

    return img


def load_bgs(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_bg(path + '/' + img_name))
    return images
