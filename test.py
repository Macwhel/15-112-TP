from astar import *
import sys
print(f'"{sys.executable}" -m pip install pillow')
print(f'"{sys.executable}" -m pip install requests')


gameBoard = [
    [0,0,7],
    [7,7,7],
    [7,0,0],
]

a = aStar((2,0), (0,2), gameBoard)
print(a[-1])
# expect: (2, 0), (1, 0), (1, 1), (1, 2), (0,2) in reverse
