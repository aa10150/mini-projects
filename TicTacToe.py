"""
Tic Tac Toe by Anshu Aramandla
Run in Linux/WSL or macOS
"""
import sys, tty, termios

def main():
    print("\n"*40)
    player = 0 # 0 = O's, 1 = X's
    grid = [[-1, -1, -1],
            [-1, -1, -1],
            [-1, -1, -1]] # -1 = empty, 0 = O, 1 = X
    position = [0, 0]
    # run game
    while(True):
        printGrid(grid, True, position, player)
        print("\n")
        # take user input
        action = getch().capitalize()
        # perform action
        match action:
            case "A": # move left
                if position[0] > 0:
                    position[0] -= 1
            case "D": # move right
                if position[0] < 2:
                    position[0] += 1
            case "W": # move up
                if position[1] > 0:
                    position[1] -= 1
            case "S": # move down
                if position[1] < 2:
                    position[1] += 1
            case " ": # pick square
                if grid[position[1]][position[0]] == -1:
                    grid[position[1]][position[0]] = player
                    if player == 0:
                        if checkWin(grid, 0):
                            displayWin(grid, 0)
                        player = 1
                    else:
                        if checkWin(grid, 1):
                            displayWin(grid, 1)
                        player = 0
                    position = [0, 0]
            case "K":
                exit()
            case _:
                continue
        # check for tie
        tie = True
        for r in grid:
            for c in r:
                if c == -1:
                    tie = False
        if tie:
            displayWin(grid, -1)
    

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

# print grid
def printGrid(grid, stillPlaying, playerPos, player):
    for _ in range(44):
        print()
    if stillPlaying:
        print("WASD to move\nSpace to select\nK to quit")
    else:
        print()
        print()
    for i in range(2):
        print()
    if stillPlaying:
        if player == 0:
            print("O turn")
        else:
            print("X turn")
        print()
        print("  "*playerPos[0], end="↓\n") # player position horizontal
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == -1:
                print("□", end=" ") # empty square
            elif grid[r][c] == 0:
                print("O", end=" ") # O
            elif grid[r][c] == 1:
                print("X", end=" ") # X
            else:
                print("Error: invalid num", end="")
            if c == len(grid[r])-1 and r == playerPos[1]:
                print("←", end="") # player position vertical
        print()
    print()

# check for win condition
def checkWin(grid, player):
    for row in grid:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(grid[row][col] == player for row in range(3)):
            return True
    if all(grid[i][i] == player for i in range(3)):
        return True
    if all(grid[i][2 - i] == player for i in range(3)):
        return True
    return False

# display win state
def displayWin(grid, winner):
    printGrid(grid, False, [3, 3], winner)
    if winner == 0:
        print("O wins!")
    elif winner == 1:
        print("X wins!")
    else:
        print("Tie")
    print()
    exit()

# execute main function
if __name__ == "__main__":
    main()