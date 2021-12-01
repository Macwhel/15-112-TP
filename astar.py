import queue
import math

#make a priority queue method thing for more lines of code

class PriorityQueue():
    def __init__(self):
        self.list1 = []
        self.list2 = []


# helper function for aStar
def h(curPos: tuple, endPos: tuple) -> int:
    # manhatten distance
    return (abs(curPos[0] - endPos[0]) + abs(curPos[1] - endPos[1]))

def e(curPos: tuple, endPos: tuple) -> int:
    # euclidean distance
    return ((curPos[0] - endPos[0])**2 + (curPos[1] - endPos[1])**2)**0.5
# Referenced wikipedia for pseudocode
# https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
# Referenced youtube videos for pseudocode 
# https://youtu.be/-L-WgKMFuhE?t=481
# https://www.youtube.com/watch?v=JtiK0DOeI4A

def aStar(curPos: tuple, endPos: tuple, gameMap: list) -> list:

    # want a priority queue for getting the locations (recommended)
    q = queue.PriorityQueue()

    # add the start node
    q.put((0, curPos))

    # a place to store our g and f values in case they need changing later
    # make sure to initialize the values of each spot to infinity
    gVal = {(i, j) : float("inf") for i in range(len(gameMap)) for j in range(len(gameMap[0]))}
    fVal = {(i, j) : float("inf") for i in range(len(gameMap)) for j in range(len(gameMap[0]))}

    # initialize the start g and f vals for future use
    gVal[curPos] = 0
    fVal[curPos] = h(curPos, endPos)
    
    # a place to check where a node came from (needed to retrace our steps)
    prevNode = {}

    # have a set for visited nodes
    visited = set(curPos)

    # did not follow pseudocode from here (didn't like the ways I found online)
    while not q.empty():

        # get the position of the item with the lowest f-value
        # print(q.get())
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
                and gameMap[newY][newX] != 0):
                legalNeighbors.append((newY, newX))

        for nei in legalNeighbors:
            tempGScore = gVal[cur] + 1
            if tempGScore < gVal[nei]:
                gVal[nei] = tempGScore
                prevNode[nei] = cur
                fVal[nei] = gVal[nei] + h(nei, endPos)
                if nei not in visited:
                    q.put((fVal[nei], nei))
                    visited.add(nei)
    return curPos

# calls aStar to find the next position for the mob to move
def getNextPos(curPos, endPos, gameMap) -> tuple:
    res = aStar(curPos, endPos, gameMap)
    return res[-1] if res else curPos

# simple get next position
def simpleGetNextPos(start: tuple, end: tuple, jumpDistance: int) -> tuple:
    startY, startX = start[0], start[1]
    endY, endX = end[0], end[1]

    # find norm or smth I forgot what it's called
    yDiff = endY - startY
    xDiff = endX - startX

    norm = math.sqrt(yDiff ** 2 + xDiff ** 2)
    if norm == 0:
        return (startY, startX)
        
    unitVec = (yDiff / norm, xDiff / norm)

    distance = (jumpDistance * unitVec[0], jumpDistance * unitVec[1])

    return (start[0] + distance[0], start[1] + distance[1])



    

    
