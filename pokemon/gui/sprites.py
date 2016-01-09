from pygame.sprite import Sprite
from pygame import Rect
import os
import pygame
from pygame.transform import scale


class Entity(Sprite):
    def __init__(self, x, y, width, height):
        Sprite.__init__(self)
        self.rect = Rect(x, y, width, height)


class BackgroundEntity(Entity):
    def __init__(self, x, y):
        directory = os.path.dirname(__file__)
        self.image = pygame.image.load(os.path.join(directory, "pokemon_drink.png"))
        size = self.image.get_size()
        Entity.__init__(self, x, y, size[0], size[1])


class CameraFocus(Entity):
    def __init__(self, x, y):
        Entity.__init__(self, x, y, 0, 0)


class FrameEntity(Entity):
    def __init__(self, x, y):
        directory = os.path.dirname(__file__)
        self.image = pygame.image.load(os.path.join(directory, "frame.png"))
        size = self.image.get_size()
        Entity.__init__(self, x, y, size[0], size[1])


class PlayerSprite(Entity):
    sprite_width = 31
    sprite_height = 32
    sprite_width_space = 1
    sprite_height_space = 0
    scale_factor = 2  # How much sprite is scaled
    counter = 0

    # The top left corner coordinate of Nth sprite
    def get_sprite_location(self, index):
        x = (self.sprite_width + self.sprite_width_space) * (index % 3)
        y = (self.sprite_height + self.sprite_height_space) * (index // 3)
        return (x, y)

    def __init__(self, x, y):
        directory = os.path.dirname(__file__)
        sprite_sheet = pygame.image.load(os.path.join(directory, "player_sprite.png")).convert_alpha()
        self.sprites = []
        for i in range(12):
            sprite = sprite_sheet.subsurface(Rect(self.get_sprite_location(i), (self.sprite_width, self.sprite_height)))
            scaled_size = (self.sprite_width * self.scale_factor, self.sprite_height * self.scale_factor)
            scaled_sprite = scale(sprite, scaled_size)
            self.sprites.append(scaled_sprite)

        self.image = self.sprites[0]

        Entity.__init__(self, x, y, self.sprite_width, self.sprite_height)

    def update(self):
        # TODO: Update depending on movment direction
        self.counter = (self.counter + 1) % len(self.sprites)
        self.image = self.sprites[self.counter]
