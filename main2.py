import numpy as np
import time
import os
import sys
import tty
import termios
import select
import math

print("hello, world")

# GAME SETTINGS
tall = 20
wide = 10
centre = 5
anchorpos = np.array([0,0])

# creates game space array
gamespace = np.zeros((tall, wide))

# for keyboard controls
def getch():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)

    try:
        tty.setcbreak(fd)
        r, _, _ = select.select([sys.stdin], [], [], 0)
        if r:
            return sys.stdin.read(1)
        return None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

def spawn_block(centre: int, anchorpos):
    anchorpos[0] = 1
    anchorpos[1] = centre 
    return anchorpos

def can_move_down(gamespace, anchorpos):
    #will be parsed in later
    L_tetro = np.array([
    [0, 0, 1], 
    [1, 1, 1]])
    
    height = L_tetro.shape[0]
    width = L_tetro.shape[1]

    
    
    
    return None


def move_block_down(gamespace, anchorpos, tall, centre):
    L_tetro = np.array([
    [0, 0, 1], 
    [1, 1, 1]])

    half = 2

    #check for floor or previous blocks
    if not anchorpos[0] >= tall-1 and gamespace[anchorpos[0] + 1, anchorpos[1]] == 0:
        #moving anchor down

        region = gamespace[anchorpos[0]:anchorpos[0] + 2, anchorpos[1] - half + 1:anchorpos[1] + half]
        mask = L_tetro != 0
        region[mask] = L_tetro[mask]


        #setting anchor postion
        anchorpos[0] = anchorpos[0] + 1

    else:
        anchorpos = spawn_block(gamespace, centre, anchorpos)
    
    return anchorpos

def player_move_block(gamespace, anchorpos, tall, currentinput, last_time, wide):
    if currentinput == 'a':
        if not anchorpos[1] <= 0:
            anchorpos[1] = anchorpos[1] - 1
            clear()
            print_temp_screen(gamespace, anchorpos)

    if currentinput == 'd':
        if not anchorpos[1] >= wide-1:
            anchorpos[1] = anchorpos[1] + 1
            clear()
            print_temp_screen(gamespace, anchorpos)
    
    if currentinput == 's':
        if not anchorpos[0] >= tall-1 and gamespace[anchorpos[0] + 1, anchorpos[1]] == 0:
            anchorpos[0] = anchorpos[0] + 1
            last_time = time.time()
            clear()
            print_temp_screen(gamespace, anchorpos)
            
        
    return anchorpos, last_time

def print_temp_screen(gamespace, anchorpos, currentblock):
    screenspace = gamespace.copy()

    #screenspace[anchorpos[0], anchorpos[1]] = 1

    print(screenspace)
    
    return None


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    return

########## Teris Blocks #############
L_tetro = np.array([
    [0, 0, 1], 
    [1, 1, 1]])

S_tetro = np.array([
    [0, 1, 1], 
    [1, 1, 0]])

J_tetro = np.array([
    [1, 0, 0], 
    [1, 1, 1]])

L_tetro = np.array([
    [1, 1, 1, 1]])


anchorpos = spawn_block(centre, anchorpos)

interval = 0.5
last_time = time.time()
while True:
    now = time.time()
    check_time = now - last_time

    if check_time >= interval:
        anchorpos = move_block_down(gamespace, anchorpos, tall, centre)
        last_time = time.time()
        clear()
        print_temp_screen(gamespace, anchorpos)
    
    else:
        currentinput  = getch()
        anchorpos, last_time = player_move_block(gamespace, anchorpos, tall, currentinput, last_time, wide)

    