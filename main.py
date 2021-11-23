from cmu_112_graphics import *
from player import *
from map import *
from rectangle import *
from mob import *
from astar import *
from gameInit import *

def appStartedHelper():
    pass

def appStarted(app):

    # these are things that'll change depending on difficulty
    # take stuff from something
    app.rows, app.cols = (10, 10)
    app.numOfMobs = 1
    app.timerDelay = app.defaultTimer = 250

    # have the board use different height measurements
    app.boardHeight = 0.9 * app.height

    # make it relative to window size
    app.sW = min(app.width / app.rows, app.boardHeight / app.rows)

    # initiliaze game states and variables: 
    '''Travel, Fight, etc.'''
    app.gameState = 'Travel'
    app.paused = False
    app.level = 0

    # initilalize map and then get start locations for player and end goal as
    # well as acceptable mob locations
    # Adjust maxTuns and maxLen scalings on difficulty****
    app.gameMap, app.pLoc, app.gLoc, mLocs = createMap(
        (app.rows, app.cols), int(1.2 * (app.rows + app.cols)), app.rows // 2.5)
    app.player = Player(app.pLoc[0], app.pLoc[1], app.sW / 3, 0)
    
    # make a list of unique mob spawning locations
    app.mobListLoc = random.sample(mLocs, app.numOfMobs)

    # create a list of mob classes
    app.mobList = [Mob(m[1], m[0], app.sW / 3, 10, i) for i, m in enumerate(app.mobListLoc)]

    # have a set to keep track of the coords so the mobs don't overlap
    app.mobCoords = {(i[0], i[1]) for i in app.mobListLoc}

    # initialize a mob for the mob fight

    # **Change the location so that if you meet the mob from your left then 
    # the battle starts from left if that makes sense. From top then top and bottom,
    # bottom then bottom top
    # change size of mob depending on difficulty as well
    # later change the battlemob based on difficulty parameters
    app.battleMobList = [BattleMob(app.height / 4, app.width / 2, app.sW * 1.5, 2, 25, 100, 20) for i in app.mobList]

    
    
    # put this in mob class
    app.initialBMSpeed = app.battleMobList[0].d
    # need this for later
    app.counter = 0
    

    app.battlePlayer = Player(3 * app.height / 4, app.width / 2, app.sW, 0, 100, 2)

    # put this in player class
    app.hitCounter = 0
    app.beenHitCounter = 0
    app.combo = 0
    app.dmgMult = 1

    # initialize mouse pressed locations
    app.cx = app.cy = 0

# clean up the code later

def keyPressed(app, event):
    if app.mode == 'Travel':
        lastCoords = (app.player.y, app.player.x)

        if app.paused: app.paused = False
        if (event.key == 'w' or event.key == 'Up'): app.player.y -= 1
        if (event.key == 's' or event.key == 'Down'): app.player.y += 1
        if (event.key == 'd' or event.key == 'Right'): app.player.x += 1
        if (event.key == 'a' or event.key == 'Left'): app.player.x -= 1
        if (event.key == 'p'): app.paused = not app.paused

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
        elif (pY, pX) in app.mobCoords: # player meets mob
            app.gameState = 'mobFight'
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
            app.gameMap, app.pLoc, app.gLoc, mLocs = createMap(
                (app.rows, app.cols), int(1.2 * (app.rows + app.cols)), app.rows // 2.5)
            app.numOfMobs += 1 # for this maybe don't have it increase all the time, maybe make a formula
            # perhaps it's 2 + (level // 2) + something abt difficulty
            # don't forget that we need to change the player location as well
            app.player.y, app.player.x = app.pLoc
            
            # Essentially do all the stuff we did for the initializing thing
            # Make a helper function that gets all this stuff for us because
            # the code is super messy
            app.sW = min(app.width / app.rows, app.boardHeight / app.rows)
            app.boardHeight = 0.9 * app.height
            app.mobListLoc = random.sample(mLocs, app.numOfMobs)
            app.mobList = [Mob(m[1], m[0], app.sW / 3, 10, i) for i, m in enumerate(app.mobListLoc)]
            app.mobCoords = {(i[0], i[1]) for i in app.mobListLoc}
            app.battleMobList = [BattleMob(app.height / 4, app.width / 2, app.sW * 1.5, 2, 25, 100, 20) for i in app.mobList]
            app.player.radius = app.sW / 3

    elif app.gameState == 'mobFight':
        p = app.battlePlayer
        lastCoords = (p.y, p.x)
        if (event.key == 'w' or event.key == 'Up'): p.y -= 10
        if (event.key == 's' or event.key == 'Down'): p.y += 10
        if (event.key == 'd' or event.key == 'Right'): p.x += 10
        if (event.key == 'a' or event.key == 'Left'): p.x -= 10

        # change player coords back if the space the players wants to move in is illegal
        if (p.y < 0 or p.y > app.height or p.x < 0 or p.x > app.width):
            p.y = lastCoords[0]
            p.x = lastCoords[1]

def mousePressed(app, event):
    if app.gameState == 'mobFight':
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
            app.dmgMult = max(app.combo // 8, 1) # this is so the dmg is never 0
            app.battleMob.curHealth -= app.dmgMult * app.battlePlayer.dmg

            # basically check if you killed the mob, maybe insert a little
            # transition later
            if app.battleMob.curHealth <= 0:
                app.player.money += app.battleMob.money
                index = app.indexOfLastMobFought
                m = app.mobList[index]
                app.mobCoords.discard((m.y, m.x))
                app.mobList.pop(index)
                app.battleMobList.pop(index)
                app.gameState = 'Travel'
                app.paused = True
                app.timerDelay = app.defaultTimer

        else:
            # missed, so counter goes down
            app.hitCounter -= 1
            app.combo = 0
            app.dmgMult = max(1, app.dmgMult - 1)

    
def timerFired(app):
    # change the coords of every mob if a mob isn't in there already
    app.counter += 1

    if app.gameState == "Travel" and not app.paused:
        for i, mob in enumerate(app.mobList):
            pos = getNextPos((mob.y, mob.x), (app.player.y, app.player.x), app.gameMap)
            if pos not in app.mobCoords:
                app.mobCoords.discard((mob.y, mob.x))
                (mob.y, mob.x) = pos # update the mob's position
                app.mobCoords.add(pos) # update the set as well

            # Mob meets player
            elif pos == app.player.loc():
                app.gameState = 'mobFight'
                app.timerDelay = 100
                app.indexOfLastMobFought = i
                app.battleMob = app.battleMobList[i]
                app.initialBMSpeed = app.battleMob.d

    elif app.gameState == 'mobFight':
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
            p.curHealth -= m.dmg
            # same methods as above when you defeat it, but this time you
            # also take damage. Perhaps I make a method for this too.
            # have it be inside another function, maybe appStarted so I can
            # use all the variables
            app.player.money += app.battleMob.money
            index = app.indexOfLastMobFought
            m = app.mobList[index]
            app.mobCoords.discard((m.y, m.x))
            app.mobList.pop(index)
            app.battleMobList.pop(index)
            app.gameState = 'Travel'
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
        


def redrawAll(app, canvas):
    if app.gameState == "Travel":
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
        
        canvas.create_text(app.width / 6, app.height - 10,
                            text = f'Health: {int(p.curHealth)}', font = 'Arial 13 bold')
        canvas.create_text(5 * app.width / 6, app.height - 10,
                            text = f'Money: {p.money}', font = 'Arial 13 bold')

    elif app.gameState == 'mobFight':
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
                            text = f'Dmg Multiplier: {app.dmgMult}x', font = 'Arial 13 bold')
        canvas.create_text(3 * app.width / 4, app.height / 9,
                            text = f'Health Left: {int(p.curHealth)}', font = 'Arial 13 bold')
        canvas.create_text(app.width / 2, app.height / 20,
                            text = f'Mob Health: {((m.curHealth / m.maxHealth) * 100):.2f}%')
    elif app.gameState == 'bossFight':
        pass




if __name__ == "__main__":
    runApp(width = 400, height = 400)
