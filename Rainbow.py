import pygame, sys
from pygame.locals import *
pygame.init ()

window = pygame.display.set_mode ((640, 480))
pygame.display.set_caption ("Rainbow Colours")

while True:
    for event in pygame.event.get ():
        if event.type == QUIT:
            pygame.quit ()
            sys.exit ()

        if event.type == KEYDOWN:
            if event.key == K_1:
                window.fill ((255, 0, 0))
            elif event.key == K_2:
                window.fill ((255, 165, 0))
            elif event.key == K_3:
                window.fill ((255, 255, 0))
            elif event.key == K_4:
                window.fill ((0, 100, 0))
            elif event.key == K_5:
                window.fill ((0, 0, 255))
            elif event.key == K_6:
                window.fill ((148, 0, 211))

    pygame.display.update ()
