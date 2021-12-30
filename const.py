OBSTACLES = True # enebling obstacles
MAP_NUMBER = 2

BLOCK_SIZE = 25 # size of an elementary game block
GAME_SPEED = 150 #speed of the game, higher=faster

MAX_MEMORY = 100000 #number of items stored in memory
BATCH_SIZE = 1000
GAMMA = 0.9 # must be <1
LR = 0.001 # learning rate
EPS_AMPL = 380 #lower = the faster random moves fade away 

INPUT_LAYER_SIZE = 11 #HAS TO BE
HIDDEN_LAYER_SIZE = 512
OUTPUT_LAYER_SIZE = 3 #HAS TO BE

# display dimentions (in blocks)
BLOCK_W = 30
BLOCK_H = 30

# reward values
REW_DIE = -10
REW_EAT = 10

# colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GRAY = (50,50,50)
ORANGE = (255,120,0)
YELLOW = (200,190,0)

OUT_SNAKE = (0,200,0)
IN_SNAKE = (0,150,0)
FOOD_COL = RED
OBST_COL = GRAY

#display buffor
DIS_BUFF = BLOCK_SIZE