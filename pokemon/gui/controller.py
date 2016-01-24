import os
import sys
import time
from abc import ABCMeta, abstractmethod

import pygame
from pygame import Rect
from pygame.locals import (FULLSCREEN, K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, KEYDOWN, QUIT, K_k, K_p)
from pygame.math import Vector2
from pygame.sprite import Group
from pygame.time import Clock

import constants
from pokemon.game_logic.gameboard import GameBoard
from pokemon.game_logic.player import Player
from pokemon.game_logic.pokemon_character import Bulbasaur, Charmander, Squirtle
from pokemon.game_logic.square import Square
from pokemon.gui.camera import Camera, FollowFocusCamera
from pokemon.gui.constants import DIRECTIONS, GAMEBOARD, Direction, State
from pokemon.gui.event import ChangeMusic, MoveCamera, MovePlayer, PingPlayer, QuitEvent, TickEvent
from pokemon.gui.sprites import BackgroundEntity, CameraFocus, FrameEntity, PlayerSprite


class EventReceiver(metaclass=ABCMeta):
    """
    A superclass for receiving events from EventManager
    """
    @abstractmethod
    def notify(self, event):
        raise NotImplementedError


class ViewController(EventReceiver):
    """
    Handles updating the game and drawing of graphics.
    """

    # Size of one square on board in pixels
    board_rect_size = (186, 186)

    def __init__(self, evManager):
        self.__evManager = evManager
        self.__evManager.register_listener(self)

        pygame.init()

        self.window = pygame.display.set_mode((0, 0), FULLSCREEN)
        pygame.display.set_caption("Pokémon Drinking Game")
        self.background = pygame.Surface(self.window.get_size())
        self.frame = FrameEntity(0, 0)
        self.background.fill((0, 0, 0))

        self.window.blit(self.background, (0, 0))
        self.bg_ent = BackgroundEntity(0, 0)
        self.player_sprite = PlayerSprite(*self.from_game_coord_to_pixel(0, 8).center)
        self.entities = Group(self.player_sprite)

        self.camera = FollowFocusCamera(0, 0, self.bg_ent.image.get_size(), self.window.get_size())
        self.init_gameboard()
        pygame.display.flip()

    def notify(self, event):
        # CPU tick event
        if isinstance(event, TickEvent):
            self.update_game()
            self.entities.update()
            # Draw moving objects
            self.window.blit(self.bg_ent.image, self.camera.apply(self.bg_ent))

            # Draw stationary parts on top
            # TODO: Find way to keep stationary from unnecessary redrawing
            # self.window.blit(self.frame.image, (0, 0))
            for entity in self.entities:
                self.window.blit(entity.image, self.camera.apply(entity))
            pygame.display.update()

        # Camera events
        elif isinstance(event, MoveCamera):
            if event.direction == Direction.UP:
                self.camera.move_up()
            elif event.direction == Direction.DOWN:
                self.camera.move_down()
            elif event.direction == Direction.LEFT:
                self.camera.move_left()
            elif event.direction == Direction.RIGHT:
                self.camera.move_right()
            elif event.target is not None:
                self.camera.target(event.target)

        # Move player
        elif isinstance(event, MovePlayer):
            self.player.move_to_target(*event.target_coordinate)
            # self.player.rect = Rect(event.target_coordinate, self.player.rect.size)

    def init_gameboard(self):
        direction_dict = {
            "U": Direction.UP,
            "R": Direction.RIGHT,
            "D": Direction.DOWN,
            "L": Direction.LEFT,
            "N": Direction.STATIONARY
        }

        squares = []
        start, finish = Vector2(0, 0)

        for j in range(9):
            row = []
            for i in [i for i in range(9)]:
                cell = GAMEBOARD[j][i]
                if cell == "S":
                    start = Vector2(i, j)
                    row.append(Direction.UP)
                elif cell == "F":
                    finish = Vector2(i, j)
                    row.append(Direction.STATIONARY)
                else:
                    row.append(direction_dict[cell])

            squares.append(row)

        current_coordinate = start
        current_direction = squares[int(current_coordinate.y)][int(current_coordinate.x)]
        self.game_coordinates = {}
        self.board_squares = []
        index = 0
        while current_direction != Direction.STATIONARY and current_coordinate != finish:
            next_coordinate = current_coordinate + DIRECTIONS[current_direction]
            self.board_squares.append(Square("", index))
            self.game_coordinates[index] = current_coordinate
            current_coordinate = next_coordinate
            current_direction = squares[int(current_coordinate.y)][int(current_coordinate.x)]
            index += 1

        self.player = Player("", Charmander())
        self.players = [self.player]
        self.gameboard = GameBoard(self.board_squares, self.players)

    def update_game(self):
        if self.player_sprite.state != State.MOVING:
            current_square = self.gameboard[self.player]
            game_coordinate = self.game_coordinates[current_square.number + 1]
            target_coordinate = self.from_game_coord_to_pixel(*game_coordinate)

            self.gameboard[self.player] = self.board_squares[current_square.number + 1]
            self.player_sprite.move_to_target(*target_coordinate.center)

    def from_game_coord_to_pixel(self, x, y):
        return Rect((x * self.board_rect_size[1], y * self.board_rect_size[0]), self.board_rect_size)


class SoundController(EventReceiver):
    base = os.path.dirname(__file__)

    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.register_listener(self)
        self.mixer = pygame.mixer

        self.mixer.init()
        f = os.path.join(self.base, "pokemon_pallet_town.mp3")
        self.mixer.music.load(f)
        self.mixer.music.play(0)

    def notify(self, event):
        if isinstance(event, ChangeMusic):
            self.mixer.music.load(os.path.join(self.base, "pokemon_opening.mp3"))
            self.mixer.music.play(0)


class KeyboardController(EventReceiver):
    """
    Handles the keyboard control events.
    """
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.register_listener(self)

    def notify(self, event):
        if isinstance(event, TickEvent):
            for event in pygame.event.get():
                # Close with ESC or window close click
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    self.evManager.post_event(QuitEvent())
                    pygame.quit()
                    sys.exit()

            # Control with arrow keys
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[K_DOWN]:
                self.evManager.post_event(MoveCamera(Direction.DOWN))
            if keys_pressed[K_UP]:
                self.evManager.post_event(MoveCamera(Direction.UP))
            if keys_pressed[K_RIGHT]:
                self.evManager.post_event(MoveCamera(Direction.RIGHT))
            if keys_pressed[K_LEFT]:
                self.evManager.post_event(MoveCamera(Direction.LEFT))
            if (not keys_pressed[K_DOWN] and not keys_pressed[K_UP] and not keys_pressed[K_RIGHT] and
                    not keys_pressed[K_LEFT]):
                    self.evManager.post_event(MoveCamera(Direction.STATIONARY))
            if keys_pressed[K_p]:
                self.evManager.post_event(ChangeMusic())
            if keys_pressed[K_k]:
                self.evManager.post_event(PingPlayer())


class CPUController(EventReceiver):
    """
    Handles game engine ticks.
    """
    tick_rate = 60
    clock = Clock()

    def __init__(self, evManager):
        self.__evManager = evManager
        self.__evManager.register_listener(self)
        self.__keep_running = True

    def run(self):
        while self.__keep_running:
            self.__evManager.post_event(TickEvent())
            self.clock.tick(self.tick_rate)

    def notify(self, event):
        if isinstance(event, QuitEvent):
            self.__keep_running = False
