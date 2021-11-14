import queue

# helper function for aStar
def h(curPos: tuple, endPos: tuple) -> int:
    # manhatten distance
    return (abs(curPos[0] - endPos[0]) + abs(curPos[1] - endPos[1]))

# Referenced wikipedia for pseudocode
# https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode

def aStar(curPos: tuple, endPos: tuple, gameMap: list) -> list:
    
    # want a priority queue for getting the locations
    q = queue.PriorityQueue()

    # add the start node
    q.put(0, curPos)

    # a place to store our g and f values in case they need changing later
    # make sure to initialize the values of each spot to infinity
    g_val = {loc : float("inf") for row in gameMap for loc in row}
    g_val[curPos] = 0
    f_val = {loc : float("inf") for row in gameMap for loc in row}
    f_val[curPos] = h(curPos, endPos)
    
    # a place to check where a node came from (needed to retrace our steps)
    prevNode = {}

    # have a set for visited nodes
    visited = set(curPos)

    while not q.empty():

        # get the position of the item with the lowest f-value
        cur = q.get()[1]

        




# calls aStar to find the next position for the mob to move
def getNextPos(curPos, endPos) -> tuple:
    return aStar(curPos, endPos)[-2]


