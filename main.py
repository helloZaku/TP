from cmu_graphics import *
from Tiles import *
from Character import *

#draw the board from drawBoard notes
def onAppStart(app):
    app.rows = 5
    app.cols = 5
    app.boardLeft = 50
    app.boardTop = 75
    app.boardWidth = 300
    app.boardHeight = 300
    app.cellBorderWidth = 2
    app.map = []
    app.player = Player('snake')
    makeMap1(app)

def redrawAll(app):
    drawBoard(app)
    drawBoardBorder(app)
    drawTiles(app)

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
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,1,0,2,0],
        [0,0,0,1,0],
        [0,0,0,0,0]
    ]
    for row in range(app.rows):
        for col in range(app.cols):
                left, top = getCellLeftTop(app, row, col)
                cellWidth, cellHeight = getCellSize(app)
                if app.map[row][col] == 0:
                    app.map[row][col] = Tiles(left,top,cellWidth,cellHeight)
                elif app.map[row][col] == 1:
                    app.map[row][col] = Tiles(left,top,cellWidth,cellHeight,Enemy('Fox',left,top,cellWidth,cellHeight,row,col))
                elif app.map[row][col] == 2:
                    app.player.setLocation(left,top,cellWidth,cellHeight,row,col)
                    app.map[row][col] = Tiles(left,top,cellWidth,cellHeight,app.player)

def drawTiles(app):
    for row in app.map:
        for tile in row:
            tile.draw()

#player movement logic. the methods return true if the movement if legal
def onKeyPress(app, keys):
    if 'up' in keys:
        if app.player.moveUp(app):
            app.map[app.player.row][app.player.col].character = None
            app.map[app.player.row-1][app.player.col].character = app.player 
            print(app.map)
    elif 'down' in keys:
        if app.player.moveDown(app):
            app.map[app.player.row][app.player.col].character = None
            app.map[app.player.row+1][app.player.col].character = app.player  
    elif 'right' in keys:
        if app.player.moveRight(app):
            app.map[app.player.row][app.player.col].character = None
            app.map[app.player.row][app.player.col + 1].character = app.player  
    elif 'left' in keys:
        if app.player.moveLeft(app):
            app.map[app.player.row][app.player.col].character = None
            app.map[app.player.row-1][app.player.col - 1].character = app.player  

def main():
    runApp()

main()
