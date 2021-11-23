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
    app.rows, app.cols = (20, 20)
    numOfMobs = 3
    app.timerDelay = app.defaultTimer = 250


    # make it relative to window size
    app.sW = min(app.width / app.rows, app.height / app.rows)

    # initiliaze game states: 
    '''Travel, Fight, etc.'''
    app.Travel = True
    app.mobFight = False
    app.bossFight = False
    app.paused = False

    # initilalize map and then get start locations for player and end goal as
    # well as acceptable mob locations
    # Adjust maxTuns and maxLen scalings on difficulty****
    app.gameMap, app.pLoc, app.gLoc, mLocs = createMap(
        (app.rows, app.cols), int(1.2 * (app.rows + app.cols)), app.rows // 2.5)
    app.player = Player(app.pLoc[0], app.pLoc[1], app.sW / 3, 0)
    
    # make a list of unique mob spawning locations
    app.mobListLoc = random.sample(mLocs, numOfMobs)

    # create a list of mob classes
    app.mobList = [Mob(i[1], i[0], app.sW / 3, 10) for i in app.mobListLoc]

    # have a set to keep track of the coords so the mobs don't overlap
    app.mobCoords = {(i[0], i[1]) for i in app.mobListLoc}

    # initialize a mob for the mob fight

    # **Change the location so that if you meet the mob from your left then 
    # the battle starts from left if that makes sense. From top then top and bottom,
    # bottom then bottom top
    # change size of mob depending on difficulty as well
    # later change the battlemob based on difficulty parameters
    app.battleMobList = [BattleMob(app.height / 4, app.width / 2, app.sW * 1.5, 2, 1, 100) for i in app.mobList]

    
    
    # put this in mob class
    app.initialBMSpeed = app.battleMob.d
    # need this for later
    app.counter = 0
    

    app.battlePlayer = Player(3 * app.height / 4, app.width / 2, app.sW, 0, 3, 2)

    # put this in player class
    app.hitCounter = 0
    app.beenHitCounter = 0
    app.combo = 0
    app.dmgMult = 1

    # initialize mouse pressed locations
    app.cx = app.cy = 0

# clean up the code

def keyPressed(app, event):
    if app.Travel:
        lastCoords = (app.player.y, app.player.x)

        if app.paused: app.paused = False
        if (event.key == 'Up'): app.player.y -= 1
        if (event.key == 'Down'): app.player.y += 1
        if (event.key == 'Right'): app.player.x += 1
        if (event.key == 'Left'): app.player.x -= 1
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

        # Check if player reached goal
        elif (pY, pX) == app.gLoc:
            # implement later
            pass

    elif app.mobFight:
        lastCoords = (app.player.y, app.player.x)

        if (event.key == 'Up'): app.battlePlayer.y -= 10
        if (event.key == 'Down'): app.battlePlayer.y += 10
        if (event.key == 'Right'): app.battlePlayer.x += 10
        if (event.key == 'Left'): app.battlePlayer.x -= 10

        # change player coords back if the space the players wants to move in is illegal
        pY = app.player.getY()
        pX = app.player.getX()
        if (pY not in range(app.rows) or pX not in range(app.cols) or 
            app.gameMap[pY][pX] == 0):
            app.player.setY(lastCoords[0])
            app.player.setX(lastCoords[1])

def mousePressed(app, event):
    if app.mobFight:
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
            app.dmgMult = max(app.combo // 8, 1)
            app.battleMob.curHealth -= app.dmgMult * app.battlePlayer.dmg
            print(app.battleMob.curHealth, app.dmgMult, app.battlePlayer.dmg)

            # basically check if you killed the mob, maybe insert a little
            # transition later
            if app.battleMob.curHealth <= 0:
                app.player.money += app.battleMob.money
                app.mobList.pop(app.indexOfLastMobFought)
                app.mobFight = False
                app.Travel = True
                app.paused = True
                app.timerDelay = app.defaultTimer

        else:
            app.hitCounter -= 1
            app.combo = 0
            app.dmgMult = max(1, app.dmgMult - 1)

    
def timerFired(app):
    # change the coords of every mob if a mob isn't in there already
    app.counter += 1

    if app.Travel and not app.paused:
        for i, mob in enumerate(app.mobList):
            pos = getNextPos((mob.y, mob.x), (app.player.y, app.player.x), app.gameMap)
            if pos not in app.mobCoords:
                app.mobCoords.discard((mob.y, mob.x))
                (mob.y, mob.x) = pos
                app.mobCoords.add(pos)

            # Mob meets player, begin fight
            elif pos == app.player.loc():
                app.mobFight = True
                app.Travel = False
                app.timerDelay = 100
                app.indexOfLastMobFought = i
                app.battleMob = app.battleMobList[i]
                app.initialBMSpeed = app.battleMob.d

    elif app.mobFight:
        m = app.battleMob
        p = app.battlePlayer
        (m.y, m.x) = simpleGetNextPos((m.y, m.x), (p.y, p.x), m.d)
        if ((m.y - m.rad) < p.y < (m.y + m.rad) and 
            (m.x - m.rad) < p.x < (m.x + m.rad)): # mob touches player
            app.beenHitCounter += 1
        
        # change up the speed of the mob so it's not boring

        if app.initialBMSpeed == app.battleMob.d:
            a = random.randint(1, 9)
            if a == 3 or a == 2:
                app.battleMob.d *= 5
                app.counter = 0
        else:
            if app.counter >= 5:
                app.battleMob.d = app.initialBMSpeed
        


def redrawAll(app, canvas):
    if app.Travel:
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

        # coords for player
        x = app.player.x * app.sW + (app.sW / 2)
        y = app.player.y * app.sW + (app.sW / 2)

        # draw player
        canvas.create_oval(
            x - app.player.radius,
            y - app.player.radius,
            x + app.player.radius,
            y + app.player.radius,
            fill = app.player.color)

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

    elif app.mobFight:
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
                            text = f'Health Left: {((p.curHealth / p.maxHealth) * 100):.2f}%', font = 'Arial 13 bold')

        canvas.create_text(app.width / 2, app.height / 20,
                            text = f'Mob Health: {((m.curHealth / m.maxHealth) * 100):.2f}%')
    elif app.bossFight:
        pass




if __name__ == "__main__":
    runApp(width = 400, height = 400)
