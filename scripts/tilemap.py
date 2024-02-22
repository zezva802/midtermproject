import pygame


# ტურის ბლოკების, გარემოს კლასი


class Tilemap:
    def __init__(self, game, tile_size=(16, 16)):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []
        # tiled აპლიკაციის(ტურების შესაქმნელი) ბიბლიოთეკის საშუალებით ბლოკების გამოტანა და ლექსიკონში/ სიაში შეტანა
        self.sprite_group = pygame.sprite.Group()
        for layer in game.tmx_data.visible_layers:
            if layer.name == 'offtile':
                for tile in layer.tiles():
                    self.offgrid_tiles.append(tile)
            elif layer.name == 'environment':
                for tile in layer.tiles():
                    self.tilemap[str(tile[0]) + ";" + str(tile[1])] = {'pos': (tile[0], tile[1]), 'img': tile[2]}

    # ბლოკების სიაში ჩამატება რასაც შეიძლება დავეჯახოთ
    # doit!!!!!!!
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tilemap:
            tl = self.tilemap[tile]

            rects.append(
                pygame.Rect(tl['pos'][0] * self.tile_size[0], tl['pos'][1] * self.tile_size[1], self.tile_size[0],
                            self.tile_size[1]))
        return rects

    # ბლოკების გამოტანა ეკრანზე, მხოლოდ იმათი რაც ახლოსაა და არა ეკრანს იქით რათა კომპიუტერისთვის შრომატევადი არ იყოს
    # offset აკლდება რათა წინ წასვლისას ბლოკებმა უკან გადაიწიოს და კამერის ეფექტი შეიქმნას
    def render(self, surf, offset=(0, 0)):

        for i in self.offgrid_tiles:
            surf.blit(i[2], (i[0] * self.tile_size[0] - offset[0], i[1] * self.tile_size[1] - offset[1]))

        for x in range(offset[0] // self.tile_size[0], (offset[0] + surf.get_width()) // self.tile_size[0] + 1):
            for y in range(offset[1] // self.tile_size[1], (offset[1] + surf.get_height()) // self.tile_size[1] + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(tile['img'],
                              (
                                  tile['pos'][0] * self.tile_size[0] - offset[0],
                                  tile['pos'][1] * self.tile_size[1] - offset[1]))

        # for loc in self.tilemap:
        #     tile = self.tilemap[loc]
        #
        #     surf.blit(self.game.assets[tile['type']][tile['variant']],
        #               (tile['pos'][0] * self.tile_size-offset[0], tile['pos'][1] * self.tile_size-offset[1]))
