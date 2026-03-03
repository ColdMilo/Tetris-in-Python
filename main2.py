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
    [1, 1, 1], 
    [1, 1, 1],
    [0, 1, 0]])

    current_block = L_tetro.copy()

    height, width = current_block.shape

    print("height:", height, "  width:", width)

    cantmove = False

    #anchorpos 0 = height, anchorpos 1 = width
    print(anchorpos[0])
    if anchorpos[0] < 20 - height:
        for i in reversed(range(width)):
            if current_block[height-1][i] == 1:
                print("its at bottom, current spot:", i)
                if gamespace[anchorpos[0] + height, anchorpos[1] + i - 1] == 1:
                    print(i, "fart", current_block[height-1][i], "something is below", anchorpos[0], anchorpos[1])
                    cantmove = True
                    break

            else:
                for o in reversed(range(height)):
                    if current_block[o][i] == 1:
                        print("not at bottom, looking at spot:", i, "   its at height:", o)
                        print(gamespace[anchorpos[0] + o + 1, anchorpos[1] + i - 1])
                        if gamespace[anchorpos[0] + height - o, anchorpos[1] + i - 1] == 1:
                            cantmove = True
                            break
                        break
    else:
        cantmove = True

    return cantmove

#anchorpos 0 = height, anchorpos 1 = width
def can_move_left(gamespace, anchorpos):
    L_tetro = np.array([
    [1, 1, 1], 
    [1, 1, 1],
    [0, 1, 0]])

    current_block = L_tetro.copy()

    height, width = current_block.shape

    print("height:", height, "  width:", width)

    left_block_padding = math.floor((width - 1)/2)

    cantmove = False

    print(L_tetro)
    for i in range(height):
        if current_block[i][0] == 1:
            print("its edge , current spot:", i)
            if gamespace[anchorpos[0] + i, anchorpos[1] - left_block_padding - 1] == 1:
                    print(i, "fart", current_block[height-1][i], "something is below", anchorpos[0], anchorpos[1])
                    cantmove = True
                    break

        else:
            for o in range(width):
                if current_block[i][o] == 1:
                    print("not at bottom, looking at spot:", i, "   its deep in at:", o)
                    if gamespace[anchorpos[0] + i, anchorpos[1] - left_block_padding + o - 1] == 1:
                            cantmove = True
                            break
    
    return cantmove


#anchorpos 0 = height, anchorpos 1 = width
def can_move_right(gamespace, anchorpos):
    L_tetro = np.array([
    [1, 1, 1], 
    [1, 1, 1],
    [0, 1, 0]])

    current_block = L_tetro.copy()

    height, width = current_block.shape

    print("height:", height, "  width:", width)

    right_block_padding = math.floor((width - 1)/2)

    cantmove = False

    print(L_tetro)
    for i in reversed(range(height)):
        if current_block[i][width - 1] == 1:
            print("its edge , current spot:", i)
            if gamespace[anchorpos[0] + i, anchorpos[1] + right_block_padding + 1] == 1:
                    print(i, "fart", current_block[height-1][i], "something is below", anchorpos[0], anchorpos[1])
                    cantmove = True
                    break

        else:
            for o in range(width):
                if current_block[i][o] == 1:
                    print("not at bottom, looking at spot:", i, "   its deep in at:", o)
                    if gamespace[anchorpos[0] + i, anchorpos[1] + right_block_padding - o + 1] == 1:
                            cantmove = True
                            break
    
    return cantmove


                






def move_block_down(gamespace, anchorpos, tall, centre):
    if can_move_down(gamespace, anchorpos) == False:
        anchorpos[0] = anchorpos[0] + 1
    return anchorpos

def player_move_block(gamespace, anchorpos, tall, currentinput, last_time, wide):
    if currentinput == 'a':
        if can_move_left(gamespace, anchorpos) == False:
            anchorpos[1] = anchorpos[1] - 1
            clear()
            print_temp_screen(gamespace, anchorpos)

    if currentinput == 'd':
        if can_move_right(gamespace, anchorpos) == False:
            anchorpos[1] = anchorpos[1] + 1
            clear()
            print_temp_screen(gamespace, anchorpos)
    
    if currentinput == 's':
        if can_move_down(gamespace, anchorpos) == False:
            anchorpos[0] = anchorpos[0] + 1
            last_time = time.time()
            clear()
            print_temp_screen(gamespace, anchorpos)
            
        
    return anchorpos, last_time

def print_temp_screen(gamespace, anchorpos):
    screenspace = gamespace.copy()

    #screenspace[anchorpos[0], anchorpos[1]] = 1
    L_tetro = np.array([
    [1, 1, 1], 
    [1, 1, 1],
    [0, 1, 0]])

    half = 2

    region = screenspace[anchorpos[0]:anchorpos[0] + 3, anchorpos[1] - half + 1:anchorpos[1] + half]
    mask = L_tetro != 0
    region[mask] = L_tetro[mask]

    screenspace[anchorpos[0], anchorpos[1]] = 2


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


gamespace[19,9] = 1
gamespace[19,8] = 1
gamespace[19,7] = 1
gamespace[19,6] = 1
gamespace[18,6] = 1
gamespace[17,6] = 1
# gamespace[19,5] = 1
# gamespace[19,4] = 1
# gamespace[19,3] = 1
# gamespace[19,2] = 1
# gamespace[19,1] = 1
# gamespace[19,0] = 1

print(gamespace)



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

    