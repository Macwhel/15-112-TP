
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