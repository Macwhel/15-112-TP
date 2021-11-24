class Player:
    def __init__(self, y, x, radius, money, health = 100, dmg = 0, defense = 0):
        self.x = x
        self.y = y
        self.color = 'yellow'
        self.radius = radius
        self.maxHealth = self.curHealth = health
        self.dmg = dmg
        self.money = money
        self.defense = defense

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