#TODO
#font
#displaying score 27min
#pip08

import pygame
import random

from const import *
from obstacles import *
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

# Main class containing game loop
class SnakeGame:

    def __init__(self, w=BLOCK_W*BLOCK_SIZE, h=BLOCK_H*BLOCK_SIZE):
        # display dimentions
        self.w = w
        self.h = h

        # init display /with a one block buffor
        self.display = pygame.display.set_mode((self.w+DIS_BUFF, self.h+DIS_BUFF))
        pygame.display.set_caption('snakin\'') # setting display caption
        self.clock = pygame.time.Clock() # setting game clock

        # initing game state (snake and food position, snake starting direction)
        self.direction = Direction.RIGHT

        # snake's head starts in the middle of a display
        self.head = Point((self.w/2)//BLOCK_SIZE*BLOCK_SIZE, (self.h/10)//BLOCK_SIZE*BLOCK_SIZE)

        # snake's body - lists represents blocks that create the snake
        self.snake = [self.head,
                     Point(self.head.x-BLOCK_SIZE, self.head.y),
                     Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        if OBSTACLES == True:
            # defining obstacle map
            self.obst = init_obst_map(self.w, self.h)

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

        # checking if food is inside an obstacle
        if OBSTACLES == True:
            if self.food in self.obst:
                self._place_food()
    
    def _set_map(self):

        for ob in self.obst:
            pygame.draw.rect(self.display, YELLOW,
                        pygame.Rect(ob.x, ob.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, ORANGE, 
                        pygame.Rect(ob.x+0.2*BLOCK_SIZE, 
                        ob.y+0.2*BLOCK_SIZE, 0.6*BLOCK_SIZE, 0.6*BLOCK_SIZE))

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
            # gotta break, otherwise takes more actions and can create 
            # changing fg left to right (hitting neck with head)
            #break

        # move the snake

        if self.head.x > self.w:
            self.head = Point(0,self.head.y)
        if self.head.x < 0:
            self.head = Point(self.w,self.head.y)
        if self.head.y > self.h:
            self.head = Point(self.head.x,0)
        if self.head.y < 0:
            self.head = Point(self.head.x,self.h)

        self._move(self.direction)
        # inserting new head to snake's elements list
        self.snake.insert(0, self.head)

        # placing new food if one was eaten
        if self.head == self.food:
            # if snake ate a food nothing changes in snake
            self.score += 1
            self._place_food()
        else:
            # if snake didnt eat, the last part of snake is taken
            self.snake.pop()

        # checking if theres a collision with snake or boundary game ends
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # updating ui and clock
        self._update_ui()
        self.clock.tick(GAME_SPEED)

        # returning game status and score
        return game_over, self.score

    def _is_collision(self):

        if OBSTACLES == True:
            # hitting obstacle
            if self.head in self.obst[:]:
                return True
        else:
            # hitting boundry
            if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
                return True
        
        #hitting itself
        if self.head in self.snake[1:]:
            print(self.head, self.snake)
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
        
        if OBSTACLES == True:
            # setting obstacles
            self._set_map()

        # updating display to the screen
        pygame.display.flip()

    def _move(self, direction):
        # extracting coordinates
        x = self.head.x
        y = self.head.y
        # moving snake by blocksize
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
            print('RIGHT')
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
            print('LEFT')
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
            print('UP')
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
            print('DOWN')

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