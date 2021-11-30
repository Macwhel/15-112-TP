from cmu_112_graphics import *
from player import *
from map import *
from rectangle import *
from mob import *
from astar import *
from gameInit import *
from items import *


# Screens concept from lecture notes (not sure if I needed to cite this but better safe than sorry)
# No code was copy pasted

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

def pause_keyPressed(app, event):
    if event.key == 'Space':
        print(app.lastState)
        app.mode = app.lastState


#########################################################

def tutorial_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "light blue")

    canvas.create_text(app.width / 2, app.height / 6, text = 'Basic Rules:', font = "Cambria 32 bold")

def tutorial_keyPressed(app, event):
    if event.key == 'Right': app.mode = 'tutorial1'
    if event.key == "Space": app.mode = 'Travel'

def tutorial_mousePressed(app, event):
    loc = (event.y, event.x)
    
    # if it ever clicks on this on this one part of the screen, then go straight to the game
    app.mode = 'Travel'

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

    canvas.create_text(app.width / 2, app.height / 20, text = f'Level {app.level} Completed', font = "Cambria 32 bold")
    canvas.create_text(app.width / 2, app.height / 8, text = 'Shop', font = "Cambria 20 bold")

    # show the player's health and money so they know what they should/can buy
    p = app.player
    canvas.create_text(app.width / 6, app.height - 10,
                        text = f'Health: {int(p.curHealth)} / {p.maxHealth}', font = 'Cambria 13 bold')
    canvas.create_text(5 * app.width / 6, app.height - 10,
                        text = f'Worms: {p.money}', font = 'Cambria 13 bold')
    
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
    p.money -= cost

    if itemType == 0:
        p.dmg += effects[0]
        p.critDmg += effects[1] / 100
        p.critRate += effects[2]
        p.maxHealth += effects[4]
        p.curHealth = min(p.maxHealth, p.curHealth + effects[3])
        p.defense += effects[5]

    elif itemType == 1:
        p.maxHealth += effects[1]
        p.curHealth = min(p.maxHealth, p.curHealth + effects[0])
        p.defense += effects[2]
        p.speed += effects[3]
        p.dmg += effects[4]

    else: 
        p.speed += effects[0]
        app.mobDropMult += effects[1]
        app.itemSpawnChanceMult += effects[2]
        app.maxCombo += effects[3]
        app.numOfMobs += effects[4]
        p.defense += effects[5]

    app.items = rerollItems(app.difficulty, app.level)

def Shop_mousePressed(app, event):

    m = app.player.money
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
        app.mode = 'Travel'

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
    canvas.create_text(app.width / 6, app.height - 10,
                        text = f'Health: {int(p.curHealth)} / {int(p.maxHealth)}', font = 'Cambria 13 bold')
    canvas.create_text(5 * app.width / 6, app.height - 10,
                        text = f'Money: {p.money}', font = 'Cambria 13 bold')

def Travel_timerFired(app):
    # get the next position for all mobs
    if not app.paused:
        for i, mob in enumerate(app.mobList):
                if (h((mob.y, mob.x), (app.player.y, app.player.x)) >= 10 and
                    h((app.gLoc[0], app.gLoc[1]),(app.player.y, app.player.x)) >= 20):
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
    if (event.key == 's' or event.key == 'Down'): app.player.y += 1
    if (event.key == 'd' or event.key == 'Right'): app.player.x += 1
    if (event.key == 'a' or event.key == 'Left'): app.player.x -= 1
    if (event.key == 'p'): 
        app.mode = 'pause'
        app.lastState = 'Travel'

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
        app.level += 1
        app.rows += 3 # change this number later
        app.cols = app.rows
        # now change all the variables that create the board and stuff as well as get new positions
        mapType = randomMap()
        mapType = "Dungeon"
        if mapType == "Kruskals":
            app.gameMap, app.pLoc, app.gLoc, mLocs = Kruskals((app.rows, app.cols))
        elif mapType == 'KruskalsWeave':
            app.gameMap, app.pLoc, app.gLoc, mLocs = KruskalsWeave((app.rows, app.cols))
        else:
            app.gameMap, app.pLoc, app.gLoc, mLocs = createMap(
                (app.rows, app.cols), int(1.2 * (app.rows + app.cols)), app.rows // 2.5)
            print(app.gLoc)
        for row in app.gameMap:
            print(row)
        app.numOfMobs = max(app.numOfMobs, int((app.level * app.difficultyNum) / 5) ) # for this maybe don't have it increase all the time, maybe make a formula
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
                                        int((app.level * app.difficultyNum) ** 0.75), 
                                        25, 
                                        100 * app.mobDropMult, 20) for i in app.mobList]
        app.player.radius = app.sW / 3

#########################################################

def mobFight_timerFired(app):
    app.counter += 1
    m = app.battleMob
    p = app.battlePlayer
    nextPos = simpleGetNextPos((m.y, m.x), (p.y, p.x), m.d)
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
        app.mode = 'Travel'
        app.paused = True
        app.timerDelay = app.defaultTimer

        #app.beenHitCounter = app.counter

    
    # change up the speed of the mob so it's not boring

    if app.initialBMSpeed == app.battleMob.d:
        a = random.randint(1, 5)
        if a == 1 or a == 2:
            app.battleMob.d *= 5
            app.counter = 0
    else:
        if app.counter >= 5:
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
        app.dmgMult = min(max(app.combo // 8, 1), app.maxCombo) # this is so the dmg is never 0 and doesn't go to infinity (combo caps at maxCombo)
        critDmg = 1
        critRoll = random.randrange(100)
        if critRoll < app.battlePlayer.critRate:
            critDmg = app.battlePlayer.critDmg
        app.battleMob.curHealth -= app.dmgMult * app.battlePlayer.dmg * critDmg

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

    else:
        # missed, so counter goes down
        app.hitCounter -= 1
        app.combo = 0
        app.dmgMult = max(1, app.dmgMult - 1)

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

def initGame(app):

    app.difficultyList = ['Easy', 'Medium', "Hard"] # default list
    app.rows, app.cols = (10, 10) # determine board size
    app.timerDelay = app.defaultTimer = 250 # default 250ms
    app.boardHeight = 0.9 * app.height # to fit everything
    app.initsW = app.sW = min(app.width / app.rows, app.boardHeight / app.rows) # based on yeah
    app.mode = 'tutorial' # start at tutorial
    app.mode = 'pause' ##*#####*********#******##*8*##
    app.paused = False # default unpaused
    mapType = randomMap() # get map
    mapType = 'Dungeon'  # change when not debugging
    app.itemSpawnChanceMult = 1 # default 1
    app.lastState = 'Travel' # default nothing
    app.numOfMobs = max((app.rows**2) // 50, 1) # formula for num of mobs
    app.level = 1 # default 1


    # get number representation of difficulty
    app.difficultyNum = app.difficultyList.index(app.difficulty)

    app.maxCombo = 4 + app.difficultyNum # init max combo
    app.items = rerollItems(app.difficulty, app.level) # init items
    app.mobDropMult = app.level * app.difficultyNum # init base mobDropMult
    
    # initilalize map and then get start locations for player and end goal as
    # well as acceptable mob locations
    # Adjust maxTuns and maxLen scalings on difficulty****
    if mapType == "Kruskals":
        app.gameMap, app.pLoc, app.gLoc, mLocs = Kruskals((app.rows, app.cols))
    elif mapType == 'KruskalsWeave':
        app.gameMap, app.pLoc, app.gLoc, mLocs = KruskalsWeave((app.rows,app.cols))
    else:
        maxTuns = int((app.difficultyNum ** 0.5) * (app.rows + app.cols))
        maxLen = int((app.difficultyNum ** 0.5) * app.rows // 1.5)
        app.gameMap, app.pLoc, app.gLoc, mLocs = createMap(
            (app.rows, app.cols), maxTuns, maxLen)
        print(app.gLoc)
        for r in app.gameMap:
            print(r)

    # init overall player
    app.player = Player(app.pLoc[0], app.pLoc[1], app.sW / 3)

    # make a list of unique mob spawning locations
    app.mobListLoc = random.sample(mLocs, app.numOfMobs)

    # create a list of mob classes for travel board
    app.mobList = [Mob(m[1], m[0], app.sW / 3, 10, i) for i, m in enumerate(app.mobListLoc)]

    # create a list of battle mobs for battle instance
    app.battleMobList = [BattleMob(app.height / 4, app.width / 2, app.initsW * 1.5 / app.level, 
                            int((app.level * app.difficultyNum) ** 0.75), 25, 
                            100 * app.mobDropMult, 20) for i in app.mobList]

    # have a set to keep track of the coords so the mobs don't overlap
    app.mobCoords = {(i[0], i[1]) for i in app.mobListLoc}

    # have the initial speed somewhere
    app.initialBMSpeed = app.battleMobList[0].d 

    # always helpful to keep track
    app.counter = 0

    # player for the fights, no change based on difficulty
    app.battlePlayer = Player(3 * app.height / 4, app.width / 2, app.initsW, 0, 100, 2)

    app.hitCounter = 0
    app.beenHitCounter = 0
    app.combo = 0
    app.dmgMult = 1

    app.cx = app.cy = 0

def appStarted(app):

    app.mode = 'startScreen'







if __name__ == "__main__":
    runApp(width = 1000, height = 1000)
