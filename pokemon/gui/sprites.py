from pygame.sprite import Sprite
from pygame import Rect
import os
import pygame


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
        Entity.__init__(self, x, y, 10, 10)
