import random


def createBoard(rows: int, cols: int) -> list:
    return [[0] * cols for _ in range(rows)]

def getDirection(directions: list, lastDirection: list) -> list:
    dir = random.choice(directions)
    while dir == lastDirection or (dir[0] == -lastDirection[0] and dir[1] == -lastDirection[1]):
        dir = random.choice(directions)
    return dir

def createMap(dimensions: tuple, maxTuns: int, maxLen: int) -> list:

    if maxTuns < 0 or maxLen < 0:
        raise ValueError("Use positive numbers please")

    # maxTunnels is how many turns will be created
    # maxLength is how long each tunnel can be

    rows, cols = dimensions[0], dimensions[1]

    # initialize the map
    gameMap = createBoard(rows, cols)
    
    # where we make our first tunnel (gotta start somewhere)
    curPos = (random.randint(0, rows - 1), random.randint(0, cols - 1))

    # we'll use this later for the player starting position
    firstPos = curPos

    # set this to be part of the path
    gameMap[curPos[0]][curPos[1]] = 7

    # it goes:      up      down    left     right
    directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]

    lastDir = (0,0)
    
    # generate tunnels in the game map

    # this is needed for a while loop
    numTunsLeft = 0

    '''using a while loop so that we can control when we increment the number
    of tunnels left, which is important in a certain case:

    if the tunnel is at a wall, and the new direction goes into the wall,
    then the loop will immediately break and a for loop would increment, but
    we dont want that'''

    while numTunsLeft < maxTuns:
        lenOfCurTun = 0
        dir = getDirection(directions, lastDir)
        tunLen = random.randint(1, maxLen)
        for i in range(1, tunLen):
            r, c = curPos[0] + dir[0], curPos[1] + dir[1]
            if r not in range(rows) or c not in range(cols):
                break
            else:
                lenOfCurTun += 1
                curPos = (r, c)
                gameMap[r][c] = 7
        if lenOfCurTun >= 1:
            numTunsLeft += 1
        lastDir = dir

    return (gameMap, firstPos)


