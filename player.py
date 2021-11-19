class Player:
    def __init__(self, y, x, radius, health = 0, dmg = 0):
        self.x = x
        self.y = y
        self.color = 'yellow'
        self.radius = radius
        self.health = health
        self.dmg = dmg


    def setY(self, newY):
        self.y = newY

    def setX(self, newX):
        self.x = newX

    def getY(self):
        return self.y

    def getX(self):
        return self.x

    def loc(self):
        return (self.y, self.x)