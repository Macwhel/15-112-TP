import random
import copy

# Don't need this
'''def createBoard(rows: int, cols: int) -> list:
    return [[0] * cols for _ in range(rows)]'''

def getDirection(directions: list, lastDirection: list) -> tuple:
    dir = random.choice(directions)
    while dir == lastDirection or (dir[0] == -lastDirection[0] and dir[1] == -lastDirection[1]):
        dir = random.choice(directions)
    return dir

# utilizes a random walker algorithm for map generation 
# (https://www.freecodecamp.org/news/how-to-make-your-own-procedural-dungeon-map-generator-using-the-random-walk-algorithm-e0085c8aa9a/)

def randomMap() -> str:
    return random.choice(["Kruskals", "Random Walker", 'KruskalsWeave'])

def createMap(dimensions: tuple, maxTuns: int, maxLen: int) -> tuple:

    if maxTuns < 0 or maxLen < 0:
        raise ValueError("Use positive numbers please")

    # maxTunnels is how many turns will be created
    # maxLength is how long each tunnel can be

    rows, cols = dimensions[0], dimensions[1]

    # initialize the map
    gameMap = [[0] * cols for _ in range(rows)]
    
    # where we make our first tunnel (gotta start somewhere)
    curPos = (random.randint(0, rows - 1), random.randint(0, cols - 1))

    # we'll use this later for the player starting position
    firstPos = curPos

    # set this to be part of the path
    gameMap[curPos[0]][curPos[1]] = 7

    # it goes:      up      down    left     right
    directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]

    lastDir = (0,0)
    

    '''using a while loop so that we can control when we increment the number
    of tunnels left, which is important in a certain case:

    if the tunnel is at a wall, and the new direction goes into the wall,
    then the loop will immediately break and a for loop would increment, but
    we dont want that'''

    # this is needed for a while loop
    numTunsLeft = 0

    # this is needed to get the goal node
    goalNodeIt = random.randint(int(0.75 * maxTuns), maxTuns)

    # initialize list for legal mob positions
    legalMobPos = []

    # generate tunnels in the game map

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
                if numTunsLeft > 0.5 * maxTuns:
                    if firstPos != curPos: legalMobPos.append(curPos)
                gameMap[r][c] = 7
        if lenOfCurTun >= 1:
            numTunsLeft += 1

        if goalNodeIt >= 1:
            goalNodeIt -= 1
        else:
            goalPos = (r,c)
        lastDir = dir

    return (gameMap, firstPos, goalPos, legalMobPos)


# try to implement based on description, no outside pseudocode
# utilized 4 slides/pictures
# http://www.jamisbuck.org/presentations/rubyconf2011/index.html#kruskals
def Kruskals(dimensions: tuple) -> list:

    # init variables
    rows, cols = dimensions

    # keep it simple, make firstPos in the center
    cent = (rows // 2) if ((rows // 2) % 2 == 0) else ((rows // 2) + 1)
    firstPos = (cent, cent)

    edge = (rows - 1) if ((rows - 1) % 2 == 0) else (rows - 2)
    # make goal pos in the corner
    goalPos = random.choice([(0,0), (0, edge), (edge, 0), (edge, edge)])
    legalMobPos = []

    r1 = [7 if i % 2 == 0 else 0 for i in range(cols)]
    r2 = [0 for i in range(cols)]
    
    # init board
    board = [copy.deepcopy(r1) if i % 2 == 0 else copy.deepcopy(r2) for i in range(rows)]

    directions = [
        [-2, 0], # up
        [2,0], # down
        [0,-2], # left
        [0,2] # right
        ]

    paths = [{(i, j)} for j in range(0, cols, 2) for i in range(0, rows, 2)]

    # 1: choose a random cell that is a path
    # 2: randomly get the directions
    # 3: if there's something that's not connected, (aka there's a 0 in between)
    # 3a: check if it's in the set that this location is also in
    # if so, check another direction and repeat from 3
    # 3b: if it's not, add it to the set
    # 4: update the board
    # 5: keep it going until len of the set is 1

    # 5
    while len(paths) > 1:
        # 1

        a = random.choice(paths)
        loc = random.sample(a, 1)[0]
        # 2
        newLoc = False
        random.shuffle(directions)
        for d in directions:
            y = d[0] + loc[0]
            x = d[1] + loc[1]
            if y in range(rows) and x in range(cols):
                newLoc = (y, x)
                
                # find where newLoc and loc is in the list of paths for later use
                indexOfNewLoc = indexOfLoc = False
                for i, path in enumerate(paths):
                    if newLoc in path:
                        indexOfNewLoc = i
                    if loc in path:
                        indexOfLoc = i
                    
                    # no need to keep on going if you find the position
                    if indexOfLoc and indexOfNewLoc:
                        break
                # 3a
                if indexOfNewLoc == indexOfLoc:
                    break # it's in the same path, get a new direction

                # 3b: otherwise, it's legal
                paths[indexOfLoc] = paths[indexOfLoc].union(paths[indexOfNewLoc])
                paths.pop(indexOfNewLoc)

                # 4
                midY = loc[0] + (d[0] // 2)
                midX = loc[1] + (d[1] // 2)
                board[midY][midX] = 7

                # add a mob to this tile if it's not right next to char
                if abs(firstPos[0] - midY) > 2 and abs(firstPos[1] - midX) > 2:
                    legalMobPos.append((midY, midX))

                break
    # (gameMap, firstPos, goalPos, legalMobPos)
    return board, firstPos, goalPos, legalMobPos

def KruskalsWeave(dimensions: tuple) -> list:

    # init variables
    rows, cols = dimensions

    # keep it simple, make firstPos in the center
    cent = (rows // 2) if ((rows // 2) % 2 == 0) else ((rows // 2) + 1)
    firstPos = (cent, cent)

    edge = (rows - 1) if ((rows - 1) % 2 == 0) else (rows - 2)
    # make goal pos in the corner
    goalPos = random.choice([(0,0), (0, edge), (edge, 0), (edge, edge)])
    legalMobPos = []

    r1 = [7 if i % 2 == 0 else 0 for i in range(cols)]
    r2 = [0 for i in range(cols)]
    
    # init board
    board = [copy.deepcopy(r1) if i % 2 == 0 else copy.deepcopy(r2) for i in range(rows)]

    directions = [
        [-2, 0], # up
        [2,0], # down
        [0,-2], # left
        [0,2] # right
        ]

    paths = [{(i, j)} for j in range(0, cols, 2) for i in range(0, rows, 2)]

    '''print(paths, len(paths))
    for r in board:
        print(r)'''

    # 1: choose a random cell that is a path
    # 2: randomly get the directions
    # 3: if there's something that's not connected, (aka there's a 0 in between)
    # 3a: check if it's in the set that this location is also in
    # if so, check another direction and repeat from 3
    # 3b: if it's not, add it to the set
    # 4: update the board
    # 5: keep it going until len of the set is 1

    # add weaves:

    numOfWeaves = rows // 3

    while numOfWeaves >= 1:
        isLegal = True
        a = random.choice(paths)
        loc = random.sample(a, 1)[0] 
        locX = loc[0]
        locY = loc[1]

        # check if legal:
        # cant be right next to an overlapped path nor out of range

        if not(2 <= locX < (cols - 2) and 2 <= locY < (rows - 2)): continue

        for i in range(-2, 3, 2):
            # -2, 2
            if (board[locX - i][locY] == 8 or board[locX - i][locY] == 9 or 
                board[locX][locY - i] == 8 or board[locX][locY - i] == 9):
                isLegal = False
                break

        
        if isLegal:
            numOfWeaves -= 1

            # 8 = vertical path on top, 9 = horizontal path on top
            board[locX][locY] = random.randrange(8,10)

            # connecting the stuff/breaking down walls
            board[locX - 1][locY] = 7
            board[locX + 1][locY] = 7 
            board[locX][locY - 1] = 7
            board[locX][locY + 1] = 7

            posLeft = (locX - 2, locY) # inLeft
            posRight = (locX + 2, locY) # inRight
            posUp = (locX, locY - 2) # inUp
            posDown = (locX, locY + 2) # inDown

            # find locations of horizontal path
            inLeft = inRight = inUp = inDown = inLoc = False
            for i, path in enumerate(paths):
                if posLeft in path:
                    inLeft = i
                if posRight in path:
                    inRight = i 
                if posUp in path:
                    inUp = i
                if posDown in path:
                    inDown = i
                if loc in path:
                    inLoc = i  

                # no need to keep on going if you find the positions
                if inLeft and inRight and inLoc and inUp and inDown:
                    break

            #print(inLeft, inRight, inUp, inDown, inLoc)

            # merge the sets
            # Probably a cleaner way to do this but I'm on lack of sleep rn and feel sick have mercy
            locSet = paths[inLoc]
            paths[inLeft] = paths[inLeft].union(locSet)
            paths[inLeft] = paths[inLeft].union(paths[inRight])
            paths.pop(inRight)

            # in case the indeces is shifted
            if inRight < inUp:
                inUp -= 1
            if inRight < inLoc:
                inLoc -= 1
            if inRight < inDown:
                inDown -= 1

            paths[inUp] = paths[inUp].union(locSet)
            paths[inUp] = paths[inUp].union(paths[inDown])
            paths.pop(inDown)

            if inDown < inLoc:
                inLoc -= 1

            paths.pop(inLoc)

            '''print(paths, len(paths))
            for r in board:
                print(r)'''

    # 5
    while len(paths) > 1:
        # 1

        a = random.choice(paths)
        loc = random.sample(a, 1)[0]
        # 2
        newLoc = False
        random.shuffle(directions)
        for d in directions:
            y = d[0] + loc[0]
            x = d[1] + loc[1]
            if y in range(rows) and x in range(cols):
                newLoc = (y, x)
                
                # find where newLoc and loc is in the list of paths for later use
                indexOfNewLoc = indexOfLoc = False
                for i, path in enumerate(paths):
                    if newLoc in path:
                        indexOfNewLoc = i
                    if loc in path:
                        indexOfLoc = i
                    
                    # no need to keep on going if you find the position
                    if indexOfLoc and indexOfNewLoc:
                        break
                # 3a
                if indexOfNewLoc == indexOfLoc:
                    break # it's in the same path, get a new direction

                # 3b: otherwise, it's legal
                paths[indexOfLoc] = paths[indexOfLoc].union(paths[indexOfNewLoc])
                paths.pop(indexOfNewLoc)
                '''print(paths, len(paths))
                for r in board:
                    print(r)'''

                # 4
                midY = loc[0] + (d[0] // 2)
                midX = loc[1] + (d[1] // 2)
                board[midY][midX] = 7

                # add a mob to this tile if it's not right next to char
                if abs(firstPos[0] - midY) > 2 and abs(firstPos[1] - midX) > 2:
                    legalMobPos.append((midY, midX))

                break

    # (gameMap, firstPos, goalPos, legalMobPos)
    return board, firstPos, goalPos, legalMobPos