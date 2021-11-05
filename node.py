#each cell on the board will be a node

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node():
    def __init__(self, r, c, width, totalRows):
        self.r = r
        self.c = c
        self.y = r * width
        self.x = c * width
        self.color = GREY
