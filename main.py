import numpy as np
import time
import os
import sys
import tty
import termios
import select
import math

print("hello, world")

tall = 20
wide = 10
centre = 5
anchorpos = np.array([0,0])

arr = np.zeros((tall, wide))


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


def row_check(arr):
    for row in arr:
        for colum in row:
            if colum == 0:
                print("empty")
            elif colum == 1:
                print("not empty")
    return arr

def ind_row_check(arr, rownum: int):
    clearrow = 0
    for row in arr[rownum]:
        if row == 0:
            clearrow = 1
            break

    if clearrow == 0:
        arr[rownum, :] = 0

    return

def spawn_block(arr, centre: int, anchorpos):
    arr[0, centre] = 1
    anchorpos[0] = 1
    anchorpos[1] = centre 

    half = 1

    L_tetro = np.array([
    [0, 0, 1], 
    [1, 1, 1]])

    region = arr[0:2, centre - 1:centre + 2]

    mask = L_tetro != 0
    region[mask] = L_tetro[mask]
    return anchorpos

def can_move_block_down(arr, block):

    return

def move_block_down(arr, anchorpos, tall, centre, block_width):
    L_tetro = np.array([
    [0, 0, 1], 
    [1, 1, 1]])

    half = math.floor(block_width/2)

    #check for floor or previous blocks
    if not anchorpos[0] >= tall-1 and arr[anchorpos[0] + 1, anchorpos[1]] == 0:
        #moving anchor down

        region = arr[anchorpos[0]:anchorpos[0] + 3, anchorpos[1] - half:anchorpos[1] + half + 1]
        mask = L_tetro != 0
        region[mask] = L_tetro[mask]


        #setting anchor postion
        anchorpos[0] = anchorpos[0] + 1

    else:
        anchorpos = spawn_block(arr, centre, anchorpos)
    
    return anchorpos

def player_move_block(arr, anchorpos, tall, currentinput, last_time, wide):
    if currentinput == 'a':
        if not anchorpos[1] <= 0:
            arr[anchorpos[0] , anchorpos[1] -1 ] = 1
            arr[anchorpos[0], anchorpos[1]] = 0

            anchorpos[1] = anchorpos[1] - 1
            clear()
            print(arr)

    if currentinput == 'd':
        if not anchorpos[1] >= wide-1:
            arr[anchorpos[0] , anchorpos[1] +1 ] = 1
            arr[anchorpos[0], anchorpos[1]] = 0

            anchorpos[1] = anchorpos[1] + 1
            clear()
            print(arr)
    
    if currentinput == 's':
        if not anchorpos[0] >= tall-1 and arr[anchorpos[0] + 1, anchorpos[1]] == 0:
            arr[anchorpos[0] + 1, anchorpos[1]] = 1
            arr[anchorpos[0], anchorpos[1]] = 0

            anchorpos[0] = anchorpos[0] + 1
            last_time = time.time()
            clear()
            print(arr)
            
        
    return anchorpos, last_time


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


# print(arr)
# arr[19,9] = 1
# arr[19,8] = 1
# arr[19,7] = 1
# arr[19,6] = 1
# arr[19,5] = 1
# arr[19,4] = 1
# arr[19,3] = 1
# arr[19,2] = 1
# arr[19,1] = 1
# arr[19,0] = 1

# print(arr)
# ind_row_check(arr, 19)
# print(arr)



block_width = 2

anchorpos = spawn_block(arr, centre, anchorpos)

interval = 0.5
last_time = time.time()
while True:
    now = time.time()
    check_time = now - last_time

    if check_time >= interval:
        anchorpos = move_block_down(arr, anchorpos, tall, centre, block_width)
        last_time = time.time()
        clear()
        print(arr)
    
    else:
        currentinput  = getch()
        anchorpos, last_time = player_move_block(arr, anchorpos, tall, currentinput, last_time, wide)

    