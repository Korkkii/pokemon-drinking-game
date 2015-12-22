from abc import abstractmethod, ABCMeta
import pygame
import sys
from event import QuitEvent, TickEvent
from pygame.locals import KEYDOWN, K_ESCAPE, QUIT


class EventReceiver(metaclass=ABCMeta):
    """
    A superclass for receiving events from EventManager
    """
    @abstractmethod
    def notify(self, event):
        raise NotImplementedError


# Example
class ViewController(EventReceiver):
    def notify(self, event):
        if isinstance(event, TickEvent):
            pygame.display.update()


class KeyboardController(EventReceiver):
    def __init__(self, evManager):
        self.__evManager = evManager

    def notify(self, event):
        if isinstance(event, TickEvent):
            for event in pygame.event.get():
                # Close with ESC or window close click
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    self.__evManager.post_event(QuitEvent())
                    pygame.quit()
                    sys.exit()


class CPUController(EventReceiver):
    def __init__(self, evManager):
        self.__evManager = evManager
        self.__keep_running = True

    def run(self):
        while self.__keep_running:
            self.__evManager.post_event(TickEvent())

    def notify(self, event):
        if isinstance(event, QuitEvent):
            self.__keep_running = False
