from cmu_112_graphics import *
from player import *
from map import *
from rectangle import *

def appStarted(app):
    app.rows, app.cols = (20, 20)
    app.sW = min(app.width / app.rows, app.height / app.rows)

    # get the map and the player's starting location
    app.gameMap, app.pLoc = createMap((app.rows, app.cols), 50, 7)
    print(app.pLoc)
    app.player = Player(app.pLoc[0], app.pLoc[1], app.sW / 3)



def keyPressed(app, event):
    pass

def redrawAll(app, canvas):
    for i, row in enumerate(app.gameMap):
        for j, val in enumerate(row):
            cell = Rectangle(i * app.sW, j * app.sW, app.sW)

            if val == 0:
                cell.setColor('black')
            else:
                cell.setColor('white')

            canvas.create_rectangle(cell.x, cell.y, cell.x2, cell.y2, fill = 
                                    cell.color, width = 0)

            # coords for player
            x = app.player.x * app.sW
            y = app.player.y * app.sW
            canvas.create_oval(
                x - app.player.radius,
                y - app.player.radius,
                x + app.player.radius,
                y + app.player.radius,
                fill = app.player.color)




if __name__ == "__main__":
    runApp(width = 800, height = 800)
