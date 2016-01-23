import os
import time
from collections import deque

import pygame
from pygame import Rect
from pygame.math import Vector2 as vec2
from pygame.sprite import Sprite
from pygame.transform import scale

from pokemon.gui.constants import DIRECTIONS, Direction, State


class Entity(Sprite):

    def __init__(self, x, y, width, height):
        Sprite.__init__(self)
        self.rect = Rect(x, y, width, height)


class BackgroundEntity(Entity):

    def __init__(self, x, y):
        directory = os.path.dirname(__file__)
        self.image = pygame.image.load(os.path.join(directory, "gameboard.png")).convert()
        size = self.image.get_size()
        Entity.__init__(self, x, y, size[0], size[1])


class CameraFocus(Entity):

    def __init__(self, x, y):
        Entity.__init__(self, x, y, 0, 0)


class FrameEntity(Entity):

    def __init__(self, x, y):
        directory = os.path.dirname(__file__)
        self.image = pygame.image.load(os.path.join(directory, "frame.png")).convert()
        size = self.image.get_size()
        Entity.__init__(self, x, y, size[0], size[1])


class MovingSprite(Entity):
        # Sprite state
        speed = 10
        facing_direction = Direction.STATIONARY
        state = State.STATIONARY
        targets = deque() # Target queue

        def __init__(self, x, y, width, height):
            super(MovingSprite, self).__init__(x, y, width, height)
            # Center the sprite to initial coords
            center_coords = (self.rect.centerx - self.rect.width, self.rect.centery - self.rect.height)
            self.rect = Rect(center_coords, self.rect.size)
            # Set current movement target equal to initial position
            self.target = vec2(self.rect.centerx, self.rect.centery)

        def move_to_target(self, x, y):
            # Set new direction
            new_target = vec2(x, y)

            if self.state == State.STATIONARY and new_target != self.target and not self.need_to_move():
                if x > self.target.x:
                    self.facing_direction = Direction.RIGHT
                elif x < self.target.x:
                    self.facing_direction = Direction.LEFT
                elif y > self.target.y:
                    self.facing_direction = Direction.DOWN
                elif y < self.target.y:
                    self.facing_direction = Direction.UP

                self.state = State.MOVING
                self.target = vec2(x, y)
            else:
                self.targets.append(vec2(x, y))

        def need_to_move(self):
            current_position = self.rect.center
            return current_position[0] != self.target.x or current_position[1] != self.target.y

        def calculate_movement(self):
            if self.facing_direction != Direction.STATIONARY:

                current_position = vec2(self.rect.centerx, self.rect.centery)
                velocity = DIRECTIONS[self.facing_direction] * self.speed
                new_position = current_position + velocity
                target_position = self.target
                # Calculate velocity to just reach the target, not go over
                if (current_position.x < target_position.x < new_position.x or
                new_position.x < target_position.x < current_position.x):

                    velocity.x = target_position.x - current_position.x
                elif (current_position.y < target_position.y < new_position.y or
                new_position.y < target_position.y < current_position.y):

                    velocity.y = target_position.y - current_position.y

                return velocity
            else:
                return vec2(0, 0)


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

    # Sprite animation state
    start_frame = time.time()
    number_of_movement_images = 2
    fps = 5  # How fast sprite should be updated

    def __init__(self, x, y):
        # Get sprite sheet
        directory = os.path.dirname(__file__)
        sprite_sheet = pygame.image.load(os.path.join(directory, "player_sprite.png")).convert_alpha()

        self.sprites = self.get_player_sprites(sprite_sheet)

        self.image = self.sprites[self.facing_direction][-1]  # Select stationary image


        Entity.__init__(self, x, y, self.sprite_width * self.scale_factor, self.sprite_height * self.scale_factor)


    def get_player_sprites(self, sprite_sheet):
        """Creates a dict containing all player sprites with grouped by facing. Not generally applicable."""

        # Order of sprites' facings in sprite sheet
        sprite_sheet_direction = [Direction.DOWN, Direction.LEFT, Direction.RIGHT, Direction.UP]

        sprites = {}
        for i in range(0, 12, 3):
            direction_sprites = []
            scaled_sprite_size = (self.sprite_width * self.scale_factor, self.sprite_height * self.scale_factor)

            # Get all sprites with certain alignment
            sprite_move_1 = Rect(self.get_sprite_location(i), (self.sprite_width, self.sprite_height))
            sprite_stationary = Rect(self.get_sprite_location(i + 1), (self.sprite_width, self.sprite_height))
            sprite_move_2 = Rect(self.get_sprite_location(i + 2), (self.sprite_width, self.sprite_height))

            current_direction = sprite_sheet_direction[i // 3]

            # Current sprite sheet has duplicate sprites for left and right facing, thus reordering to allow animation
            if current_direction == Direction.RIGHT or current_direction == Direction.LEFT:
                direction_sprites = [scale(sprite_sheet.subsurface(rect), scaled_sprite_size) for rect in
                                     [sprite_move_1, sprite_stationary, sprite_move_2]]
            else:
                direction_sprites = [scale(sprite_sheet.subsurface(rect), scaled_sprite_size) for rect in
                                     [sprite_move_1, sprite_move_2, sprite_stationary]]

            # Add sprites to sprite dict with alignment as key
            sprites[sprite_sheet_direction[i // 3]] = direction_sprites

        return sprites

    # The top left corner coordinate of Nth sprite in a sprite sheet
    def get_sprite_location(self, index):
        x = (self.sprite_width + self.sprite_width_space) * (index % 3)
        y = (self.sprite_height + self.sprite_height_space) * (index // 3)
        return (x, y)

    def update(self):
        # print(self.need_to_move())
        if not self.need_to_move(self.target, self.facing_direction):
            # Stationary image
            self.image = self.sprites[self.facing_direction][-1]
            self.state = State.STATIONARY
        else:
            # Update image
            frame_index = int((time.time() - self.start_frame) * self.fps % self.number_of_movement_images)
            self.image = self.sprites[self.facing_direction][frame_index]

            new_velocity = self.calculate_movement(self.rect.center, self.target, DIRECTIONS[self.facing_direction],
                                                   self.velocity)

            self.rect = self.rect.move(*new_velocity)
