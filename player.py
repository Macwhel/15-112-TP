# initializing the player class

class Player:
    def __init__(self, y, x, radius, money = 0, health = 100, dmg = 0, speed = 0, defense = 0):
        self.x = x
        self.y = y
        self.color = 'yellow'
        self.radius = radius
        self.maxHealth = self.curHealth = health
        self.dmg = dmg
        self.money = money
        self.defense = defense
        self.critRate = 0
        self.critDmg = 1.5
        self.speed = speed

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