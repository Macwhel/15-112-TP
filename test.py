from astar import *

gameBoard = [
    [0,0,0,0],
    [7,7,7,7],
    [7,0,0,7],
    [7,7,7,7]
]

a = aStar((3,1), (3,3), gameBoard)
print(a[-1])
# expect: (2, 0), (1, 0), (1, 1), (1, 2), (0,2) in reverse
