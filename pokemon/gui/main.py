from event import EventManager
from controller import CPUController, KeyboardController, ViewController
from pygame.locals import QUIT
import pygame
import sys

if __name__ == '__main__':
    # PyGame window setup
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Hello World")

    # while True:
    #     for event in pygame.event.get():
    #         if event.type == QUIT:
    #             pygame.quit()
    #             sys.exit()
    #     pygame.display.update()

    # Game setup
    evManager = EventManager()

    kb_control = KeyboardController(evManager)
    cpu_control = CPUController(evManager)
    view_control = ViewController()
    evManager.register_listener(view_control)
    evManager.register_listener(cpu_control)
    evManager.register_listener(kb_control)

    # Start game
    cpu_control.run()
