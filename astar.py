import queue

def h(curPos: tuple, endPos: tuple) -> int:
    return (abs(curPos[0] - endPos[0]) + abs(curPos[1] - endPos[1]))

# Referenced wikipedia for pseudocode
# https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode

def aStar(curPos, endPos, gameMap) -> list:
    pass
    


# calls aStar to find the next position for the mob to move
def getNextPos(curPos, endPos) -> tuple:
    return aStar(curPos, endPos)[-2]


