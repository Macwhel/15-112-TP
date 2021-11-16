from astar import *



gameBoard = [
    [7,0,7],
    [7,7,7],
    [7,0,0],
]

a = aStar((1,2), (0,2), gameBoard)
print(a)
print(a[-1])
# expect: (2, 0), (1, 0), (1, 1), (1, 2), (0,2) in reverse
