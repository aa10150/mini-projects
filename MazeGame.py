"""
Maze Game by Anshu Aramandla
Run in Linux/WSL or macOS
"""
import copy
import time
import sys, tty, termios

def main():
    mode = 0
    print("\n"*15)
    print("1 for easy mode\n2 for hard mode\n3 for extra hard mode")
    print("\n"*15)
    while (mode != 1 and mode != 2 and mode != 3):
        modeInp = getch()
        if intCast(modeInp):
            mode = int(modeInp)
    maps = [[[0 for _ in range(10)] for _ in range(10)] for _ in range(4)]
    maps[0] = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 0, 0, 0, 1, 0, 0, 1],
               [1, 1, 0, 1, 0, 1, 1, 0, 1],
               [1, 0, 0, 1, 0, 1, 0, 0, 1],
               [1, 0, 1, 1, 2, 1, 0, 0, 1],
               [1, 0, 1, 0, 1, 0, 1, 0, 1],
               [1, 0, 0, 0, 0, 0, 1, 0, 1],
               [1, 0, 1, 1, 1, 0, 0, 3, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1]]
    maps[1] = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
               [1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1],
               [1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
               [1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
               [1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
               [1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1],
               [1, 0, 1, 0, 2, 1, 0, 0, 0, 1, 0, 1],
               [1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1],
               [1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1],
               [1, 3, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    maps[2] = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
               [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
               [1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1],
               [1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1],
               [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 2, 0, 1, 0, 1],
               [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
               [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1],
               [1, 0, 0, 3, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    maps[3] = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 3, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
               [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
               [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
               [1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
               [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
               [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
               [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
               [1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
               [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
               [1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
               [1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
               [1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1],
               [1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
               [1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
               [1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    # set position
    currentMap = 0
    map = maps[currentMap]
    position = findPlayer(map)
    # run game
    while(True):
        if mode == 1:
            printMap(map, True, currentMap)
        elif mode == 2:
            printMapRadius(map, True, position, 2, currentMap)
        elif mode == 3:
            printMapRadius(map, True, position, 1, currentMap)
        print()
        print(("Level " + str(currentMap+1)).rjust(int(round(len(map[0])))+3))
        print()
        # take user input
        #action = input("Move (W/A/S/D): ").capitalize()
        action = getch().capitalize()
        # perform action
        match action:
            case "W":
                map, newPos = moveUp(map, position)
                if newPos == 0:
                    position[0] -= 1
                elif newPos == 2:
                    position[0] -= 1
                    if currentMap == len(maps) - 1:
                        # win
                        break
                    else:
                        # next level
                        levelWin(map, position)
                        currentMap += 1
                        map = maps[currentMap]
                        position = findPlayer(map)
            case "S":
                map, newPos = moveDown(map, position)
                if newPos == 0:
                    position[0] += 1
                elif newPos == 2:
                    position[0] += 1
                    if currentMap == len(maps) - 1:
                        # win
                        break
                    else:
                        # next level
                        levelWin(map, position)
                        currentMap += 1
                        map = maps[currentMap]
                        position = findPlayer(map)
            case "A":
                map, newPos = moveLeft(map, position)
                if newPos == 0:
                    position[1] -= 1
                elif newPos == 2:
                    position[1] -= 1
                    if currentMap == len(maps) - 1:
                        # win
                        break
                    else:
                        # next level
                        levelWin(map, position)
                        currentMap += 1
                        map = maps[currentMap]
                        position = findPlayer(map)
            case "D":
                map, newPos = moveRight(map, position)
                if newPos == 0:
                    position[1] += 1
                elif newPos == 2:
                    position[1] += 1
                    if currentMap == len(maps) - 1:
                        # win
                        break
                    else:
                        # next level
                        levelWin(map, position)
                        currentMap += 1
                        map = maps[currentMap]
                        position = findPlayer(map)
            case "K":
                exit()
            case _:
                continue
    # win
    indices = [[-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1]]
    k = 0
    while(True):
        for index in indices:
            map[position[0]+index[0]][position[1]+index[1]] = 4
        if k == 7:
            k = 0
        else:
            k += 1
        index = indices[k]
        map[position[0]+index[0]][position[1]+index[1]] = 2
        map[position[0]-index[0]][position[1]-index[1]] = 2
        printMap(map, False, currentMap)
        print()
        print("Win!".rjust(int(len(map[0])+2)))
        print()
        time.sleep(0.3)

# print map with only points in radius
def printMapRadius(map, stillPlaying, position, radius, gameNo):
    mapX = len(map[0])
    mapY = len(map)
    emptyMap = [[-1 for _ in range(mapX)] for _ in range(mapY)]
    currentMap = emptyMap
    for y in range(mapY):
        for x in range(mapX):
            if abs(position[0]-y) <= radius and abs(position[1]-x) <= radius:
                currentMap[y][x] = map[y][x]
    for _ in range(44):
        print()
    if stillPlaying and gameNo <= 2:
        print("WASD to move\nK to quit")
    else:
        print("\n"*2)
    for _ in range(4):
        print()
    for row in currentMap:
        for col in row:
            if col == -1:
                print(" ", end=" ") # unknown
            elif col == 0:
                print(" ", end=" ") # empty space
            elif col == 1:
                print("■", end=" ") # wall
            elif col == 2:
                print("★", end=" ") # win
            elif col == 3:
                print("ඞ", end=" ") # player
            elif col == 4:
                print("☆", end=" ") # win+
            else:
                print("Error: invalid num", end="")
        print()
    print()

# get key pressed
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# find player
def findPlayer(map):
    position = [1, 1]
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 3:
                position = [i, j]
    return position

# print map
def printMap(map, stillPlaying, gameNo):
    for _ in range(44):
        print()
    if stillPlaying and gameNo <= 2:
        print("WASD to move\nK to quit")
    else:
        print()
        print()
    for i in range(4):
        print()
    for row in map:
        for col in row:
            if col == 0:
                print(" ", end=" ") # empty space
            elif col == 1:
                print("■", end=" ") # wall
            elif col == 2:
                print("★", end=" ") # win
            elif col == 3:
                print("ඞ", end=" ") # player
            elif col == 4:
                print("☆", end=" ") # win+
            else:
                print("Error: invalid num", end="")
        print()
    print()

# move up
def moveUp(map, position):
    newMap = copy.deepcopy(map)
    newPos = [position[0]-1, position[1]]
    # if empty space
    if map[newPos[0]][newPos[1]] == 0:
        # move
        newMap[newPos[0]][newPos[1]] = 3
        newMap[position[0]][position[1]] = 0
        return newMap, 0
    # if win
    elif map[newPos[0]][newPos[1]] == 2:
        # move and win
        newMap[newPos[0]][newPos[1]] = 3
        newMap[position[0]][position[1]] = 0
        return newMap, 2
    else:
        return newMap, 1

# move down
def moveDown(map, position):
    newMap = copy.deepcopy(map)
    newPos = [position[0]+1, position[1]]
    # if empty space
    if map[newPos[0]][newPos[1]] == 0:
        # move
        newMap[newPos[0]][newPos[1]] = 3
        newMap[position[0]][position[1]] = 0
        return newMap, 0
    # if win
    elif map[newPos[0]][newPos[1]] == 2:
        # move and win
        newMap[newPos[0]][newPos[1]] = 3
        newMap[position[0]][position[1]] = 0
        return newMap, 2
    else:
        return newMap, 1

# move left
def moveLeft(map, position):
    newMap = copy.deepcopy(map)
    newPos = [position[0], position[1]-1]
    # if empty space
    if map[newPos[0]][newPos[1]] == 0:
        # move
        newMap[newPos[0]][newPos[1]] = 3
        newMap[position[0]][position[1]] = 0
        return newMap, 0
    # if win
    elif map[newPos[0]][newPos[1]] == 2:
        # move and win
        newMap[newPos[0]][newPos[1]] = 3
        newMap[position[0]][position[1]] = 0
        return newMap, 2
    else:
        return newMap, 1

# move right
def moveRight(map, position):
    newMap = copy.deepcopy(map)
    newPos = [position[0], position[1]+1]
    # if empty space
    if map[newPos[0]][newPos[1]] == 0:
        # move
        newMap[newPos[0]][newPos[1]] = 3
        newMap[position[0]][position[1]] = 0
        return newMap, 0
    # if win
    elif map[newPos[0]][newPos[1]] == 2:
        # move and win
        newMap[newPos[0]][newPos[1]] = 3
        newMap[position[0]][position[1]] = 0
        return newMap, 2
    else:
        return newMap, 1

# check if castable to int
def intCast(x):
    try:
        int(x)
        return True
    except(ValueError, TypeError):
        return False

# display map before next level
def levelWin(map, position):
    indices = [[-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1]]
    k = 0
    for _ in range(10):
        for index in indices:
            map[position[0]+index[0]][position[1]+index[1]] = 4
        if k == 7:
            k = 0
        else:
            k += 1
        index = indices[k]
        map[position[0]+index[0]][position[1]+index[1]] = 2
        map[position[0]-index[0]][position[1]-index[1]] = 2
        printMap(map, False, 3)
        print()
        print("Next level...".rjust(int(len(map[0])+6)))
        print()
        time.sleep(0.3)

# execute main function
if __name__ == "__main__":
    main()