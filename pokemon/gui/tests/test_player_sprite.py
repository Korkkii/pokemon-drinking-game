from unittest import TestCase

import pygame
from pygame.math import Vector2

from pokemon.gui.constants import Direction, DIRECTIONS, State
from pokemon.gui.sprites import MovingSprite


class PlayerSpriteTest(TestCase):
    def setUp(self):
        self.sprite = MovingSprite(50, 50, 10, 10)

    def test_move_to_target_no_change_in_state(self):
        self.sprite.move_to_target(50, 50)

        self.assertEqual(self.sprite.state, State.STATIONARY)

    def test_move_to_target_change_in_state(self):
        directions = [(Direction.RIGHT, Vector2(10, 0)), (Direction.LEFT, Vector2(-10, 0)),
                      (Direction.UP, Vector2(0, -10)), (Direction.DOWN, Vector2(0, 10))]
        for direction, vector in directions:
            self.sprite = MovingSprite(50, 50, 10, 10)
            self.sprite.move_to_target(self.sprite.rect.centerx + vector.x, self.sprite.rect.centery + vector.y)

            self.assertEqual(self.sprite.state, State.MOVING)
            self.assertEqual(self.sprite.facing_direction, direction)

    def test_no_need_to_move(self):
        self.assertFalse(self.sprite.need_to_move())

    def test_needs_to_move_towards_target(self):
        directions = [Vector2(10, 0), Vector2(-10, 0), Vector2(0, -10), Vector2(0, 10)]
        for vector in directions:
            self.sprite.move_to_target(self.sprite.rect.centerx + vector.x, self.sprite.rect.centery + vector.y)

            self.assertTrue(self.sprite.need_to_move())

    def test_calculate_movement_no_movement(self):
        """No movement if stationary"""
        self.assertEqual(self.sprite.calculate_movement(), Vector2(0, 0))

    def test_calculate_movement_move_whole_velocity(self):
        directions = [Vector2(20, 0), Vector2(-20, 0), Vector2(0, -20), Vector2(0, 20)]
        for direction in directions:
            self.sprite = MovingSprite(50, 50, 10, 10)
            self.sprite.move_to_target(self.sprite.rect.centerx + direction.x, self.sprite.rect.centery + direction.y)

            self.assertEqual(self.sprite.calculate_movement(), direction / 2)

    def test_calculate_movement_move_partial_amount(self):
        directions = [Vector2(3, 0), Vector2(-3, 0), Vector2(0, -3), Vector2(0, 3)]
        for direction in directions:
            self.sprite = MovingSprite(50, 50, 10, 10)
            self.sprite.move_to_target(self.sprite.rect.centerx + direction.x, self.sprite.rect.centery + direction.y)

            self.assertEqual(self.sprite.calculate_movement(), direction)
