from cmu_112_graphics import *
from player import *
from map import *
from rectangle import *
from mob import *
from astar import *
from items import *

# all the tkinter material

# Screens concept from lecture notes (not sure if I needed to cite this but better safe than sorry)
# No code was copy pasted from outside sources

def initBossFight(app):
    app.canDamageBoss = False
    bp = app.battlePlayer
    app.initialRad = bp.radius
    app.initialSpeed = bp.speed
    bp.radius /= 2
    bp.speed /= 3
    app.timerDelay = 100
    app.bossBattleCounter = 0
    app.bossBattleCounter2 = 0
    level = app.level
    diff = app.difficultyNum
    app.boss = Boss(- app.height / 3, # y coord
                    app.width / 2, # x coord
                    app.width / 2, # radius
                    0, # speed
                    1000 * app.difficultyNum, # maxHealth
                    2000 * app.level, # money drop
                    9999, # dmg if you touch it
                    20, # rate of fire in 100ms
                    2 * app.level * app.difficultyNum) # flat defense

    app.bossProjectileList = []

def bossFight_redrawAll(app, canvas):
    # draw boss
    b = app.boss
    rp = app.player
    canvas.create_oval(b.x - b.rad, b.y - b.rad,
                        b.x + b.rad, b.y + b.rad,
                        fill = b.color, width = 10)

    # draw "bullets"
    for p in app.bossProjectileList:
        canvas.create_oval(p.x - p.rad, p.y - p.rad,
                            p.x + p.rad, p.y + p.rad,
                            fill = p.color, width = 4)

    # draw character
    bp = app.battlePlayer
    canvas.create_oval(
        bp.x - bp.radius,
        bp.y - bp.radius,
        bp.x + bp.radius,
        bp.y + bp.radius,
        fill = "yellow"
    )

    canvas.create_text(app.width / 4, app.height / 9,
                        text = f'Dmg Multiplier: {app.dmgMult}x', font = 'Cambria 13 bold')
    canvas.create_text(3 * app.width / 4, app.height / 9,
                        text = f'Health: {int(rp.curHealth)} / {int(rp.maxHealth)}', font = 'Cambria 13 bold')
    canvas.create_text(app.width / 2, app.height / 20,
                        text = f'Boss Health: {((b.curHealth / b.maxHealth) * 100):.2f}%')

def beatBoss(app):
    app.mode = "Shop"
    app.items = rerollItems(app.difficulty, app.level)
    app.player.money += app.boss.money 
    app.timerDelay = app.defaultTimer
    bp = app.battlePlayer
    bp.speed *= 3
    bp.radius *= 3
    bp.y, bp.x = 3 * app.height / 4, app.width / 2

def bossFight_mousePressed(app, event):
    bp = app.battlePlayer
    B = app.boss
    # clicking on boss = dealing damage
    if app.canDamageBoss and e((event.y, event.x), (B.y, B.x) ) < (B.rad):
        app.combo += 1
        app.dmgMult = min(max(app.combo // (8 - app.difficultyNum), 1), app.maxCombo) 
        critDmg = 1
        critRoll = random.randrange(100)
        if critRoll < app.battlePlayer.critRate:
            critDmg = app.battlePlayer.critDmg
        B.curHealth -= (bp.dmg * critDmg) ** app.dmgMult

        # player wins
        if app.boss.curHealth <= 0:
                beatBoss(app)

    # clicking on bullets = removing them
    for i, p in enumerate(app.bossProjectileList):
        if e( (event.y, event.x), (p.y, p.x) ) < p.rad:
            app.combo += 1
            app.dmgMult = min(max(app.combo // (8 - app.difficultyNum), 1), app.maxCombo) 
            critDmg = 1
            critRoll = random.randrange(100)
            if critRoll < app.battlePlayer.critRate:
                critDmg = app.battlePlayer.critDmg
            p.curHealth -= (bp.dmg * critDmg) ** app.dmgMult

            if p.curHealth < p.maxHealth / 2:
                p.color = 'pink'
                if p.curHealth <= 0:
                    app.bossProjectileList.pop(i)

def bossFight_keyPressed(app, event):
    p = app.battlePlayer
    lastCoords = (p.y, p.x)
    jumpSize = app.width / 30 
    if (event.key == 'w' or event.key == 'Up'): p.y -= jumpSize * p.speed
    if (event.key == 's' or event.key == 'Down'): p.y += jumpSize * p.speed
    if (event.key == 'd' or event.key == 'Right'): p.x += jumpSize * p.speed
    if (event.key == 'a' or event.key == 'Left'): p.x -= jumpSize * p.speed
    elif (event.key == 'p'):
        app.mode = 'pause'
        app.lastState = 'bossFight'

    # change player coords back if the space the players wants to move in is illegal
    if p.y < 0: 
        p.y = 0
    elif p.y > app.height: 
        p.y = app.height    
    
    if p.x < 0: 
        p.x = 0
    elif p.x > app.width: 
        p.x = app.width

def fireProjectile(app):
    xLocations = [app.width / 4, app.width / 2, 3 * app.width / 4]
    random.shuffle(xLocations)
    for i in range(app.difficultyNum):
        dy = random.randint(3, 8) 
        dx = ((10**2 - dy**2)**0.5) * random.randrange(-1, 2, 2)
        projectile = bossProjectile(app.height / 10, # y coord
                                    xLocations.pop(0), # x coord
                                    app.width / 25, # radius
                                    2 * app.difficultyNum, # speed
                                    8 * app.difficultyNum, # health
                                    5 * app.difficultyNum, # damage
                                    dy / 2.5,
                                    dx / 2.5)
        app.bossProjectileList.append(projectile)

def bossFight_timerFired(app):
    bp = app.battlePlayer
    app.bossBattleCounter += 1
    app.bossBattleCounter2 += 1
    if app.bossBattleCounter2 % 50 == 0:
        app.canDamageBoss = True
        app.boss.color = 'pink'
    elif app.bossBattleCounter2 % 70 == 0:
        app.canDamageBoss = False
        app.boss.color = "dark red"
    for p in app.bossProjectileList:
        oldPos = (p.y, p.x)
        p.getNextPos(app.width, app.height)
        if e( (p.y, p.x), (bp.y, bp.x) ) < (p.rad + bp.radius):
            bp.curHealth -= max(p.damage - bp.defense, 0)
            if bp.curHealth <= 0:
                app.mode = 'gameOver'
    
    if (len(app.bossProjectileList) < (5 * app.difficultyNum) and 
        app.bossBattleCounter % app.boss.rateOfFire == 0):
        fireProjectile(app)

#########################################################

def startScreen_redrawAll(app, canvas):
    canvas.create_text(app.width / 2, app.height / 16, text = 'Select your difficulty', font = "Cambria 35 bold")
    canvas.create_rectangle(app.width / 3, 4 * app.height / 20, 2 * app.width / 3, 7 * app.height / 20, fill = "blue")
    canvas.create_rectangle(app.width / 3, 9 * app.height / 20, 2 * app.width / 3, 12 * app.height / 20, fill = "blue")
    canvas.create_rectangle(app.width / 3, 14 * app.height / 20, 2 * app.width / 3, 17 * app.height / 20, fill = "blue")
    canvas.create_text(app.width / 2, 5.5 * app.height / 20, text = "Easy", font = "Cambria 16 bold", fill = "light green")
    canvas.create_text(app.width / 2, 10.5 * app.height / 20, text = "Medium", font = "Cambria 16 bold", fill = "yellow")
    canvas.create_text(app.width / 2, 15.5 * app.height / 20, text = "Hard", font = "Cambria 16 bold", fill = "red")

def startScreen_mousePressed(app, event):
    if (app.width / 3) < event.x < (2 * app.width / 3):
        if (4 * app.height / 20) < event.y < (7 * app.height / 20):
            app.difficulty = 'Easy'
            initGame(app)
        elif (9 * app.height / 20) < event.y < (12 * app.height / 20):
            app.difficulty = "Medium"
            initGame(app)
        elif (14 * app.height / 20) < event.y < (17 * app.height / 20):
            app.difficulty = "Hard"
            initGame(app)

#########################################################

def pause_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'light blue')
    canvas.create_text(app.width / 2, app.height / 6, 
                        text = "Press Space Bar to Continue", 
                        font = "Cambria 23 bold")
    canvas.create_text(app.width / 2, app.height / 2,
                        text = "If you encounter the very rare \nunsolvable maze, press b to get a new maze",
                        font = "Cambria 23 bold")
    canvas.create_text(app.width / 2, app.height * 3 / 4,
                        text = 'Press r to reset the game',
                        font = "Cambria 23 bold")

def pause_keyPressed(app, event):
    if event.key == 'Space':
        app.mode = app.lastState
    elif event.key == 'b':
        resetLevel(app)
        app.mode = 'Travel'
    elif event.key == 'r':
        app.mode = 'startScreen'

#########################################################

# no time to make this yet
def tutorial_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "light blue")

    canvas.create_text(app.width / 2, app.height / 6, text = 'Basic Rules:', font = "Cambria 32 bold")

def tutorial_keyPressed(app, event):
    if event.key == 'Right': app.mode = 'tutorial1'
    if event.key == "Space": 
        app.mode = app.lastState = 'Travel'

def tutorial_mousePressed(app, event):
    loc = (event.y, event.x)
    
    # if it ever clicks on this on this one part of the screen, then go straight to the game
    app.mode = app.lastState = 'Travel'

#########################################################

def gameOver_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
    canvas.create_text(app.width / 2, app.height / 2, fill = 'Red', text = "GAME OVER", font = "Cambria 35 bold")
    canvas.create_text(8 * app.width / 9, app.height / 35, fill = 'Red', text = "Press 'R' to restart", font = "Cambria 16 bold")

def gameOver_keyPressed(app, event):
    if event.key == 'r':
        app.mode = 'startScreen'

#########################################################

def Shop_redrawAll(app, canvas):
    # background
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "light blue")

    if app.lastState == 'Travel': 
        text = f'Level {app.level} Completed'
    else:
        levelBoss = app.level // 3
        if levelBoss == 1:
            aText = 'st'
        elif levelBoss == 2:
            aText = 'nd'
        else:
            aText = 'rd'
        text = f'{levelBoss}{aText} Boss Fight Completed'
    canvas.create_text(app.width / 2, app.height / 20, text = f'Level {app.level - 1} Completed', font = "Cambria 32 bold")
    canvas.create_text(app.width / 2, app.height / 8, text = 'Shop', font = "Cambria 25 bold")
    canvas.create_text(app.width / 2, app.height / 6, text = "Press Space to Continue", font = 'Cambria 20 bold')

    # show the player's health and money so they know what they should/can buy
    p = app.player
    bp = app.battlePlayer
    canvas.create_text(app.width / 6, 28 * app.height / 30,
                        text = f'Health: {int(p.curHealth)} / {p.maxHealth}', font = 'Cambria 13 bold')
    canvas.create_text(app.width / 6, 29 * app.height / 30,
                        text = f'Worms: {p.money}', font = 'Cambria 13 bold')
    canvas.create_text(app.width / 2, 28.5 * app.height / 30,
                        text = f"Stats: \nAttack: {bp.dmg} \t Crit Rate: {bp.critRate}% \t Crit Damage {bp.critDmg * 100}% \nSpeed: {bp.speed} \t Damage Reduction: {bp.defense}",
                        font = "Cambria 13 bold")
    
    m = p.money

    # Reroll Button
    rColor = 'green' if m >= 50 else 'gray'
    canvas.create_rectangle(1.05 * app.width / 12, 1.25 * app.height / 5, 2.85 * app.width / 12, 1.55 * app.height / 5, fill = rColor)
    canvas.create_text(app.width / 6, 1.4 * app.height / 5, text = "Reroll Shop: \n 50 Worms", font = "Cambria 16 bold")

    # Damage Item
    dColor = 'green' if m >= app.items[0][1][0] else 'gray'
    canvas.create_text(app.width / 6, 2 * app.height / 5, text = "Damage:", font = "Cambria 20 bold")
    canvas.create_rectangle(0.95 * app.width / 3, 1.7 * app.height / 5, 2.05 * app.width / 3, 2.3 * app.height / 5, fill = dColor)
    canvas.create_text(app.width / 2, 2 * app.height / 5, text = f'{app.items[0][0]}: {app.items[0][1][0]} Worms', font = "Cambria 14 bold")

    # Survivability item (health, defense)
    sColor = 'green' if m >= app.items[1][1][0] else 'gray'
    canvas.create_text(app.width / 6,  3 * app.height / 5, text = "Survivability:", font = "Cambria 20 bold")
    canvas.create_rectangle(0.95 * app.width / 3, 2.7 * app.height / 5, 2.05 * app.width / 3, 3.3 * app.height / 5, fill = sColor)
    canvas.create_text(app.width / 2, 3 * app.height / 5, text = f'{app.items[1][0]}: {app.items[1][1][0]} Worms', font = "Cambria 14 bold")

    # Misc Item
    mColor = 'green' if m >= app.items[2][1][0] else 'gray'
    canvas.create_text(app.width / 6, 4 * app.height / 5, text = "Misc:", font = "Cambria 20 bold")
    canvas.create_rectangle(0.95 * app.width / 3, 3.7 * app.height / 5, 2.05 * app.width / 3, 4.3 * app.height / 5, fill = mColor)
    canvas.create_text(app.width / 2, 4 * app.height / 5, text = f'{app.items[2][0]}: {app.items[2][1][0]} Worms', font = "Cambria 14 bold")
    
def Shop_buyItem(app, itemType: int) -> None:

    # 0: dmg, 1: surv, 2: misc
    cost, effects = app.items[itemType][1][0], app.items[itemType][1][1]
    p = app.player
    pb = app.battlePlayer
    p.money -= cost

    if itemType == 0:
        pb.dmg += effects[0]
        pb.critDmg += effects[1] / 100
        pb.critRate += effects[2]
        p.maxHealth += effects[4]
        p.curHealth = min(p.maxHealth, p.curHealth + effects[3])
        pb.defense += effects[5]

    elif itemType == 1:
        p.maxHealth += effects[1]
        p.curHealth = min(p.maxHealth, p.curHealth + effects[0])
        pb.defense += effects[2]
        pb.speed = pb.speed * effects[3] if effects[3] != 0 else pb.speed
        pb.dmg += effects[4]

    else: 
        pb.speed *= effects[0]
        app.mobDropMult += effects[1]
        app.itemSpawnChanceMult += effects[2]
        app.maxCombo += effects[3]
        app.numOfMobs += effects[4]
        pb.defense += effects[5]

    app.items = rerollItems(app.difficulty, app.level - 1)

def Shop_mousePressed(app, event):

    m = app.erer.money
    # reroll button
    if (m >= 50 and
        (1.05 * app.width / 12) < event.x < (2.85 * app.width / 12) and 
        (1.25 * app.height / 5) < event.y < (1.55 * app.height / 5)):
        app.player.money -= 50
        app.items = rerollItems(app.difficulty, app.level)
    # Dmg Item
    elif (m >= app.items[0][1][0] and
            (0.95 * app.width / 3) < event.x < (2.05 * app.width / 3) and
            (1.7 * app.height / 5) < event.y < (2.3 * app.height / 5)):
            Shop_buyItem(app, 0)
    # Survival Item
    elif (m >= app.items[1][1][0] and
            (0.95 * app.width / 3) < event.x < (2.05 * app.width / 3) and
            (2.7 * app.height / 5) < event.y < (3.3 * app.height / 5)): 
            Shop_buyItem(app, 1)

    # Misc Item
    # 0.95 * app.width / 3, 3.7 * app.height / 5, 2.05 * app.width / 3, 4.3 * app.height / 5
    elif (m >= app.items[2][1][0] and
            (0.95 * app.width / 3) < event.x < (2.05 * app.width / 3) and
            (3.7 * app.height / 5) < event.y < (4.3 * app.height / 5)):
            Shop_buyItem(app, 2)

def Shop_keyPressed(app, event):
    if event.key == "Space":
        if (app.level - 1) % 3 == 0 and app.lastState != 'bossFight':
            app.mode = app.lastState = 'bossFight'
            initBossFight(app)
        else: 
            app.mode = app.lastState = 'Travel'


    elif event.key == 'p':
        app.mode = 'pause'
        app.lastState = 'Shop'

#########################################################

def Travel_redrawAll(app, canvas):
    for i in range(len(app.gameMap)):
            for j in range(len(app.gameMap[0])):
                cell = Rectangle(i * app.sW, j * app.sW, app.sW)

                if app.gameMap[i][j] == 0:
                    cell.setColor('black')
                else:
                    if (i, j) == app.gLoc:
                        cell.setColor('green')
                    else: 
                        cell.setColor('white')

                canvas.create_rectangle(cell.x, cell.y, cell.x2, cell.y2, fill = 
                                        cell.color, width = 0)

                if app.gameMap[i][j] == 9:
                    canvas.create_line(cell.x, cell.y, cell.x, cell.y2, width = 3)
                    canvas.create_line(cell.x2, cell.y, cell.x2, cell.y2, width = 6)
                elif app.gameMap[i][j] == 8:
                    canvas.create_line(cell.x, cell.y, cell.x2, cell.y, width = 3)
                    canvas.create_line(cell.x, cell.y2, cell.x2, cell.y2, width = 6)
    p = app.player

    # coords for player
    x = p.x * app.sW + (app.sW / 2)
    y = p.y * app.sW + (app.sW / 2)

    # draw player
    canvas.create_oval(
        x - p.radius,
        y - p.radius,
        x + p.radius,
        y + p.radius,
        fill = p.color)

    # draw mobs
    for mob in app.mobList:
        x = mob.x * app.sW + (app.sW / 2)
        y = mob.y * app.sW + (app.sW / 2)
        canvas.create_oval(
            x - mob.rad,
            y - mob.rad,
            x + mob.rad,
            y + mob.rad,
            fill = "red"
        )

    # draw that little border on the bottom of the map
    border = app.rows * app.sW
    canvas.create_line(0, border, app.boardHeight, border,
                        width = 3)
    canvas.create_line(border, 0, border, app.boardHeight, width = 3)

    # draw the stuff I'll use later
    canvas.create_text(app.width / 6, 39 * app.height / 40,
                        text = f'Health: {int(p.curHealth)} / {int(p.maxHealth)}', font = 'Cambria 13 bold')
    canvas.create_text(5 * app.width / 6, 39 * app.height / 40,
                        text = f'Money: {p.money}', font = 'Cambria 13 bold')
    canvas.create_text(app.width / 2, 39 * app.height / 40,
                        text = f'Level: {app.level}', font = 'Cambria 13 bold')

def Travel_timerFired(app):
    # get the next position for all mobs
    if not app.paused:
        app.travelCounter += 1
        for i, mob in enumerate(app.mobList):
                if (h((mob.y, mob.x), (app.player.y, app.player.x)) >= (app.rows // 3 * app.difficultyNum) and
                    h((app.gLoc[0], app.gLoc[1]),(app.player.y, app.player.x)) >= app.rows): # don't have mobs move until certain distance away
                    continue
                pos = getNextPos((mob.y, mob.x), (app.player.y, app.player.x), app.gameMap)
                if pos not in app.mobCoords:
                    app.mobCoords.discard((mob.y, mob.x))
                    (mob.y, mob.x) = pos # update the mob's position
                    app.mobCoords.add(pos) # update the set as well

                # Mob meets player
                elif pos == app.player.loc():
                    app.mode = 'mobFight'
                    app.timerDelay = 100
                    app.indexOfLastMobFought = i
                    app.battleMob = app.battleMobList[i]
                    app.initialBMSpeed = app.battleMob.d

def Travel_keyPressed(app, event):
    lastCoords = (app.player.y, app.player.x)

    if app.paused: app.paused = False
    if (event.key == 'w' or event.key == 'Up'): app.player.y -= 1
    elif (event.key == 's' or event.key == 'Down'): app.player.y += 1
    elif (event.key == 'd' or event.key == 'Right'): app.player.x += 1
    elif (event.key == 'a' or event.key == 'Left'): app.player.x -= 1
    elif (event.key == 'p'): 
        app.mode = 'pause'
        app.lastState = 'Travel'
    elif (event.key == 'r'):
        app.mode = 'startScreen'

    moveY, moveX = app.player.y - lastCoords[0], app.player.x - lastCoords[1]

    # for debugging purposes
    '''if (event.key == "Space"):
        for i, mob in enumerate(app.mobList):
            (mob.y, mob.x) = getNextPos((mob.y, mob.x), app.pLoc, app.gameMap)
            print(i, mob.y, mob.x, app.pLoc)'''

    # change player coords back if the space the players wants to move in is illegal
    pY = app.player.getY()
    pX = app.player.getX()
    if (pY not in range(app.rows) or pX not in range(app.cols) or 
        app.gameMap[pY][pX] == 0):
        app.player.setY(lastCoords[0])
        app.player.setX(lastCoords[1])
    elif (app.gameMap[pY][pX] == 8 or app.gameMap[pY][pX] == 9): # force the player up/down and left/right
        app.player.y += moveY
        app.player.x += moveX
    elif (pY, pX) in app.mobCoords: # player meets mob
        app.mode = 'mobFight'
        app.timerDelay = 100
        # somehow get the index of the mob in the list so you can pop it later
        for i, m in enumerate(app.mobList):
            if (m.y, m.x) == (pY, pX): # you know it's in there so no need for an else case
                app.indexOfLastMobFought = i
                app.battleMob = app.battleMobList[i]
                app.initialBMSpeed = app.battleMob.d

    # Check if player reached goal
    elif (pY, pX) == app.gLoc:
        beatLevel(app)

#########################################################

def mobFight_timerFired(app):
    app.counter += 1
    m = app.battleMob
    p = app.battlePlayer
    nextPos = simpleGetNextPos((m.y, m.x), (p.y, p.x), int(m.d * app.difficultyNum ** 0.85))
    # make sure the mob goes away from the player kinda like a knockback or so the mob doesn't just stick on you
    '''if app.counter - app.beenHitCounter <= 5 and app.beenHitCounter != 0:
        nextPos = (nextPos[0] - 10, nextPos[1] - 10)'''
    # nvm the mechanic isn't working out and I don't care
    (m.y, m.x) = nextPos
    if ((m.y - m.rad) < p.y < (m.y + m.rad) and 
        (m.x - m.rad) < p.x < (m.x + m.rad)): # mob touches player
        dmgDealt = max((m.dmg - p.defense), 0)
        p.curHealth -= dmgDealt
        app.player.curHealth -= dmgDealt
        if app.player.curHealth <= 0:
            app.mode = 'gameOver'
        elif app.player.curHealth <= 20:
            app.player.dmg *= 2
        # same methods as above when you defeat it, but this time you
        # also take damage. Perhaps I make a method for this too.
        # have it be inside another function, maybe appStarted so I can
        # use all the variables
        index = app.indexOfLastMobFought
        m = app.mobList[index]
        app.mobCoords.discard((m.y, m.x))
        app.mobList.pop(index)
        app.battleMobList.pop(index)
        app.mode = 'Travel' if app.mode != 'gameOver' else 'gameOver'
        app.paused = True
        app.timerDelay = app.defaultTimer
        app.battlePlayer.y, app.battlePlayer.x = 3 * app.height / 4, app.width / 2 # reset position
        #app.beenHitCounter = app.counter

    
    # change up the speed of the mob so it's not boring

    if app.initialBMSpeed == app.battleMob.d:
        a = random.randint(1, 14 - app.difficultyNum)
        if a == 1:
            app.battleMob.d *= 8
            app.counter = 0
    else:
        if app.counter >= 24:
            app.battleMob.d = app.initialBMSpeed

def mobFight_mousePressed(app, event):
    app.cx = event.x
    app.cy = event.y
    
    tempY = app.battleMob.y
    tempX = app.battleMob.x
    tempRad = app.battleMob.rad

    if ((tempY - tempRad) < app.cy < (tempY + tempRad) 
        and (tempX - tempRad) < app.cx < (tempX + tempRad)): 
        # if the mouse is on the mob
        app.hitCounter += 1
        app.combo += 1
        app.dmgMult = min(max(app.combo // (8 - app.difficultyNum), 1), app.maxCombo) # this is so the dmg is never 0 and doesn't go to infinity (combo caps at maxCombo)
        critDmg = 1
        critRoll = random.randrange(100)
        if critRoll < app.battlePlayer.critRate:
            critDmg = app.battlePlayer.critDmg
        app.battleMob.curHealth -= (app.battlePlayer.dmg * critDmg) ** app.dmgMult

        # basically check if you killed the mob, maybe insert a little
        # transition later
        if app.battleMob.curHealth <= 0:
            app.player.money += app.battleMob.money
            index = app.indexOfLastMobFought
            m = app.mobList[index]
            app.mobCoords.discard((m.y, m.x))
            app.mobList.pop(index)
            app.battleMobList.pop(index)
            app.mode = 'Travel'
            app.paused = True
            app.timerDelay = app.defaultTimer
            app.battlePlayer.y, app.battlePlayer.x = 3 * app.height / 4, app.width / 2

    else:
        # missed, so counter goes down
        app.combo = max(app.combo - (app.combo // (8 - app.difficultyNum)), (8 - app.difficultyNum))
        app.dmgMult = min(max(app.combo // (8 - app.difficultyNum), 1), app.maxCombo)

def mobFight_keyPressed(app, event):
    p = app.battlePlayer
    lastCoords = (p.y, p.x)
    jumpSize = app.width / 30 
    if (event.key == 'w' or event.key == 'Up'): p.y -= jumpSize * p.speed
    if (event.key == 's' or event.key == 'Down'): p.y += jumpSize * p.speed
    if (event.key == 'd' or event.key == 'Right'): p.x += jumpSize * p.speed
    if (event.key == 'a' or event.key == 'Left'): p.x -= jumpSize * p.speed
    elif (event.key == 'p'):
        app.mode = 'pause'
        app.lastState = 'mobFight'

    # change player coords back if the space the players wants to move in is illegal
    if p.y < 0: 
        p.y = 0
    elif p.y > app.height: 
        p.y = app.height    
    
    if p.x < 0: 
        p.x = 0
    elif p.x > app.width: 
        p.x = app.width

def mobFight_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "white")

    # draw mob
    m = app.battleMob
    canvas.create_rectangle(
        m.x - m.rad, 
        m.y - m.rad,
        m.x + m.rad,
        m.y + m.rad,
        fill = "red")

    # draw player
    p = app.battlePlayer
    canvas.create_oval(
        p.x - p.radius,
        p.y - p.radius,
        p.x + p.radius,
        p.y + p.radius,
        fill = "yellow"
    )

    canvas.create_text(app.width / 4, app.height / 9,
                        text = f'Dmg Multiplier: {app.dmgMult}x', font = 'Cambria 13 bold')
    canvas.create_text(3 * app.width / 4, app.height / 9,
                        text = f'Health: {int(p.curHealth)} / {int(p.maxHealth)}', font = 'Cambria 13 bold')
    canvas.create_text(app.width / 2, app.height / 20,
                        text = f'Mob Health: {((m.curHealth / m.maxHealth) * 100):.2f}%')

#########################################################

def resetLevel(app):
    mapType = randomMap()
    app.mapTypeNum = app.maps.index(mapType)
    if mapType == "Kruskals":
        app.gameMap, app.pLoc, app.gLoc, mLocs = Kruskals((app.rows, app.cols))
    elif mapType == 'KruskalsWeave':
        app.gameMap, app.pLoc, app.gLoc, mLocs = KruskalsWeave((app.rows, app.cols))
    else:
        app.gameMap, app.pLoc, app.gLoc, mLocs = createMap(
            (app.rows, app.cols), int(app.difficultyNum * (app.rows)), app.rows // 1.5)
            
    app.player.y, app.player.x = app.pLoc
    app.paused = True
    app.travelCounter = 0
    app.sW = min(app.width / app.rows, app.boardHeight / app.rows)
    app.boardHeight = 0.9 * app.height
    app.mobListLoc = random.sample(mLocs, app.numOfMobs)
    app.mobList = [Mob(m[1], m[0], app.sW / 3, 10, i) for i, m in enumerate(app.mobListLoc)]
    app.mobCoords = {(i[0], i[1]) for i in app.mobListLoc}
    app.battleMobList = [BattleMob(app.height / 4, 
                                    app.width / 2, 
                                    app.sW * 1.5, 
                                    int(app.level * app.difficultyNum ** 0.75), 
                                    25, 
                                    100 * app.mobDropMult, 20) for i in app.mobList]
    app.player.radius = app.sW / 3

def beatLevel(app):
    mn = app.mapTypeNum
    if mn == 0: expectedTime = app.rows * 10 # aka 1.2app.rows seconds
    elif mn == 1: expectedTime = app.rows * app.cols / 2
    elif mn == 2: expectedTime = app.rows * app.cols
    timeBonus = min(int( 100 * app.level * (expectedTime / app.travelCounter) ), 200 * app.level) # have min so it's not tooooo big
    app.travelCounter = 0
    app.player.money += 100 * app.level + timeBonus
    app.level += 1
    app.rows += app.difficultyNum # change this number later
    app.cols = app.rows
    app.noticeRange = (app.rows // 3 * app.difficultyNum)
    app.numOfMobs = max(app.numOfMobs, int(app.difficultyNum * (app.rows**2 / 150)))
    # now change all the variables that create the board and stuff as well as get new positions
    mapType = randomMap()
    app.mapTypeNum = app.maps.index(mapType)
    if mapType == "Kruskals":
        app.gameMap, app.pLoc, app.gLoc, mLocs = Kruskals((app.rows, app.cols))
    elif mapType == 'KruskalsWeave':
        app.gameMap, app.pLoc, app.gLoc, mLocs = KruskalsWeave((app.rows, app.cols))
    else:
        app.gameMap, app.pLoc, app.gLoc, mLocs = createMap(
            (app.rows, app.cols), int(app.difficultyNum * (app.rows)), app.rows // 1.5)
        app.numOfMobs += app.difficultyNum
    # perhaps it's 2 + (level // 2) + something abt difficulty
    # don't forget that we need to change the player location as well
    app.player.y, app.player.x = app.pLoc
    
    # give the player some breathing room
    app.paused = True
    app.mode = "Shop"
    app.items = rerollItems(app.difficulty, app.level)

    # Essentially do all the stuff we did for the initializing thing
    # Make a helper function that gets all this stuff for us because
    # the code is super messy
    app.sW = min(app.width / app.rows, app.boardHeight / app.rows)
    app.boardHeight = 0.9 * app.height
    app.mobListLoc = random.sample(mLocs, app.numOfMobs)
    app.mobList = [Mob(m[1], m[0], app.sW / 3, 10, i) for i, m in enumerate(app.mobListLoc)]
    app.mobCoords = {(i[0], i[1]) for i in app.mobListLoc}
    app.battleMobList = [BattleMob(app.height / 4, 
                                    app.width / 2, 
                                    app.sW * 1.5, 
                                    int(app.level * app.difficultyNum ** 0.75), 
                                    25, 
                                    100 * app.mobDropMult, 20) for i in app.mobList]
    app.player.radius = app.sW / 3

def initGame(app):

    app.difficultyList = ['Easy', 'Medium', "Hard"] # default list
    app.difficultyNum = app.difficultyList.index(app.difficulty) + 1
    app.rows, app.cols = (15 + app.difficultyNum, 15 + app.difficultyNum) # determine board size
    app.timerDelay = app.defaultTimer = 250 # default 250ms
    app.boardHeight = 0.9 * app.height # to fit everything
    app.initsW = app.sW = min(app.width / app.rows, app.boardHeight / app.rows) # based on yeah
    #app.mode = 'tutorial' # start at tutorial
    app.mode = 'Travel'
    app.paused = True # default paused
    mapType = randomMap() # get map
    app.itemSpawnChanceMult = 1 # default 1
    app.lastState = 'Travel' # default nothing
    app.numOfMobs = max((app.rows**2) // 150, 1) # formula for num of mobs
    app.level = 1 # default 1
    app.noticeRange = (app.rows // 3 * app.difficultyNum)


    # get number representation of difficulty

    app.maxCombo = 4 + app.difficultyNum # init max combo
    app.items = rerollItems(app.difficulty, app.level) # init items
    app.mobDropMult = app.level * app.difficultyNum # init base mobDropMult
    
    # initilalize map and then get start locations for player and end goal as
    # well as acceptable mob locations
    # Adjust maxTuns and maxLen scalings on difficulty****
    app.maps = ["Random Walker", "Kruskals", "KruskalsWeave"]
    if mapType == "Kruskals":
        app.gameMap, app.pLoc, app.gLoc, mLocs = Kruskals((app.rows, app.cols))
    elif mapType == 'KruskalsWeave':
        app.gameMap, app.pLoc, app.gLoc, mLocs = KruskalsWeave((app.rows,app.cols))
    else:
        '''maxTuns = int((app.difficultyNum ** 0.5) * (app.rows + app.cols))
        maxLen = int((app.difficultyNum ** 0.5) * app.rows // 1.5)'''
        app.gameMap, app.pLoc, app.gLoc, mLocs = createMap(
            (app.rows, app.cols), int(app.difficultyNum * (app.rows)), app.rows // 1.5)
        app.numOfMobs += app.difficultyNum
    app.mapTypeNum = app.maps.index(mapType)

    # init overall player
    app.player = Player(app.pLoc[0], app.pLoc[1], app.sW / 3)

    # make a list of unique mob spawning locations
    app.mobListLoc = random.sample(mLocs, min(len(mLocs), app.numOfMobs)) # fix this

    # create a list of mob classes for travel board
    app.mobList = [Mob(m[1], m[0], app.sW / 3, 10, i) for i, m in enumerate(app.mobListLoc)]

    # create a list of battle mobs for battle instance
    app.battleMobList = [BattleMob(app.height / 4, app.width / 2, app.initsW * 1.5 / app.level, 
                            int(app.level * app.difficultyNum ** 0.75), 25 * app.difficultyNum, 
                            100 * app.mobDropMult, 20) for i in app.mobList]

    # have a set to keep track of the coords so the mobs don't overlap
    app.mobCoords = {(i[0], i[1]) for i in app.mobListLoc}

    # have the initial speed somewhere
    app.initialBMSpeed = app.battleMobList[0].d 

    # always helpful to keep track
    app.counter = 0
    app.travelCounter = 0

    # player for the fights, no change based on difficulty
    app.battlePlayer = Player(3 * app.height / 4, # y
                                app.width / 2, # x
                                app.initsW / 2, # radius
                                0, # money
                                100, # health
                                2, # dmg
                                2 * app.difficultyNum) 

    app.hitCounter = 0
    app.beenHitCounter = 0
    app.combo = 8 - app.difficultyNum
    app.dmgMult = 1

    app.cx = app.cy = 0

def appStarted(app):

    app.mode = 'startScreen'
