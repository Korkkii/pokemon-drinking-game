from abc import abstractmethod, ABCMeta
import pygame
import sys
from event import QuitEvent, TickEvent, MoveCamera, Direction
from pygame.locals import KEYDOWN, K_ESCAPE, QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT
import os
from camera import Camera, FollowFocusCamera
from pygame.sprite import Group
from sprites import BackgroundEntity, CameraFocus


class EventReceiver(metaclass=ABCMeta):
    """
    A superclass for receiving events from EventManager
    """
    @abstractmethod
    def notify(self, event):
        raise NotImplementedError


class ViewController(EventReceiver):
    def __init__(self, evManager):
        self.__evManager = evManager
        self.__evManager.register_listener(self)

        pygame.init()
        self.window = pygame.display.set_mode((400, 300))
        pygame.display.set_caption("Pokémon Drinking Game")
        self.background = pygame.Surface(self.window.get_size())
        self.background.fill((0, 0, 0))
        # directory = os.path.dirname(__file__)
        # self.background_image = pygame.image.load(os.path.join(directory, "pokemon_drink.png"))
        self.window.blit(self.background, (0, 0))
        self.entities = Group(BackgroundEntity(0, 0))

        self.camera = FollowFocusCamera(300, 200, self.window.get_size())
        self.camera_focus = CameraFocus(0, 0)

        pygame.display.flip()

    def notify(self, event):
        if isinstance(event, TickEvent):
            self.camera.update(self.camera_focus)

            for entity in self.entities:
                self.window.blit(entity.image, self.camera.apply(entity))

            pygame.display.flip()
        elif isinstance(event, MoveCamera):
            if event.direction == Direction.DOWN:
                self.camera_focus.rect.move_ip(0, 30)
            elif event.direction == Direction.RIGHT:
                self.camera_focus.rect.move_ip(30, 0)
            elif event.direction == Direction.UP:
                self.camera_focus.rect.move_ip(0, -30)
            elif event.direction == Direction.LEFT:
                self.camera_focus.rect.move_ip(-30, 0)


class KeyboardController(EventReceiver):
    def __init__(self, evManager):
        self.__evManager = evManager
        self.__evManager.register_listener(self)

    def notify(self, event):
        if isinstance(event, TickEvent):
            for event in pygame.event.get():
                # Close with ESC or window close click
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    self.__evManager.post_event(QuitEvent())
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        self.__evManager.post_event(MoveCamera(Direction.DOWN))
                    elif event.key == K_UP:
                        self.__evManager.post_event(MoveCamera(Direction.UP))
                    elif event.key == K_RIGHT:
                        self.__evManager.post_event(MoveCamera(Direction.RIGHT))
                    elif event.key == K_LEFT:
                        self.__evManager.post_event(MoveCamera(Direction.LEFT))


class CPUController(EventReceiver):
    def __init__(self, evManager):
        self.__evManager = evManager
        self.__evManager.register_listener(self)
        self.__keep_running = True

    def run(self):
        while self.__keep_running:
            self.__evManager.post_event(TickEvent())

    def notify(self, event):
        if isinstance(event, QuitEvent):
            self.__keep_running = False
