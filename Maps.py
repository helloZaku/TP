#elite type enemies currently broken when chase starts. To see it moving on the board, put 3 anywhere in the 2D list of the map. Node class currently
#contains A* for its pathfinding

from cmu_graphics import *
from Tiles import *
from Character import *
from Object import *

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
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,4,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0],
        [0,0,0,0,4,0,0,0,0,0,0,4,0,0,0,0,0,0,4,0],
        [0,0,0,0,4,0,0,0,0,0,0,4,0,0,0,0,0,0,4,0],
        [0,0,0,0,4,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0],
        [0,0,4,4,4,0,0,0,0,0,0,4,4,4,4,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,4,0,0,0,0,4,0,4,0,0,0,0,4,0,0,0,0,0],
        [0,4,0,0,0,0,0,4,0,4,0,0,0,0,0,4,0,0,0,0],
        [0,0,0,0,0,0,0,4,1,4,0,0,0,0,0,0,4,0,0,0],
        [0,0,0,0,0,0,0,4,0,4,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,4,0,4,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,4,4,4,4,0,0,0,0,0,0,0,0,0,4,4,4,4,4,0],
        [0,0,0,0,4,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0],
        [0,0,0,0,4,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0],
        [0,0,0,0,4,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
        
    ]
    for row in range(app.rows):
        for col in range(app.cols):
                left, top = getCellLeftTop(app, row, col)
                cellWidth, cellHeight = getCellSize(app)
                if app.map[row][col] == 0:
                    app.map[row][col] = Tiles(left,top,cellWidth,cellHeight)
                elif app.map[row][col] == 1:
                    Jimmy = Enemy('Ocelot',left,top,cellWidth,cellHeight,row,col,
                                [(0,0),(10,19)])
                    app.map[row][col] = Tiles(left,top,cellWidth,cellHeight,Jimmy)
                    app.enemyList.append(Jimmy)
                elif app.map[row][col] == 2:
                    app.player.setLocation(left,top,cellWidth,cellHeight,row,col)
                    app.map[row][col] = Tiles(left,top,cellWidth,cellHeight,app.player)
                elif app.map[row][col] == 3:
                    Liquid = Elite('Liquid',left,top,cellWidth,cellHeight,row,col,
                                [(0,0),(19,19)])
                    app.enemyList.append(Liquid)
                    app.map[row][col] = Tiles(left,top,cellWidth,cellHeight,Liquid)
                elif app.map[row][col] == 4:
                    app.map[row][col] = Tiles(left,top,cellWidth,cellHeight,None,Wall(left,top,cellWidth,cellHeight,row,col))
                

def makeMap2(app):
    app.map = [
        [2,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,4,0,0,0,0,4,0,0,0,0,0,4,4,0,0,0],
        [0,0,0,4,4,0,0,0,4,4,0,0,0,0,4,0,0,4,0,0],
        [0,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,1,0,0,0],
        [0,4,0,0,4,0,0,0,0,4,0,0,0,0,0,0,0,3,0,0],
        [0,0,0,0,4,0,0,0,0,4,0,0,0,0,4,0,0,0,0,0],
        [0,0,0,0,4,0,0,0,0,4,0,0,0,4,0,0,0,0,0,0],
        [0,0,0,0,4,0,3,0,0,4,0,0,0,4,0,0,3,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,1,4,0,0,0,0,0,0],
        [0,0,0,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,4,0,0,0,3,4,0,0,0,4,0,0,0,0,0,1],
        [0,0,0,0,4,0,0,0,0,4,0,0,0,4,0,0,0,0,0,0],
        [0,0,0,0,4,0,0,0,0,4,0,0,0,4,0,0,0,0,0,0],
        [0,0,4,4,4,4,0,4,4,4,4,4,0,4,4,4,4,4,4,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
        
    ]
    for row in range(app.rows):
        for col in range(app.cols):
                left, top = getCellLeftTop(app, row, col)
                cellWidth, cellHeight = getCellSize(app)
                if app.map[row][col] == 0:
                    app.map[row][col] = Tiles(left,top,cellWidth,cellHeight)
                elif app.map[row][col] == 1:
                    Jimmy = Enemy('Ocelot',left,top,cellWidth,cellHeight,row,col,
                                [(0,0),(10,10)])
                    app.map[row][col] = Tiles(left,top,cellWidth,cellHeight,Jimmy)
                    app.enemyList.append(Jimmy)
                elif app.map[row][col] == 2:
                    app.player.setLocation(left,top,cellWidth,cellHeight,row,col)
                    app.map[row][col] = Tiles(left,top,cellWidth,cellHeight,app.player)
                elif app.map[row][col] == 3:
                    Liquid = Enemy('Liquid',left,top,cellWidth,cellHeight,row,col,
                                [(0,18),(12,18)])
                    app.enemyList.append(Liquid)
                    app.map[row][col] = Tiles(left,top,cellWidth,cellHeight,Liquid)
                elif app.map[row][col] == 4:
                    app.map[row][col] = Tiles(left,top,cellWidth,cellHeight,None,Wall(left,top,cellWidth,cellHeight,row,col))
               
