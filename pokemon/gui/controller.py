from abc import abstractmethod, ABCMeta
import pygame
import sys
from event import QuitEvent, TickEvent, MoveCamera, ChangeMusic
from constants import Direction
from pygame.locals import KEYDOWN, K_ESCAPE, QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT, K_p, FULLSCREEN
import os
from camera import Camera, FollowFocusCamera
from pygame.sprite import Group
from sprites import BackgroundEntity, CameraFocus, FrameEntity, PlayerSprite
from pygame.time import Clock


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
        self.player = PlayerSprite(0, 0)
        self.entities = Group(self.player)

        self.camera = FollowFocusCamera(0, 0, self.bg_ent.image.get_size(), self.window.get_size())

        pygame.display.flip()

    def notify(self, event):
        # CPU tick event
        if isinstance(event, TickEvent):
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
                # self.player.facing_direction = Direction.UP
                # self.player.moving = True
                self.camera.move_up()
            elif event.direction == Direction.DOWN:
                # self.player.facing_direction = Direction.DOWN
                # self.player.moving = True
                self.camera.move_down()
            elif event.direction == Direction.LEFT:
                # self.player.facing_direction = Direction.LEFT
                # self.player.moving = True
                self.camera.move_left()
            elif event.direction == Direction.RIGHT:
                # self.player.facing_direction = Direction.RIGHT
                # self.player.moving = True
                self.camera.move_right()
            # elif event.direction == Direction.STATIONARY:
                # self.player.facing_direction = Direction.DOWN
                # self.player.moving = False
            # self.entities.update()


class SoundController(EventReceiver):
    base = os.path.dirname(__file__)

    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.register_listener(self)
        self.mixer = pygame.mixer

        self.mixer.init()
        f = os.path.join(self.base, "pokemon_opening.mp3")
        self.mixer.music.load(f)
        self.mixer.music.play(0)

    def notify(self, event):
        if isinstance(event, ChangeMusic):
            self.mixer.music.load(os.path.join(self.base, "pokemon_pallet_town.mp3"))
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
