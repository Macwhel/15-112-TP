from astar import *
<<<<<<< HEAD

gameBoard = [
    [0,0,0,0],
    [7,7,7,7],
    [7,0,0,7],
    [7,7,7,7]
]

a = aStar((3,1), (3,3), gameBoard)
=======



gameBoard = [
    [7,0,7],
    [7,7,7],
    [7,0,0],
]

a = aStar((1,2), (0,2), gameBoard)
print(a)
>>>>>>> 8b01b76a7e834a9d0cc199c98b7a6b5761e9c654
print(a[-1])
# expect: (2, 0), (1, 0), (1, 1), (1, 2), (0,2) in reverse
