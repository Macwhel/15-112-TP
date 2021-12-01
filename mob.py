
class Mob:

    def __init__(self, x, y, rad, moveFreq, id):
        self.x = x
        self.y = y
        self.rad = rad
        self.moveFreq = moveFreq
        self.id = id # for debugging

    def __repr__(self): # for debugging mostly
        return f'({self.y}, {self.x}), {self.id}'

class BattleMob:

    def __init__(self, y, x, rad, d, maxHealth, money, damage):
        self.y = y
        self.x = x
        self.rad = rad
        self.d = d
        self.maxHealth = self.curHealth = maxHealth
        self.money = money
        self.dmg = damage

    def __repr__(self): # for debugging mostly
        return f'Position: ({self.y}, {self.x}). Current Health: {self.curHealth}'

class Boss:
    def __init__(self, y, x, rad, speed, maxHealth, money, damage, rateOfFire, defense):
        self.y = y
        self.x = x
        self.rad = rad
        self.speed = speed
        self.maxHealth = self.curHealth = maxHealth
        self.money = money
        self.damage = damage
        self.rateOfFire = rateOfFire
        self.defense = defense
        self.color = 'dark red'

class bossProjectile:
    def __init__(self, y, x, rad, speed, maxHealth, damage, dy, dx):
        self.y = y
        self.x = x
        self.rad = rad
        self.speed = speed
        self.maxHealth = self.curHealth = maxHealth
        self.color = 'dark red'
        self.damage = damage
        self.dy = dy
        self.dx = dx

    def getNextPos(self, width, height) -> None:
        yJump = self.dy * self.speed
        newY = self.y + yJump

        xJump = self.dx * self.speed
        newX = self.x + xJump

        if (newY - self.rad) < 0:
            remToMove = abs(newY)
            newY = self.rad + remToMove
            self.dy *= -1
            self.speed *= 1.1
        elif (newY + self.rad) > height:
            inBoundsMovement = height - self.rad - self.y
            remToMove = yJump - inBoundsMovement
            newY = height - self.rad + remToMove
            self.dy *= -1
            self.speed *= 1.1

        if (newX - self.rad) < 0:
            remToMove = newX
            newX = self.rad + remToMove
            self.dx *= -1
            self.speed *= 1.1
        elif (newX + self.rad) > width:
            inBoundsMovement = width - self.rad - self.x
            remToMove = xJump - inBoundsMovement
            newX = width - self.rad + remToMove
            self.dx *= -1
            self.speed *= 1.1

        self.y = newY
        self.x = newX
        