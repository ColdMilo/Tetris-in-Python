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

def can_move_down(gamespace, anchorpos, current_block):

    height, width = current_block.shape

    print("height:", height, "  width:", width)

    cantmove = False

    #anchorpos 0 = height, anchorpos 1 = width
    print(anchorpos[0])
    if anchorpos[0] < 20 - height:
        for i in reversed(range(width)):
            if current_block[height-1][i] == 1:
                print("its at bottom, current spot:", i)
                if gamespace[anchorpos[0] + height, anchorpos[1] + i] == 1:
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
def can_move_left(gamespace, anchorpos, current_block):

    height, width = current_block.shape

    print("height:", height, "  width:", width)

    left_block_padding = 0

    cantmove = False

    if anchorpos[1] > 0 + left_block_padding:
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
                        
    else:
        cantmove = True
    
    return cantmove


#anchorpos 0 = height, anchorpos 1 = width
def can_move_right(gamespace, anchorpos, current_block):

    height, width = current_block.shape

    print("height:", height, "  width:", width)

    right_block_padding = width - 1

    cantmove = False

    print(L_tetro)
    if anchorpos[1] < 10 - 1 - right_block_padding:
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

    else:
        cantmove = True
    
    return cantmove

def hard_drop(gamespace, anchorpos, current_block):
    while True:
        if can_move_down(gamespace, anchorpos, current_block) == False:
            anchorpos[0] = anchorpos[0] + 1
        else:
            break

    
    return anchorpos

def place_block(gamespace, anchorpos, current_block):
    height, width = current_block.shape

    start_row = anchorpos[0]
    start_col = anchorpos[1]

    region = gamespace[
        start_row:start_row + height,
        start_col:start_col + width
    ]

    mask = current_block != 0
    region[mask] = current_block[mask]

    print(gamespace)

    anchorpos = spawn_block(5, anchorpos)

    gamespace = row_check(gamespace)

    return gamespace, anchorpos

#ONLY WORKS ON BOTTOM ROW ATM 
def row_check(gamespace):
    clearrow = 0
    for row in gamespace[19]:
        if row == 0:
            clearrow = 1
            break

    if clearrow == 0:
        gamespace[19, :] = 0
        r = 19 #row 19
        gamespace[1:r+1] = gamespace[0:r]
        gamespace[0] = 0 
      
    return gamespace

def move_block_down(gamespace, anchorpos, current_block, block_hover):
    if can_move_down(gamespace, anchorpos, current_block) == False:
        anchorpos[0] = anchorpos[0] + 1
        print("test1")
    else:
        if block_hover == True:
            print("test2")
            block_hover = False
        else:
            print("moving down")
            gamespace, anchorpos = place_block(gamespace, anchorpos, current_block)
    return anchorpos, gamespace, block_hover

def player_move_block(gamespace, anchorpos, currentinput, last_time, current_block):
    if currentinput == 'a':
        if can_move_left(gamespace, anchorpos, current_block) == False:
            anchorpos[1] = anchorpos[1] - 1
            clear()
            print_temp_screen(gamespace, anchorpos, current_block)

    if currentinput == 'd':
        if can_move_right(gamespace, anchorpos, current_block) == False:
            anchorpos[1] = anchorpos[1] + 1
            clear()
            print_temp_screen(gamespace, anchorpos, current_block)
    
    if currentinput == 's':
        if can_move_down(gamespace, anchorpos, current_block) == False:
            anchorpos[0] = anchorpos[0] + 1
            last_time = time.time()
            clear()
            print_temp_screen(gamespace, anchorpos, current_block)
    
    if currentinput == 'w':
        current_block = np.rot90(current_block)
        clear()
        print_temp_screen(gamespace, anchorpos, current_block)

    if currentinput == ' ':
        anchorpos = hard_drop(gamespace, anchorpos, current_block)
        clear()
        print_temp_screen(gamespace, anchorpos, current_block)      
        
    return anchorpos, last_time, current_block

#anchorpos 0 = height, anchorpos 1 = width
def print_temp_screen(gamespace, anchorpos, current_block):
    screenspace = gamespace.copy()

    height, width = current_block.shape

    start_row = anchorpos[0]
    start_col = anchorpos[1]

    region = screenspace[
        start_row:start_row + height,
        start_col:start_col + width
    ]

    mask = current_block != 0
    region[mask] = current_block[mask]

    #screenspace[anchorpos[0], anchorpos[1]] = 2

    print(screenspace)
    
    return None


def clear():
    #os.system('cls' if os.name == 'nt' else 'clear')
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

Long_tetro = np.array([
    [1, 1, 1, 1]])

current_block = L_tetro.copy()

print(gamespace)

anchorpos = spawn_block(centre, anchorpos)

interval = 0.5
last_time = time.time()
block_hover = True
while True:
    now = time.time()
    check_time = now - last_time

    if check_time >= interval:
        anchorpos, gamespace, block_hover = move_block_down(gamespace, anchorpos, current_block, block_hover)
        last_time = time.time()
        clear()
        print_temp_screen(gamespace, anchorpos, current_block)
    
    else:
        currentinput  = getch()
        anchorpos, last_time, current_block = player_move_block(gamespace, anchorpos, currentinput, last_time, current_block)

    