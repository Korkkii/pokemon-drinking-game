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
        self.image = pygame.image.load(os.path.join(directory, "assets/gameboard.png")).convert()
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
        """
        Sprite base class that implements movement on a gameboard.
        """
        # Sprite state
        speed = 5
        facing_direction = Direction.DOWN
        state = State.STATIONARY
        targets = deque()  # Target queue

        def __init__(self, x, y, width, height):
            super(MovingSprite, self).__init__(x, y, width, height)
            # Center the sprite to initial coords
            center_coords = (self.rect.centerx - self.rect.width, self.rect.centery - self.rect.height)
            self.rect = Rect(center_coords, self.rect.size)
            # Set current movement target equal to initial position
            self.target = vec2(self.rect.centerx, self.rect.centery)

        def move_to_target(self, x, y):
            """
            Add new target for the sprite to move towards. Starts movement towards target if stationary, otherwise
            appends the target to a queue.
            """
            # Set new direction
            new_target = vec2(x, y)

            if self.state == State.STATIONARY and new_target != self.target and not self.need_to_move():
                self.facing_direction = self.get_facing(x, y)
                self.state = State.MOVING
                self.target = vec2(x, y)
            else:
                self.targets.append(vec2(x, y))

        def get_facing(self, x, y):
            if x > self.target.x:
                return Direction.RIGHT
            elif x < self.target.x:
                return Direction.LEFT
            elif y > self.target.y:
                return Direction.DOWN
            elif y < self.target.y:
                return Direction.UP
            else:
                return Direction.STATIONARY

        def need_to_move(self):
            current_position = self.rect.center
            return current_position[0] != self.target.x or current_position[1] != self.target.y

        def calculate_movement(self):
            if self.state != State.STATIONARY:
                current_position = vec2(self.rect.centerx, self.rect.centery)
                velocity = DIRECTIONS[self.facing_direction] * self.speed
                new_position = current_position + velocity
                target_position = self.target
                print(current_position, velocity, new_position, target_position, self.targets)
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

        def move(self):
            """
            Move the sprite towards next target. Switches to a new target if targets queue is not empty, otherwise
            stays still.
            """
            # Check if already at current target
            if not self.need_to_move():
                # Get new target
                if len(self.targets) != 0:
                    next_target = self.targets.popleft()
                    facing = self.get_facing(*next_target)

                    # If new target is equal to previous
                    if facing == Direction.STATIONARY:
                        self.state = State.STATIONARY
                        return

                    self.facing_direction = facing
                    self.target = next_target
                # No target, stay still
                else:
                    self.state = State.STATIONARY
                    return
            if self.state != State.MOVING:
                self.state = State.MOVING

            velocity = self.calculate_movement()
            self.rect.move_ip(*velocity)


class PlayerSprite(MovingSprite):
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
    fps = 7  # How fast sprite should be updated

    def __init__(self, x, y):
        # Get sprite sheet
        directory = os.path.dirname(__file__)
        sprite_sheet = pygame.image.load(os.path.join(directory, "assets/player_sprite.png")).convert_alpha()

        self.sprites = self.get_player_sprites(sprite_sheet)

        self.image = self.sprites[self.facing_direction][-1]  # Select stationary image
        sprite_size = (self.sprite_width * self.scale_factor, self.sprite_height * self.scale_factor)
        super(PlayerSprite, self).__init__(x, y, *sprite_size)

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
        # Update movement state
        self.move()

        # Update image
        if self.state == State.STATIONARY:
            # Stationary image
            self.image = self.sprites[Direction.DOWN][-1]
        else:
            # Update image with respect to movement
            frame_index = int((time.time() - self.start_frame) * self.fps % self.number_of_movement_images)
            self.image = self.sprites[self.facing_direction][frame_index]
