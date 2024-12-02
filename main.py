from cmu_graphics import *
from Tiles import *
from Character import *
from Node import *
from Object import *
from Maps import *

#from Krosbie
from urllib.request import urlopen
from PIL import Image
def loadImage(url):
    pilImage = Image.open(urlopen(url))
    cmuImage = CMUImage(pilImage)
    return cmuImage


#appStart
def onAppStart(app):
    app.enemyList = []
    app.rows = 20
    app.cols = 20
    app.boardLeft = 50
    app.boardTop = 75
    app.boardWidth = 600
    app.boardHeight = 600
    app.cellBorderWidth = 2
    app.map = []
    app.player = Player('snake')
    makeMap1(app)
    app.stepPerSecond = 1
    
    app.debuggingMode = True

    app.counter = 0
    app.paused = True
    
    app.searchStartStep = 0
    app.searchStarted = False
    app.searchCurrStep = 0

    #player position
    app.playerRow = 0
    app.playerCol = 0
    app.lastKnownLocationOfPlayer = None

    #pictures
    '''app.enemyPicUp = loadImage('https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Red_Triangle.svg/516px-Red_Triangle.svg.png?20100215063256')
    app.enemyPicLeft = loadImage('https://upload.wikimedia.org/wikipedia/commons/f/f1/Long_red_right-pointing_triangle.svg')
    app.enemyPicDown = loadImage('https://www.emoji.co.uk/files/microsoft-emojis/symbols-windows10/10303-up-pointing-red-triangle.png')
    app.enemyPicRight = loadImage('https://commons.wikimedia.org/wiki/File:TriangleArrow-Left-red.png')'''
    app.titleScreen = CMUImage(Image.open('titleScreen.jpeg'))

############################################################
# Start Screen
############################################################

def start_redrawAll(app):
    drawImage(app.titleScreen,0,0)

def start_onKeyPress(app, key):
    if key == 'space':
        setActiveScreen('map1')

############################################################
# map1 Screen
############################################################
def map1_onScreenActivate(app):
    # Every time we switch to the game screen, reset the score
    app.score = 0

def map1_redrawAll(app):
    drawBoard(app)
    drawBoardBorder(app)
    drawTiles(app)

def drawTiles(app):
    for row in app.map:
        for tile in row:
            tile.draw(app)



#player movement logic and various commands.

def map1_onKeyPress(app, key):
    if key == 'p':
        app.paused = not app.paused
    elif key == 's':
        map1_takeStep(app)
    elif key == 'f':
        #takedown enemy
        app.player.CQC(app)
    elif key == 'd':
        print('set all enemies to search')
        for enemy in app.enemyList:
            enemy.inChase = False
            enemy.firstDetection = False
            enemy.inSearch = True
            #self.searchRadius
            enemy.inPatrol = False
            if app.lastKnownLocationOfPlayer != None:
                app.lastKnownLocationOfPlayer = (app.playerRow,app.playerCol)
            
        

        
            
def map1_onKeyHold(app,keys):
    if app.counter % 5 == 0:
        if 'up' in keys:
            app.player.moveUp(app)
        elif 'down' in keys:
            app.player.moveDown(app)
        elif 'right' in keys:
            app.player.moveRight(app)  
        elif 'left' in keys:
            app.player.moveLeft(app)

# initializing and running the app


def map1_onStep(app):
    if not app.paused: 
        map1_takeStep(app)

def map1_takeStep(app):
    app.counter += 1
    for enemy in app.enemyList:
        print(f'chasing:{enemy.inChase},searching:{enemy.inSearch}')
        enemy.clearCurrFOV(app)
        enemy.clearHearing(app)
        if enemy.HP > 0:
            enemy.createFOV(app)
            enemy.createHearingRadius(app)
            enemy.checkFOV(app)

        if enemy.inChase == True and app.counter % 15 == 0:
            #siren goes off and all enemies alertmeter goes up to 300 and start chasing
            for enemy in app.enemyList:
                if enemy.firstDetection == False:
                    enemy.alertMeter += 200
                    enemy.firstDetection = True
                enemy.takeAStep(app,app.playerRow,app.playerCol)
        elif enemy.inSearch == True and app.counter % 1 == 0:
            enemy.firstDetection = False
            #generate LKL of player and start search the radius

            if app.lastKnownLocationOfPlayer == None:
                    app.lastKnownLocationOfPlayer = (app.playerRow,app.playerCol)

            print('we are here')
            if app.searchStarted == False:
                app.searchStartStep = app.counter
                app.searchStarted = True
                print('we started search')
            else:
                print('we are doing search')
                app.searchCurrStep = app.counter
                if app.searchCurrStep - app.searchStartStep > 50:
                    #when 50 steps passed call off search
                    print('we are calling off search')
                    for enemy in app.enemyList:
                        enemy.inSearch = False
                        app.lastKnownLocationOfPlayer = None
                        enemy.searchCurrStep = 0
                        enemy.currSearchPath = None
                        
                else:
                    print('we are thinking about search')
                    #when no searchtile or arrived at searchtile, generate a new one
                    if enemy.searchTile == None or (enemy.row,enemy.col) == enemy.searchTile:
                        print('we are generating a search tile')
                        enemy.searchTile = enemy.generateRandomSearchTile(app,app.lastKnownLocationOfPlayer)
                    else:
                        print(f'This is the {enemy.searchCurrStep + 1} of 5 steps to search tile')
                        if enemy.searchCurrStep == 0:
                            path = []
                            visited = set()
                            pathFindingMap = enemy.makePathFindingMap(app)
                            start = (enemy.row,enemy.col)
                            end = enemy.searchTile
                            enemy.currSearchPath = findShortestPath(pathFindingMap, start, end, path,visited)
                            if enemy.currSearchPath == None:
                                print('''I can't get there''')
                            else:
                                targetRow = enemy.currSearchPath[0][0]
                                targetCol = enemy.currSearchPath[0][1]
                                dRow = targetRow - enemy.row
                                dCol = targetCol - enemy.col
                                enemy.move(app,dRow,dCol)
                                enemy.currSearchPath.pop(0)
                                print('took a step')
                                enemy.searchCurrStep += 1
                        elif enemy.searchCurrStep < 6:
                            targetRow = enemy.currSearchPath[0][0]
                            targetCol = enemy.currSearchPath[0][1]
                            dRow = targetRow - enemy.row
                            dCol = targetCol - enemy.col
                            enemy.move(app,dRow,dCol)
                            enemy.currSearchPath.pop(0)
                            print('took a step')
                            enemy.searchCurrStep += 1
                        else:
                            enemy.searchCurrStep = 0
        
                
                    

############################################################
# Main
############################################################

def main():

    runAppWithScreens(initialScreen='start')

main()
