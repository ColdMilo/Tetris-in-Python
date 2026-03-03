import numpy as np

L_tetro = np.array([
[1, 1, 1, 1], 
[0, 1, 0, 0],
[0, 0, 1, 0], 
[0, 0, 0, 1]])

current_block = L_tetro.copy()

height, width = current_block.shape

print("height:", height, "  width:", width)

print(L_tetro)
for i in reversed(range(height)):
    if current_block[i][width - 1] == 1:
        print("its edge , current spot:", i)


    else:
        for o in range(width):
            if current_block[i][o] == 1:
                print("not at bottom, looking at spot:", i, "   its deep in at:", o)
                break
                
