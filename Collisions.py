# Import modules
import pygame
from math import radians, sin, cos, asin, acos
from random import randint
from pygame.locals import *
pygame.init ()

# Create constants
WINDOWSIZE = (800, 600)

# Create window
window = pygame.display.set_mode (WINDOWSIZE, 0, 32)
pygame.display.set_caption ("Introduction to Pygame")




class Colour (object):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)




class Sound (object):
    isOn = True
    pygame.mixer.music.load ("bg_music.mp3")
    bounce = pygame.mixer.Sound ("funny-bounce.wav")




class Angle (object):
    @staticmethod
    def format (a):
        '''in - (angle)
        Formats angle to a number from 0 to 359.
        out - formatted angle (int/float)'''
        while a < 0:
            a += 360
        while a >= 360:
            a -= 360
        return a

    @staticmethod
    def opposite (a, n):
        '''in - (angle, normal)
        Calculates the opposite (reflected) angle of the given angle to the given normal.
        out - opposite angle (int/float)'''
        return Angle.format (2 * n - a)        # n - (a - n)




class Circle (object):
    def __init__ (self, center, radius):
        '''in - (self, center point, radius)'''
        self.center = center
        self.radius = radius

    @staticmethod
    def getCircle (rect):
        '''in - (Rect)
        Returns a Circle object of the given Rect.
        out - Circle'''
        return Circle (rect.center, (rect.width + rect.height) / 4)

    def collide (self, c2):
        '''in - (self, other circle)
        Determines if the 2 circles are in collision.
        out - bool'''
        distance_x = abs (self.center [0] - c2.center [0])
        distance_y = abs (self.center [1] - c2.center [1])
        distance_z = (distance_x ** 2 + distance_y ** 2) ** 0.5
        if distance_z < (self.radius + c2.radius):
            return True
        return False
    


    
class Wall (object):
    SIZE = 10

    def __init__ (self, position, size, normal):
        '''in - (self, position (x, y), size (x, y), normal (angle))'''
        self.rect = pygame.Rect (position, size)
        self.normal = normal

    @staticmethod
    def createList ():
        '''Creates list of walls.
        out - list of walls'''
        walls = []
        walls.append (Wall ( (0, 0), (WINDOWSIZE [0],  Wall.SIZE), 180) )      # top
        walls.append (Wall ( (0, WINDOWSIZE [1] - Wall.SIZE), (WINDOWSIZE [0], Wall.SIZE), 0) )     # bottom
        walls.append (Wall ( (0, 0), (Wall.SIZE, WINDOWSIZE [1]), 270) )       # left
        walls.append (Wall ( (WINDOWSIZE [0] - Wall.SIZE, 0), (Wall.SIZE, WINDOWSIZE [1]), 90) )     # right
        return walls




class Obstacle (Rect):
    SIZE = 100
    NUMBER = 4

    def __init__ (self, left, top):
        Rect.__init__ (self, left, top, Obstacle.SIZE, Obstacle.SIZE)

    @staticmethod
    def createList ():
        '''Creates list of obstacles.
        out - list of obstacles'''
        obstacles = []
        obstacles.append (Obstacle (200, 125) )
        obstacles.append (Obstacle (500, 125) )
        obstacles.append (Obstacle (200, 375) )
        obstacles.append (Obstacle (500, 375) )
        return obstacles

    def getWalls (self):
        '''Creates list of walls from an obstacle.
        out - list of walls'''
        walls = []
        walls.append (Wall (self.topleft, (self.width, 1), 180) )
        walls.append (Wall (self.bottomleft, (self.width, 1), 0) )
        walls.append (Wall (self.topleft, (1, self.height), 270) )
        walls.append (Wall (self.topright, (1, self.height), 90) )
        return walls
        



class Block (object):
    SIZE = 20
    NUMBER = 50

    @staticmethod
    def createList (obstacles):
        '''Creates list of blocks.
        out - blocks (list of Rects)'''
        blocks = []
        for i in range (Block.NUMBER):
            blocks.append (pygame.Rect (randint (Wall.SIZE, WINDOWSIZE [0] - Wall.SIZE - Block.SIZE), \
                randint (Wall.SIZE, WINDOWSIZE [1] - Wall.SIZE - Block.SIZE), Block.SIZE, Block.SIZE))

            # Create list of all balls, walls, and blocks
            rectList = []
            for o in obstacles:
                rectList.append (o)
            if len (blocks) >= 2:
                for b in blocks [:-1]:
                    rectList.append (b)

            # Check if block is colliding with another object, and modify its position if necessary
            while True:
                for r in rectList:
                    if r.colliderect (blocks [-1]):       
                        blocks [-1].left = randint (Wall.SIZE, WINDOWSIZE [0] - Wall.SIZE - Block.SIZE)
                        blocks [-1].top = randint (Wall.SIZE, WINDOWSIZE [1] - Wall.SIZE - Block.SIZE)
                        break
                else:
                    break

        return blocks

    @staticmethod
    def update (blocks, balls):
        '''in - (list of blocks, list of balls)
        Checks if any blocks collided with a ball, and deletes them if necessary.'''
        for ba in balls:
            delete = []
            for i, bl in enumerate (blocks [:]):
                if bl.colliderect (ba.rect):
                    delete.append (i)
            for i in delete [::-1]:
                del blocks [i]




class Ball (object):
    SIZE = 50
    SPEED = (1, 1)
    
    def __init__ (self, obstacles, blocks, balls):
        '''in - (self, list of obstacles, list of blocks, list of balls)'''
        self.rect = pygame.Rect (randint (Wall.SIZE, WINDOWSIZE [0] - Wall.SIZE - Ball.SIZE), \
            randint (Wall.SIZE, WINDOWSIZE [1] - Wall.SIZE - Ball.SIZE), Ball.SIZE, Ball.SIZE)
        self.speed = randint (*Ball.SPEED)
        self.direction = randint (0, 359)        # angle
        self.collidedwith_walls = []
        self.collidedwith_balls = []
        
        # Create list of all balls and blocks (Rects)
        rectList = []
        for o in obstacles:
            rectList.append (o)
        rectList += blocks
        for b in balls:
            rectList.append (b.rect)

        # Check if ball is colliding with another object, and modify its position if necessary
        while True:
            for r in rectList:
                if r.colliderect (self.rect):       
                    self.rect.left = randint (Wall.SIZE, WINDOWSIZE [0] - Wall.SIZE - Ball.SIZE)
                    self.rect.top = randint (Wall.SIZE, WINDOWSIZE [1] - Wall.SIZE - Ball.SIZE)
                    break
            else:
                break

    def getMoveVector (self):
        '''in - (self)
        Calculates (x, y) vector for movement using direction.
        out - (x, y) tuple of ints'''
        a = Angle.format (self.direction + 90)
        x = int (round (cos (radians (a)) * self.speed, 0))
        y = int (round (sin (radians (a)) * self.speed, 0))
        return (x, y)

    def getNewDirection (self, b2):
        '''in - (self, collision ball)
        Calculates and implements the ball's new direction after colliding with another ball.'''
        distance_x = abs (self.rect.center [0] - b2.rect.center [0])
        distance_y = abs (self.rect.center [1] - b2.rect.center [1])
        distance_z = float ((distance_x ** 2 + distance_y ** 2) ** 0.5)
        normal1 = acos (distance_x / distance_z)
        normal2 = asin (distance_y / distance_z)
        normal = int (round ((normal1 + normal2) / 2.0, 0))
        self.direction = Angle.format (Angle.opposite (Angle.format (self.direction - 180), normal))

    def update (self, walls, balls):
        '''in - (self, list of balls, list of walls)
        Moves ball, checks if it collided with a wall, and changes its direction if necessary.'''
        test = self.rect.move (*self.getMoveVector ())
        
        balls_copy = balls [:]
        try:
            del balls_copy [balls_copy.index (self)]
        except:
            pass

        # Determine how many walls ball collided with
        collidedwith_walls_old = self.collidedwith_walls
        
        oWalls = []
        for w in walls:
            if w.rect.colliderect (test):
                oWalls.append (w)
                self.collidedwith_walls.append (w)

        # Ball collided with multiple obstacles
        if len (oWalls) > 2:
            self.direction = Angle.format (self.direction - 180)
            if Sound.isOn:
                Sound.bounce.play ()

        # len (oWalls) == 1 or 2
        elif len (oWalls) != 0:
            # Ball collided with 2 walls
            if len (oWalls) == 2:
                angle0 = abs (Angle.format (self.direction - 180) - oWalls [0].normal)
                angle1 = abs (Angle.format (self.direction - 180) - oWalls [1].normal)
                if angle0 < angle1 and not self.rect.colliderect (oWalls [0]):
                    self.direction = Angle.opposite (Angle.format (self.direction - 180), oWalls [0].normal)
                elif angle1< angle0 and not self.rect.colliderect (oWalls [1]):
                    self.direction = Angle.opposite (Angle.format (self.direction - 180), oWalls [1].normal)
                else:
                    self.direction = Angle.format (self.direction - 180)

            # Ball collided with 1 wall
            else:
                self.direction = Angle.opposite (Angle.format (self.direction - 180), oWalls [0].normal)

            if Sound.isOn:
                Sound.bounce.play ()
                    
        self.rect.move_ip (*self.getMoveVector ())


        for w in self.collidedwith_walls [:]:
            if not (self.rect.colliderect (w) ):
                del self.collidedwith_walls [self.collidedwith_walls.index (w) ]


        # Determine if ball collided with another ball
        collidedwith_balls_old = self.collidedwith_balls
        
        circle = Circle.getCircle (test)
        for b in balls_copy:
            c2 = Circle.getCircle (b.rect)
            if circle.collide (c2):
                if balls.index (b) not in collidedwith_balls_old:
                    self.collidedwith_balls.append (balls.index (b) )
                    self.getNewDirection (b)
                
        for b in self.collidedwith_balls [:]:
            if not (self.rect.colliderect (balls [b].rect) ):
                del self.collidedwith_balls [self.collidedwith_balls.index (b) ]



# Create game objects
walls = Wall.createList ()
obstacles = Obstacle.createList ()
for o in obstacles:
    walls += o.getWalls ()
blocks = Block.createList (obstacles)
balls = []
for i in range (6):
    balls.append (Ball (obstacles, blocks, balls) )

# Play background music
if Sound.isOn:
    pygame.mixer.music.set_volume (0.5)
    pygame.mixer.music.play (-1, 0.0)

# Game loop
keepGoing = True
while keepGoing:
    # Event handling
    for event in pygame.event.get ():
        # Quit
        if event.type == QUIT:
            keepGoing = False

        # Check if speed mod keys are being pressed
        if event.type == KEYDOWN:
            if event.key == K_UP:
                for b in balls:
                    b.speed += 1
            if event.key == K_DOWN:
                for b in balls:
                    if b.speed >= 2:
                        b.speed -= 1

    # Update balls
    balls_old = balls [:]
    for b in balls:
        b.update (walls, balls_old [:])

    # Update blocks
    Block.update (blocks, balls)

    # Draw screen
    window.fill ((Colour.WHITE))
    for w in walls:
        pygame.draw.rect (window, Colour.BLACK, w)
    for o in obstacles:
        pygame.draw.rect (window, Colour.BLACK, o)
    for b in blocks:
        pygame.draw.rect (window, Colour.GREEN, b)
    for b in balls:
        pygame.draw.circle (window, Colour.BLUE, b.rect.center, Ball.SIZE / 2)
    pygame.display.update ()

    if len (blocks) == 0:
        keepGoing = False


# Quit
pygame.mixer.music.stop ()
pygame.quit ()
