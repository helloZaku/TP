from cmu_graphics import *
from Tiles import *
from Character import *
from Node import *

#1. make maps
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)

def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=None, border='black',
             borderWidth=app.cellBorderWidth)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

#draw the map the characters actually use(a 2D list);doesn't show up on screen
def makeMap1(app):
    app.map = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,2,0,3,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ]
    for row in range(app.rows):
        for col in range(app.cols):
                left, top = getCellLeftTop(app, row, col)
                cellWidth, cellHeight = getCellSize(app)
                if app.map[row][col] == 0:
                    app.map[row][col] = Tiles(left,top,cellWidth,cellHeight)
                elif app.map[row][col] == 1:
                    app.map[row][col] = Tiles(left,top,cellWidth,cellHeight,Enemy('Fox',left,top,cellWidth,cellHeight,row,col,
                                                                                  'straightVertical'))
                elif app.map[row][col] == 2:
                    app.player.setLocation(left,top,cellWidth,cellHeight,row,col)
                    app.map[row][col] = Tiles(left,top,cellWidth,cellHeight,app.player)
                elif app.map[row][col] == 3:
                    app.map[row][col] = Tiles(left,top,cellWidth,cellHeight,Enemy('Jimmy',left,top,cellWidth,cellHeight,row,col,
                                                                                  'straightHorizontal'))



# 2. draw the board from drawBoard notes


def redrawAll(app):
    drawBoard(app)
    drawBoardBorder(app)
    drawTiles(app)

def drawTiles(app):
    for row in app.map:
        for tile in row:
            tile.draw()



#player movement logic and various commands.

def onKeyPress(app, key):
    if 'up' == key:
        app.player.moveUp(app)
    elif 'down' == key:
        app.player.moveDown(app)
    elif 'right' == key:
        app.player.moveRight(app)  
    elif 'left' == key:
        app.player.moveLeft(app)
    elif key == 'p':
        app.paused = not app.paused
    elif key == 's':
        takeStep(app)
            


# initializing and running the app
def onAppStart(app):
    app.rows = 10
    app.cols = 15
    app.boardLeft = 50
    app.boardTop = 75
    app.boardWidth = 600
    app.boardHeight = 600
    app.cellBorderWidth = 2
    app.map = []
    app.player = Player('snake')
    makeMap1(app)

    app.counter = 0
    app.paused = True
    app.stepsPerSecond = 10

    #player position
    app.playerRow = 0
    app.playerCol = 0

    #enemy list
    app.enemyList = []

def onStep(app):
    if not app.paused: 
        app.counter += 1
        takeStep(app)

def takeStep(app):
    app.counter += 1
    for row in app.map:
        for tile in row:
            if tile.character != None:
                if isinstance(tile.character,Enemy):
                    if tile.character.inChase == True:
                        tile.character.chase(app)
                    #tile.character.patrol(app)


def main():
    runApp()

main()
