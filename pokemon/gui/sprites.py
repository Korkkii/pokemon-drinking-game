from pygame.sprite import Sprite
from pygame import Rect
import os
import pygame
from pygame.transform import scale
from pygame.math import Vector2 as vec2
import time
from gui.constants import Direction, DIRECTIONS


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
    """
    Player sprite class that shows appropriate sprite for sprite state.
    """

    # Sprite dimensions
    sprite_width = 31
    sprite_height = 32
    sprite_width_space = 1
    sprite_height_space = 0
    scale_factor = 2

    # Sprite state
    velocity = 10
    start_frame = time.time()
    number_of_movement_images = 2
    facing_direction = Direction.RIGHT
    moving = False
    fps = 5  # How fast sprite should be updated

    # The top left corner coordinate of Nth sprite in a sprite sheet
    def get_sprite_location(self, index):
        x = (self.sprite_width + self.sprite_width_space) * (index % 3)
        y = (self.sprite_height + self.sprite_height_space) * (index // 3)
        return (x, y)

    def __init__(self, x, y):
        # Get sprite sheet
        directory = os.path.dirname(__file__)
        sprite_sheet = pygame.image.load(os.path.join(directory, "player_sprite.png")).convert_alpha()

        # Order of sprites' alignments in sprite sheet
        sprite_sheet_direction = [Direction.DOWN, Direction.LEFT, Direction.RIGHT, Direction.UP]

        # Create all sprites to a dict
        self.sprites = {}
        for i in range(0, 12, 3):
            direction_sprites = []
            scaled_sprite_size = (self.sprite_width * self.scale_factor, self.sprite_height * self.scale_factor)

            # Get all sprites with certain alignment
            sprite_move_1 = Rect(self.get_sprite_location(i), (self.sprite_width, self.sprite_height))
            sprite_stationary = Rect(self.get_sprite_location(i + 1), (self.sprite_width, self.sprite_height))
            sprite_move_2 = Rect(self.get_sprite_location(i + 2), (self.sprite_width, self.sprite_height))

            current_direction = sprite_sheet_direction[i // 3]

            if current_direction == Direction.RIGHT or current_direction == Direction.LEFT:
                direction_sprites = [scale(sprite_sheet.subsurface(rect), scaled_sprite_size) for rect in
                                     [sprite_move_1, sprite_stationary, sprite_move_2]]
            else:
                direction_sprites = [scale(sprite_sheet.subsurface(rect), scaled_sprite_size) for rect in
                                     [sprite_move_1, sprite_move_2, sprite_stationary]]

            # Add sprites to sprite dict with alignment as key
            self.sprites[sprite_sheet_direction[i // 3]] = direction_sprites

        self.image = self.sprites[self.facing_direction][-1]  # Select stationary image
        self.target = vec2(x, y)
        Entity.__init__(self, x, y, self.sprite_width * self.scale_factor, self.sprite_height * self.scale_factor)

    def update(self):
        if not self.moving:
            # Stationary image
            self.image = self.sprites[self.facing_direction][-1]
        else:
            # Update image
            frame_index = int((time.time() - self.start_frame) * self.fps % self.number_of_movement_images)
            self.image = self.sprites[self.facing_direction][frame_index]

            # Calculate new position
            new_velocity = DIRECTIONS[self.facing_direction] * self.velocity
            self.rect.move_ip(new_velocity.x, new_velocity.y)
