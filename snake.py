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

# Main class containing game loop
class SnakeGame:

    def __init___(self, w=640, h=480):
        # display dimentions
        self.w = w
        self.h = h

        # init display
        self.display = pygame.display.set_model((self.w, self.h))
        pygame.display.set_caption('snakin\'') # setting display caption
        self.clock = pygame.time.Clock() # setting speed game control

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
        x = random.randomint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randomint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
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

        # returning game status and score
        game_over = False

        self.score = 0
        return game_over, self.score

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