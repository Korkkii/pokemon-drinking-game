from enum import Enum
from pygame.math import Vector2

"""
GUI constants and enumerations
"""


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
    STATIONARY = 5

DIRECTIONS = {
    Direction.UP: Vector2(0, -1),
    Direction.RIGHT: Vector2(1, 0),
    Direction.DOWN: Vector2(0, 1),
    Direction.LEFT: Vector2(-1, 0)
}
