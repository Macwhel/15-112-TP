class Player:
    def __init__(self, y, x, radius):
        self.x = x
        self.y = y
        self.color = 'yellow'
        self.radius = radius

    def setY(self, newY):
        self.y = newY

    def setX(self, newX):
        self.x = newX

    def getY(self):
        return self.y

    def getX(self):
        return self.x