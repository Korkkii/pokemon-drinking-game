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


class State(Enum):
    STATIONARY = 0
    MOVING = 1


DIRECTIONS = {
    Direction.UP: Vector2(0, -1),
    Direction.RIGHT: Vector2(1, 0),
    Direction.DOWN: Vector2(0, 1),
    Direction.LEFT: Vector2(-1, 0)
}
GAMEBOARD = [
    ["R",  "R",  "R",  "R",  "R",  "GR", "R",  "R",  "D"],
    ["U",  "SR", "SR", "SR", "R",  "R",  "GR", "D",  "D"],
    ["GU", "SU", "R",  "R",  "R",  "GR", "D",  "D",  "D"],
    ["U",  "SU", "U",  "N",  "N",  "N",  "D",  "D",  "GD"],
    ["U",  "U",  "GU", "N",  "N",  "N",  "D",  "D",  "D"],
    ["U",  "U",  "U",  "N",  "N",  "N",  "D",  "SD", "D"],
    ["U",  "U",  "U",  "F",  "GL", "GL", "GL", "SD", "D"],
    ["U",  "GU", "U",  "L",  "L",  "GL", "SL", "SL", "SD"],
    ["S",  "U",  "L",  "L",  "L",  "SL", "SL", "SL", "SL"]
]
