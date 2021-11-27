import random
import copy

rows = cols = 5

def pprintBoard(board: list) -> None:
    for row in board:
        print(row)

# init board
r1 = [1 if i % 2 == 0 else 0 for i in range(cols)]
r2 = [0 for i in range(cols)]
board = [copy.deepcopy(r1) if i % 2 == 0 else copy.deepcopy(r2) for i in range(rows)]
pprintBoard(board)
directions = [
    [-2, 0], # up
    [2,0], # down
    [0,-2], # left
    [0,2] # right
    ]
a = ['a','b','c','d','e','f','g','h','i']
random.shuffle(a)

'''
[1, 1, 1, 0, 1]
[0, 0, 1, 0, 0]
[1, 1, 1, 0, 1]
[0, 0, 0, 0, 0]
[1, 0, 1, 0, 1]
'''

paths = [{(i, j)} for j in range(0, cols, 2) for i in range(0, rows, 2)]
locations = {(i, j) for j in range(0, cols, 2) for i in range(0, rows, 2)}

#print(paths, len(paths))

'''paths[0] = paths[0].union(paths[1])
paths.pop(1)
print(paths, len(paths))
print(paths[0])'''
# 1: choose a random 1

# 2: randomly get the directions

# 3: if there's something that's not connected, (aka there's a 0 in between)

# 3a: check if it's in the set that this location is also in

# if so, check another direction and repeat from 3

# 3b: if it's not, add it to the set

# 4: update the board

# keep it going until len of the set is 1

while len(paths) > 1:
    # 1
    # getting random method idea from stack overflow
    # https://stackoverflow.com/questions/44605255/what-is-the-most-pythonic-way-to-pop-a-random-element-from-a-set-in-python3-6
    loc = random.sample(locations, 1)[0]
    locations.discard(loc)
    print(loc)
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
                elif loc in path:
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
            print(loc, newLoc, (midY, midX))
            board[midY][midX] = 1

            break

            
        

    # couldn't find a legal direction 
    # it'll happen for at least one cell every generation
    if not newLoc: 
        # find a new location by starting the while loop again
        # continue
        pass

    pprintBoard(board)
    print(paths, len(paths))






'''while len(paths) > 1:
    # 1
    index = random.randrange(len(paths))

    # 1a

<<<<<<< HEAD
    if len(paths[index] > 1):
        index2 = random.randrange(len(paths[index]))
=======
# get a random cell
# connect it with another cell

r, c = random.randrange(rows), random.randrange(cols)


>>>>>>> ce1ef08a26cb427eeaa889cd02096c04701c6dd4

    loc = paths[index][index2]

    # 2
    random.shuffle(directions)
    for d in directions:
        newLoc = '''