
class Mob:

    def __init__(self, x, y, rad, moveFreq):
        self.x = x
        self.y = y
        self.rad = rad
        self.moveFreq = moveFreq

class BattleMob:

    def __init__(self, y, x, rad, d, curHealth, maxHealth):
        self.y = y
        self.x = x
        self.rad = rad
        self.d = d
        self.curHealth = curHealth
        self.maxHealth = maxHealth