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
from pokemon.game_logic.game import Game
from pokemon.game_logic.gameboard import GameBoard
from pokemon.game_logic.player import Player
from pokemon.game_logic.pokemon_character import Bulbasaur, Charmander, Squirtle
from pokemon.gui.camera import Camera, FollowFocusCamera
from pokemon.gui.constants import DIRECTIONS, GAMEBOARD, Direction, State
from pokemon.gui.event import (ChangeMusic, MoveCamera, PlayerMoved, PlayersFought, QuitEvent, TickEvent, PlayTurn,
                               OtherPlayersRequired, OtherPlayers)
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
    board_rect_space = (2, 2)
    board_frame = (4, 4)

    def __init__(self, evManager):
        self.__evManager = evManager
        self.__evManager.register_listener(self)

        # Initialize window
        pygame.init()
        self.window = pygame.display.set_mode((0, 0), FULLSCREEN)
        pygame.display.set_caption("Pokémon Drinking Game")

        # Initialize game
        self.entities = Group()
        self.init_game()

        self.background = pygame.Surface(self.window.get_size())
        self.background.fill((0, 0, 0))

        self.window.blit(self.background, (0, 0))
        self.bg_ent = BackgroundEntity(0, 0)

        self.camera = FollowFocusCamera(0, 0, self.bg_ent.image.get_size(), self.window.get_size())
        pygame.display.flip()

    def notify(self, event):
        # CPU tick event
        if isinstance(event, TickEvent):
            self.entities.update()
            # Draw moving objects
            self.window.blit(self.bg_ent.image, self.camera.apply(self.bg_ent))
            # for j in range(0, 9):
            #     for i in range(0, 9):
            #         if ((9 * j + i) < 70):
            #             loc = self.from_game_coord_to_pixel(9 * j + i)
            #             pygame.draw.rect(self.window, pygame.Color(255, 0, 0, 0), Rect(loc, self.board_rect_size), 1)

            # Draw stationary parts on top
            # TODO: Find way to keep stationary from unnecessary redrawing
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
        elif isinstance(event, PlayTurn):
            self.update_game()
        # Move player
        elif isinstance(event, PlayerMoved):
            movement_targets = [self.from_game_coord_to_pixel(square_num) for square_num in range(event.from_square + 1,
                                                                                                  event.to_square + 1)]
            player_sprite = self.player_sprites[event.player]
            for target in movement_targets:
                player_sprite.move_to_target(*target)
        elif isinstance(event, PlayersFought):
            results = event.results
            for result in results:
                print(result)
        elif isinstance(event, OtherPlayersRequired):
            required = [player for player in self.players if player != self.game.current_player]
            self.__evManager.post_event(OtherPlayers(required[0:event.players_required], event.square_num))

            # self.player_sprites[event.player].move_to_target(*target_coordinate)
            # self.player.rect = Rect(event.target_coordinate, self.player.rect.size)

    def init_game(self):
        self.players = [Player("tester1", Charmander()), Player("tester2", Bulbasaur()), Player("tester3", Squirtle())]
        self.game = Game(self.players, self.__evManager)
        self.player_sprites = {}

        for player in self.players:
            player_coordinates = self.from_game_coord_to_pixel(self.game.get_player_square(player).number)
            sprite = PlayerSprite(*player_coordinates)
            self.entities.add(sprite)
            self.player_sprites[player] = sprite

    def update_game(self):
        self.game.play_next_turn()

    def from_game_coord_to_pixel(self, square_num):
        w, h = self.board_rect_size
        x, y = self.game.game_coordinates[square_num]
        return (self.board_frame[0] + (x + 0.5) * (w + self.board_rect_space[0]),
                self.board_frame[1] + (y + 0.5) * (h + self.board_rect_space[1]))
        # return ((x + 0.5) * w, (y + 0.5) * h)


class SoundController(EventReceiver):
    base = os.path.dirname(__file__)

    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.register_listener(self)
        self.mixer = pygame.mixer

        self.mixer.init()
        f = os.path.join(self.base, "assets/pokemon_pallet_town.mp3")
        self.mixer.music.load(f)
        # self.mixer.music.play(0)

    def notify(self, event):
        if isinstance(event, ChangeMusic):
            self.mixer.music.load(os.path.join(self.base, "assets/pokemon_opening.mp3"))
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
                elif event.type == KEYDOWN and event.key == K_k:
                    self.evManager.post_event(PlayTurn())

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
            if keys_pressed[K_p]:
                self.evManager.post_event(ChangeMusic())
            pygame.event.pump()


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
