from cmu_112_graphics import *
from player import *
from map import *
from rectangle import *
from mob import *
from astar import *
from items import *

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

def Travel_keyPressed(app, event):

    lastCoords = (app.player.y, app.player.x)

    if (event.key == 'w' or event.key == 'Up'): app.player.y -= 1
    if (event.key == 's' or event.key == 'Down'): app.player.y += 1
    if (event.key == 'd' or event.key == 'Right'): app.player.x += 1
    if (event.key == 'a' or event.key == 'Left'): app.player.x -= 1
    if (event.key == 'r'): runApp(width = 1000, height = 1000)

    moveY, moveX = app.player.y - lastCoords[0], app.player.x - lastCoords[1]

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
    elif (pY, pX) == app.gLoc:
        runApp(width = 1000, height = 1000)

def appStarted(app):
    app.mode = 'Travel'
    app.rows = app.cols = 18
    app.gameMap, app.pLoc, app.gLoc, mLocs = KruskalsWeave((18,18))
    app.boardHeight = 0.9 * app.height
    app.initsW = app.sW = min(app.width / app.rows, app.boardHeight / app.rows)

    app.player = Player(app.pLoc[0], app.pLoc[1], app.sW / 3)

runApp(width = 1000, height = 1000)