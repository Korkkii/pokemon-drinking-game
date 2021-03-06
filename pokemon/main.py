from pokemon.gui.event import EventManager
from pokemon.gui.controller import CPUController, KeyboardController, ViewController, SoundController
from pygame.locals import QUIT
import pygame
import sys

if __name__ == '__main__':
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
    view_control = ViewController(evManager)
    sound_control = SoundController(evManager)

    # Start game
    cpu_control.run()
