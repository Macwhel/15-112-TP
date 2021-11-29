import random
import copy

dimensions = (10,10)

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

numOfWeaves = rows // 3
print(numOfWeaves)

while numOfWeaves >= 1:
    isLegal = True
    a = random.choice(paths)
    loc = random.sample(a, 1)[0] 
    locX = loc[0]
    locY = loc[1]

    # check if legal:
    # cant be right next to an overlapped path nor out of range

    print(2, locX, cols - 2)
    print(2, locY, rows - 2)
    if not(2 <= locX < (cols - 2) and 2 <= locY < (rows - 2)): continue

    for i in range(-2, 3, 4):
        # -2, 2
        print(locX, locY)
        print(locX - i, locY)
        print(locX, locY - i)
        if (board[locX - i][locY] != 7 or board[locX][locY - i] != 7):
            isLegal = False
            print('broke it')
            break

    
    if isLegal:
        print('here')
        numOfWeaves -= 1

        # 8 = vertical path on top, 9 = horizontal path on top
        board[locX][locY] = random.randrange(8,10)

        # connecting the stuff/breaking down walls
        board[locX - 1][locY] = 7 # inLeft
        board[locX + 1][locY] = 7 # inRight
        board[locX][locY - 1] = 7 # inUp
        board[locX][locY + 1] = 7 # inDown

        posLeft = (locX - 1, locY)
        posRight = (locX + 1, locY)
        posUp = (locX, locY - 1)
        posDown = (locX, locY + 1)

        # find locations of each loc
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
            if inLeft and inRight and inUp and inDown and inLoc:
                break

        # merge the sets
        # Probably a cleaner way to do this but I'm on lack of sleep rn and feel sick have mercy
        paths[inLeft] = paths[inLeft].union(paths[inLoc])
        paths[inLeft] = paths[inLeft].union(paths[inRight])
        paths[inUp] = paths[inUp].union(paths[inLoc])
        paths[inUp] = paths[inUp].union(paths[inDown])
        paths.pop(inLoc)
        paths.pop(inDown)
        paths.pop(inRight)

for row in board:
    print(row)