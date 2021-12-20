#TODO
#font
#displaying score 27min
#pip08

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

BLOCK_SIZE = 25 # size of an elementary game block
GAME_SPEED = 10 #speed of the game, higher=faster
# colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
OUT_SNAKE = (0,200,0)
IN_SNAKE = (0,150,0)
FOOD_COL = RED
# display dimentions (in blocks)
BLOCK_W = 32
BLOCK_H = 32

# Main class containing game loop
class SnakeGame:

    def __init__(self, w=BLOCK_W*BLOCK_SIZE, h=BLOCK_H*BLOCK_SIZE):
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

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit() # exiting game
                quit() # exiting programm
            elif event.type == pygame.KEYDOWN:
                if event.key == (pygame.K_LEFT or event.key == pygame.K_a) and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == (pygame.K_UP or event.key == pygame.K_w) and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == (pygame.K_RIGHT or event.key == pygame.K_d) and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == (pygame.K_DOWN or event.key == pygame.K_s) and self.direction != Direction.UP:
                    self.direction = Direction.DOWN

        # move the snake

        self._move(self.direction)
        # inserting new head to snake's elements list
        self.snake.insert(0, self.head)

        # checking if theres a collision with snake or boundary game ends
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # placing new food if one was eaten
        if self.head == self.food:
            # if snake ate a food nothing changes in snake
            self.score += 1
            self._place_food()
        else:
            # if snake didnt eat, the last part of snake is taken
            self.snake.pop()

        # updating ui and clock
        self._update_ui()
        self.clock.tick(GAME_SPEED)

        # returning game status and score
        return game_over, self.score

    def _is_collision(self):
        # hitting boundry 
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # hitting itself
        if self.head in self.snake[1:]:
            return True

        #no collision
        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        for point in self.snake:
            pygame.draw.rect(self.display, OUT_SNAKE,
                        pygame.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, IN_SNAKE, 
                        pygame.Rect(point.x+0.2*BLOCK_SIZE, 
                        point.y+0.2*BLOCK_SIZE, 0.6*BLOCK_SIZE, 0.6*BLOCK_SIZE))
        
        pygame.draw.rect(self.display, FOOD_COL,
                    pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        # updating display to the screen
        pygame.display.flip()

    def _move(self, direction):
        # extracting coordinates
        x = self.head.x
        y = self.head.y
        # moving snake by blocksize
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE

        # updating head position
        self.head = Point(x, y)

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