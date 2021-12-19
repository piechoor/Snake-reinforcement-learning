#TODO
#font
#repair self.score
#displaying score 27min


import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()

# Enumeration class
# because values are constant we use uppercase
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

# Object representing a point, implementation is done
# nametuple - it resembles simplified class implementation 
Point = namedtuple('Point', 'x, y')

# size of an elementary game block
BLOCK_SIZE = 20
# speed of the game, higher=faster
GAME_SPEED = 30
# colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE1 = (0,0,255)
BLUE2 = (0,0,200)

# Main class containing game loop
class SnakeGame:

    def __init__(self, w=640, h=480):
        # display dimentions
        self.w = w
        self.h = h

        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('snakin\'') # setting display caption
        self.clock = pygame.time.Clock() # setting game clock

        # initing game state (snake and food position, snake starting direction)
        self.direction = Direction.RIGHT

        # snake's head starts in the middle of a display
        self.head = Point(self.w/2, self.h/2)

        # snake's body - lists represents blocks that create the snake
        self.snake = [self.head,
                     Point(self.head.x-BLOCK_SIZE, self.head.y),
                     Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()

    # function places food in the game
    # // returns integer division value
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x, y)
        # checking if food is inside the snake
        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        # collecting user input

        # move the snake

        # checking if game ends

        # placing new food if one was eaten

        # updating ui and clock
        self._update_ui()
        self.clock.tick(GAME_SPEED)

        # returning game status and score
        game_over = False

        return game_over, self.score

    def _update_ui(self):
        self.display.fill(BLACK)

        for point in self.snake:
            pygame.draw.rect(self.display, BLUE1,
                        pygame.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, 
                        pygame.Rect(point.x+0.2*BLOCK_SIZE, 
                        point.y+0.2*BLOCK_SIZE, 0.6*BLOCK_SIZE, 0.6*BLOCK_SIZE))
        
        pygame.draw.rect(self.display, RED,
                    pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        # updating display to the screen
        pygame.display.flip()

if __name__ == '__main__':
    game = SnakeGame()

    #main game loop
    while True:
        game_over, score = game.play_step()

        #condition breaking loop when game is over
        if game_over == True:
            break
    
    print('Your final score is: ', score)

pygame.quit()