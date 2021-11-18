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
    q.put((0, curPos))

    # a place to store our g and f values in case they need changing later
    # make sure to initialize the values of each spot to infinity
    g_val = {(i, j) : float("inf") for i in range(len(gameMap)) for j in range(len(gameMap[0]))}
    f_val = {(i, j) : float("inf") for i in range(len(gameMap)) for j in range(len(gameMap[0]))}

    # initialize the start g and f vals for future use
    g_val[curPos] = 0
    f_val[curPos] = h(curPos, endPos)
    
    # a place to check where a node came from (needed to retrace our steps)
    prevNode = {}

    # have a set for visited nodes
    visited = set(curPos)

    while not q.empty():

        # get the position of the item with the lowest f-value
        #print(q.get())
        cur = q.get()[1]

        # if we reach the end
        if cur == endPos:

            # for bugtesting
            #print(prevNode)

            # then trace back your steps
            res = []
            temp = cur
            while temp != curPos:
                res.append(temp)
                temp = prevNode[temp]
            # and return a list of the direction
            return res

        # get all the legal neighbors
        directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        legalNeighbors = []

        for r,c in directions:
            newY = cur[0] + r
            newX = cur[1] + c

            if (newY in range(len(gameMap)) and newX in range(len(gameMap[0]))
                and gameMap[newY][newX] == 7):
                legalNeighbors.append((newY, newX))

        for nei in legalNeighbors:
            tempGScore = g_val[cur] + 1
            if tempGScore < g_val[nei]:
                g_val[nei] = tempGScore
                prevNode[nei] = cur
                f_val[nei] = g_val[nei] + h(nei, endPos)
                if nei not in visited:
                    q.put((f_val[nei], nei))
                    visited.add(nei)
    return curPos

# calls aStar to find the next position for the mob to move
def getNextPos(curPos, endPos, gameMap) -> tuple:
    res = aStar(curPos, endPos, gameMap)
    if type(res) == tuple:
        return res
    else:
        return res[-1]



