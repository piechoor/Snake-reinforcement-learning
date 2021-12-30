import torch
import random
import numpy as np
import const

from collections import deque
from snake_agent import SnakeGame, Direction, Point
from model import Linear_Qnet, QTrainer
from plot import plot

class Agent:

    def __init__(self):
        self.no_games = 0
        self.epsilon = 0 # randomness factor
        # if maxlen is exceeded deque does popleft()
        self.memory = deque(maxlen=const.MAX_MEMORY)
        self.model = Linear_Qnet(const.INPUT_LAYER_SIZE,
                                 const.HIDDEN_LAYER_SIZE, const.OUTPUT_LAYER_SIZE)
        self.trainer = QTrainer(self.model, lr=const.LR, gamma=const.GAMMA)

    def get_state(self, game):
        head = game.snake[0]

        #blocks around the head
        block_left = Point(head.x-const.BLOCK_SIZE, head.y)
        block_right = Point(head.x+const.BLOCK_SIZE, head.y)
        block_up = Point(head.x, head.y-const.BLOCK_SIZE)
        block_down = Point(head.x, head.y+const.BLOCK_SIZE)

        #current directions state
        dir_left = game.direction == Direction.LEFT
        dir_right = game.direction == Direction.RIGHT
        dir_up = game.direction == Direction.UP
        dir_down = game.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_right and game.is_collision(block_right)) or 
            (dir_left and game.is_collision(block_left)) or 
            (dir_up and game.is_collision(block_up)) or 
            (dir_down and game.is_collision(block_down)),

            # Danger right
            (dir_up and game.is_collision(block_right)) or 
            (dir_down and game.is_collision(block_left)) or 
            (dir_left and game.is_collision(block_up)) or 
            (dir_right and game.is_collision(block_down)),

            # Danger left
            (dir_down and game.is_collision(block_right)) or 
            (dir_up and game.is_collision(block_left)) or 
            (dir_right and game.is_collision(block_up)) or 
            (dir_left and game.is_collision(block_down)),
            
            # Move direction
            dir_left,
            dir_right,
            dir_up,
            dir_down,
            
            # Food location 
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y  # food down
            ]

        # changing boolean to int data type while returning
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        # storing as a one tuple (double()) 
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > const.BATCH_SIZE:
            mini_sample = random.sample(self.memory, const.BATCH_SIZE)
        else:
            mini_sample = self.memory

        # extracting states to one list and so on
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self,state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        #random moves - tradeoff
        self.epsilon = const.EPS_AMPL - self.no_games
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGame()

    while True:
        #getting old state
        state_old = agent.get_state(game)

        #getting move
        final_move = agent.get_action(state_old)

        #performs move and gets new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        #train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        #remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            #training long memory, plot results
            game.reset_game()
            agent.no_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game:', agent.no_games, 'Score:', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / (agent.no_games + 1)
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()