import pygame, sys, time
from pygame.locals import *

# set up pygame
pygame.init()

# set up the window
WINDOWWIDTH = 400
WINDOWHEIGHT = 400
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Animation')

# set up direction variables
LEFT = 0
DOWNLEFT = 1
RIGHT = 2
DOWNRIGHT = 3
UPLEFT = 7
UPRIGHT = 9

MOVESPEED = 4
YELLOWSPEED = 2

# set up the colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# set up the block data structure
b1 = {'rect':pygame.Rect(300, 80, 50, 100), 'color':RED, 'dir':UPRIGHT}
b2 = {'rect':pygame.Rect(200, 200, 20, 20), 'color':GREEN, 'dir':UPLEFT}
b3 = {'rect':pygame.Rect(100, 150, 60, 60), 'color':BLUE, 'dir':DOWNLEFT}
blocks = [b1, b2, b3]
by = {'rect':pygame.Rect(170, 170, 60, 60), 'color':YELLOW, 'dir':LEFT}

# run the game loop
while True:
    # check for the QUIT event
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == KEYDOWN:
            if event.key == K_UP:
                MOVESPEED += 1
            elif event.key == K_DOWN:
                MOVESPEED -= 1

    # draw the black background onto the surface
    windowSurface.fill(BLACK)

    if by ["dir"] == LEFT:
        by ["rect"].left -= YELLOWSPEED
    elif by ["dir"] == RIGHT:
        by ["rect"].left += YELLOWSPEED

    if by ["rect"].left < 0:
        by ["dir"] = RIGHT
    elif by ["rect"].left > WINDOWWIDTH:
        by ["dir"] = LEFT

    pygame.draw.rect (windowSurface, by ["color"], by ["rect"])

    for b in blocks:
        # move the block data structure
        if b['dir'] == DOWNLEFT:
            b['rect'].left -= MOVESPEED
            b['rect'].top += MOVESPEED
        if b['dir'] == DOWNRIGHT:
            b['rect'].left += MOVESPEED
            b['rect'].top += MOVESPEED
        if b['dir'] == UPLEFT:
            b['rect'].left -= MOVESPEED
            b['rect'].top -= MOVESPEED
        if b['dir'] == UPRIGHT:
            b['rect'].left += MOVESPEED
            b['rect'].top -= MOVESPEED

        # check if the block has move out of the window
        if b['rect'].top < 0:
            # block has moved past the top
            if b['dir'] == UPLEFT:
                b['dir'] = DOWNLEFT
            if b['dir'] == UPRIGHT:
                b['dir'] = DOWNRIGHT
        if b['rect'].bottom > WINDOWHEIGHT:
            # block has moved past the bottom
            if b['dir'] == DOWNLEFT:
                b['dir'] = UPLEFT
            if b['dir'] == DOWNRIGHT:
                b['dir'] = UPRIGHT
        if b['rect'].left < 0:
            # block has moved past the left side
            if b['dir'] == DOWNLEFT:
                b['dir'] = DOWNRIGHT
            if b['dir'] == UPLEFT:
                b['dir'] = UPRIGHT
        if b['rect'].right > WINDOWWIDTH:
            # block has moved past the right side
            if b['dir'] == DOWNRIGHT:
                b['dir'] = DOWNLEFT
            if b['dir'] == UPRIGHT:
                b['dir'] = UPLEFT

        # draw the block onto the surface
        pygame.draw.rect(windowSurface, b['color'], b['rect'])

    for i, b in enumerate (blocks [:]):
        if b ["rect"].colliderect (by ["rect"]):
            del blocks [i]

    if len (blocks) == 0:
        pygame.event.post (pygame.event.Event (QUIT))

    # draw the window onto the screen
    pygame.display.update()
    time.sleep(0.02)
