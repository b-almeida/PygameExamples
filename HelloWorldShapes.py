import pygame, sys
from pygame.locals import *

# set up pygame
pygame.init()

# set up the window
windowSurface = pygame.display.set_mode((500, 400), 0, 32)
pygame.display.set_caption('Hello world!')

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 140, 0)

# set up fonts
basicFont = pygame.font.SysFont(None, 48)

# set up the text
text = basicFont.render('Hello world!', True, BLACK, GREEN)
textRect = text.get_rect()
textRect.bottom = windowSurface.get_rect ().bottom - 20
textRect.left = 20

# draw the white background onto the surface
windowSurface.fill(WHITE)

# draw a green polygon onto the surface
pygame.draw.polygon(windowSurface, GREEN, ((100, 0), (200, 50), (175, 150), (50, 150), (0, 50)))

# draw some blue lines onto the surface
pygame.draw.line(windowSurface, BLUE, (450, 0), (500, 50), 4)
pygame.draw.line(windowSurface, BLUE, (500, 0), (450, 50), 4)

# draw a blue circle onto the surface
pygame.draw.circle(windowSurface, RED, (460, 360), 40, 0)

# draw a red ellipse onto the surface
pygame.draw.ellipse(windowSurface, RED, (300, 250, 40, 80), 1)

# draw the text's background rectangle onto the surface
pygame.draw.rect(windowSurface, BLUE, (textRect.left - 20, textRect.top - 20, textRect.width + 40, textRect.height + 40))

# get a pixel array of the surface
pixArray = pygame.PixelArray(windowSurface)
pixArray[480][380] = BLACK
del pixArray

# draw the text onto the surface
windowSurface.blit(text, textRect)

# draw the pumpkin
pygame.draw.ellipse (windowSurface, ORANGE, pygame.Rect (200, 50, 240, 300) )
pygame.draw.polygon (windowSurface, BLACK, ( (320, 175), (300, 200), (340, 200) ) )
pygame.draw.circle (windowSurface, BLACK, (275, 125), 15)
pygame.draw.circle (windowSurface, BLACK, (365, 125), 15)
pygame.draw.lines (windowSurface, BLACK, False, ( (260, 250), (290, 300), (320, 250), (350, 300), (380, 250) ), 10)

# draw the window onto the screen
pygame.display.update()

# run the game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
