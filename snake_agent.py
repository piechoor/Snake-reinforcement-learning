#TODO
#font
#displaying score 27min
#pip08

import pygame
import random
import numpy as np

from constants import *
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
        self.reset_game()

    def reset_game(self):
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

        # iteration of the game 
        self.frame_iteration = 0

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

    def play_step(self, action):
        # increasing game frame
        self.frame_iteration += 1

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
        # checking if snake hits boundry - if yes teleports
        # on the other side
        if self.head.x > self.w:
            self.head = Point(0,self.head.y)
        if self.head.x < 0:
            self.head = Point(self.w,self.head.y)
        if self.head.y > self.h:
            self.head = Point(self.head.x,0)
        if self.head.y < 0:
            self.head = Point(self.head.x,self.h)

        self._move(action)
        # inserting new head to snake's elements list
        self.snake.insert(0, self.head)

        # checking if theres a collision with snake or boundary game ends
        reward = 0
        game_over = False
        # if we collide or snake does nothing too long
        if self._is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = REW_DIE
            return reward, game_over, self.score

        # placing new food if one was eaten
        if self.head == self.food:
            # if snake ate a food nothing changes in snake
            self.score += 1
            reward = REW_EAT
            self._place_food()
        else:
            # if snake didnt eat, the last part of snake is taken
            self.snake.pop()

        # updating ui and clock
        self._update_ui()
        self.clock.tick(GAME_SPEED)

        # returning game status and score
        return reward, game_over, self.score

    # checks if theres a collision with a given point,
    # if it wasnt given we check with the snake's head
    def _is_collision(self, point=None):
        
        if point == None:
            point = self.head

        if OBSTACLES == True:
            # hitting obstacle
            if self.point in self.obst[:]:
                return True
        else:
            # hitting boundry
            if self.point.x > self.w - BLOCK_SIZE or self.point.x < 0 or self.point.y > self.h - BLOCK_SIZE or self.point.y < 0:
                return True
        
        #hitting itself
        if self.point in self.snake[1:]:
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

    def _move(self, action):
        # changing direction (kepping straight/to the right/to the left)
        clockwise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clockwise.index(self.direction)

        # if straight dont change
        if np.array_equal(action, [1,0,0]):
            new_direction = clockwise[idx]
        # if right
        elif np.array_equal(action, [0,1,0]):
            idx = (idx+1)%4
            new_direction = clockwise[idx]
        # if left
        elif np.array_equal(action, [0,0,1]):
            idx = (idx-1)%4
            new_direction = clockwise[idx]


        # extracting coordinates
        x = self.head.x
        y = self.head.y
        # moving snake by blocksize
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE

        # updating head position
        self.head = Point(x, y)

pygame.quit()