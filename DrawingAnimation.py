import pygame, sys
from pygame.locals import *
pygame.init ()

def terminate ():
    pygame.quit ()
    sys.exit ()

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
MOVESPEED = 5
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

blitLocation = [0, 0]
moveUp = moveDown = moveLeft = moveRight = False

window = pygame.display.set_mode ((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption ("Drawing Movement")

drawing = pygame.Surface ((WINDOWWIDTH, WINDOWHEIGHT)).convert ()
pygame.draw.rect (drawing, RED, pygame.Rect (200, 200, 400, 300))
pygame.draw.circle (drawing, GREEN, (500, 250), 100)
pygame.draw.line (drawing, BLUE, (300, 50), (700, 475), 10)

while True:
    for event in pygame.event.get ():
        if event.type == QUIT:
            terminate ()

        if event.type == KEYDOWN:
            if event.key == K_UP:
                moveUp = True
                moveDown = False
            elif event.key == K_DOWN:
                moveDown = True
                moveUp = False
            elif event.key == K_LEFT:
                moveLeft = True
                moveRight = False
            elif event.key == K_RIGHT:
                moveRight = True
                moveLeft = False

        if event.type == KEYUP:
            if event.key == K_UP:
                moveUp = False
            elif event.key == K_DOWN:
                moveDown = False
            elif event.key == K_LEFT:
                moveLeft = False
            elif event.key == K_RIGHT:
                moveRight = False

    if moveUp:
        blitLocation [1] -= 5
    elif moveDown:
        blitLocation [1] += 5
    if moveLeft:
        blitLocation [0] -= 5
    elif moveRight:
        blitLocation [0] += 5

    window.blit (drawing, tuple (blitLocation))
        
    pygame.display.update ()
