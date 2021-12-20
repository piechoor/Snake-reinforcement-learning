from constants import *
from collections import namedtuple

# Object representing a point, implementation is done
# nametuple - it resembles simplified class implementation 
Point = namedtuple('Point', 'x, y')

# MAPS BY NUMBERS
# MAP #0 - borders around the display
# MAP #1 - windmill

def block_adj(val):
    return val//BLOCK_SIZE*BLOCK_SIZE

def init_obst_map(width, height):
    obstacles = []
    if MAP_NUMBER == 0:
        for i in range(int(width/BLOCK_SIZE)+1):
            obstacles.append(Point(i*BLOCK_SIZE,0))
            obstacles.append(Point(i*BLOCK_SIZE,height))
        for i in range(1, int(height/BLOCK_SIZE)):
            obstacles.append(Point(0,i*BLOCK_SIZE))
            obstacles.append(Point(width,i*BLOCK_SIZE))

    if MAP_NUMBER == 1:
        mid = Point(int(width/2), int(height/2))
        thr_w = int(width/3)
        thr_h = int(height/3)
        
        for i in range(int((mid.x-thr_w)/BLOCK_SIZE), int((mid.x+thr_w)/BLOCK_SIZE)):
            obstacles.append(Point(i*BLOCK_SIZE,block_adj(mid.y)))
            if i < mid.x/BLOCK_SIZE:
                obstacles.append(Point(i*BLOCK_SIZE,block_adj(mid.y-thr_h)))
            else:
                obstacles.append(Point(i*BLOCK_SIZE,block_adj(mid.y+thr_h)))
        for i in range(int((mid.y-thr_h)/BLOCK_SIZE), int((mid.y+thr_h)/BLOCK_SIZE)):
            obstacles.append(Point(block_adj(mid.x),i*BLOCK_SIZE))
            if i > mid.y/BLOCK_SIZE:
                obstacles.append(Point(block_adj(mid.x-thr_w),i*BLOCK_SIZE))
            else:
                obstacles.append(Point(block_adj(mid.x+thr_w),i*BLOCK_SIZE))

    return obstacles