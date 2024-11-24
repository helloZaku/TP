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
        [0,1,0,0,0],
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
                    app.map[row][col] = Tiles(left,top,cellWidth,cellHeight,Enemy('Jimmy',left,top,cellWidth,cellHeight))
    print(app.map)

def drawTiles(app):
    for row in app.map:
        for tile in row:
            tile.draw()

def main():
    runApp()

main()
