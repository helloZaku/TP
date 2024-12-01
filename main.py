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
    app.stepPerSecond = 1
    
    app.debuggingMode = True

    app.counter = 0
    app.paused = True
    

    #player position
    app.playerRow = 0
    app.playerCol = 0
   

    #pictures
    '''app.enemyPicUp = loadImage('https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Red_Triangle.svg/516px-Red_Triangle.svg.png?20100215063256')
    app.enemyPicLeft = loadImage('https://upload.wikimedia.org/wikipedia/commons/f/f1/Long_red_right-pointing_triangle.svg')
    app.enemyPicDown = loadImage('https://www.emoji.co.uk/files/microsoft-emojis/symbols-windows10/10303-up-pointing-red-triangle.png')
    app.enemyPicRight = loadImage('https://commons.wikimedia.org/wiki/File:TriangleArrow-Left-red.png')'''

############################################################
# Start Screen
############################################################

def start_redrawAll(app):
    drawLabel('Welcome!', 200, 160, size=24, bold=True)
    # Note: we can access app.highScore (and all app variables) from any screen
    drawLabel('Press space to begin!', 200, 240, size=16)

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
        if enemy.inChase == True and enemy.startedChase == False:
            for enemy in app.enemyList:
                enemy.inChase = True
                enemy.startChase(app)
                
                    

############################################################
# Main
############################################################

def main():

    runAppWithScreens(initialScreen='start')

main()
