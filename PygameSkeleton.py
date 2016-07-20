import pygame
from pygame.locals import *
pygame.init ()

WINDOWSIZE = (640, 480)

window = pygame.display.set_mode (WINDOWSIZE, 0, 32)
pygame.display.set_caption ("Pygame")

keepGoing = True
while keepGoing:
    for event in pygame.event.get ():
        if event.type == QUIT:
            keepGoing = False

    # Your main loop code here

    pygame.display.update ()
