#snake and enemy sprites: https://www.spriters-resource.com/fullview/22527/
#ground and tiles sprites: https://www.gog.com/en/game/metal_gear
#need to implement dead logic for enemies

from cmu_graphics import *
from Tiles import *
from Character import *
from Node import *
from Object import *
from Maps import *

#from Krosbie
from urllib.request import urlopen
from PIL import Image

#appStart
def onAppStart(app):
    
    

    #pictures
    app.titleScreen = CMUImage(Image.open('titleScreen.jpeg'))
    app.gameOverScreen = CMUImage(Image.open('gameOverScreen.jpg'))
    app.enemyUp = CMUImage(Image.open('enemyUp.png'))
    app.enemyStabUp = CMUImage(Image.open('enemyUpStab.png'))
    app.enemyRight = CMUImage(Image.open('enemyRight.png'))
    app.enemyStabRight = CMUImage(Image.open('enemyStabRight.png'))
    app.enemyDown = CMUImage(Image.open('enemyDown.png'))
    app.enemyStabDown = CMUImage(Image.open('enemyDownStab.png'))
    app.enemyLeft = CMUImage(Image.open('enemyLeft.png'))
    app.enemyStabLeft = CMUImage(Image.open('enemyLeftStab.png'))
    app.enemyDead = CMUImage(Image.open('enemyDead.png'))
    app.playerUp = CMUImage(Image.open('playerUp.png'))
    app.playerStabUp = CMUImage(Image.open('playerStabUp.png'))
    app.playerRight = CMUImage(Image.open('playerRight.png'))
    app.playerStabRight = CMUImage(Image.open('playerStabRight.png'))
    app.playerDown = CMUImage(Image.open('playerDown.png'))
    app.playerStabDown = CMUImage(Image.open('playerStabDown.png'))
    app.playerLeft = CMUImage(Image.open('playerLeft.png'))
    app.playerStabLeft = CMUImage(Image.open('playerStabLeft.png'))
############################################################
# Start Screen
############################################################

def start_redrawAll(app):
    drawImage(app.titleScreen,0,0)

def start_onKeyPress(app, key):
    if key == 'space':
        setActiveScreen('map1')

    elif key == 'g':
        setActiveScreen('gameOverScreen')

############################################################
# map1 Screen
############################################################
def map1_onScreenActivate(app):
    #win condition
    app.startTime = time.time()
    app.currTime = time.time()
    app.timeDifference = 0
    app.winTime = 60

    #reinitialize variables
    app.playerHP = 100
    app.enemyList = []
    app.playerHP = 100
    app.rows = 20
    app.cols = 20
    app.boardLeft = 50
    app.boardTop = 75
    app.boardWidth = 700
    app.boardHeight = 700
    app.cellBorderWidth = 2
    app.map = []
    app.player = Player('snake')
    makeMap1(app)
    app.stepPerSecond = 1
    
    app.counter = 0
    app.paused = True
    
    app.searchStartStep = 0
    app.searchStarted = False
    app.searchCurrStep = 0

    #player position
    app.playerRow = 0
    app.playerCol = 0
    app.lastKnownLocationOfPlayer = None

def map1_redrawAll(app):
    drawBoard(app)
    drawBoardBorder(app)
    drawTiles(app)
    drawHP(app)
    drawLabel()

def drawHP(app):
    drawLabel('HP',700,600)
    if app.playerHP > 0:

        drawRect(700,670,app.playerHP * 2, 50, fill = 'red')

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
    if app.counter % 2 == 0:
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
    if app.playerHP < 0:
        setActiveScreen('gameOverScreen')

    app.counter += 1
    for enemy in app.enemyList:
        
        #create perception if alive
        if enemy.HP <= 0:
            pass
        else:
            enemy.createFOV(app)
            enemy.checkFOV(app)


        #chase logic
            if enemy.inChase == True and app.counter % 4 == 0:
                #siren goes off and all enemies alertmeter goes up to 300 and start chasing
                #first get out of stabbing animation
                if enemy.isStabbing == True:
                    enemy.isStabbing = False
                for enemy in app.enemyList:
                    if enemy.firstDetection == False:
                        enemy.alertMeter += 200
                        enemy.firstDetection = True
                    enemy.clearCurrFOV(app)
                    
                    if isRightNextToEachOther((app.playerRow,app.playerCol),(enemy.row,enemy.col)):
                        enemy.stabPlayer(app)
                        enemy.checkFOV(app)
                    else:
                        enemy.takeAStep(app,app.playerRow,app.playerCol)
                        enemy.checkFOV(app)
                    
                        
                    
            elif enemy.inSearch == True and enemy.inChase == True:
                print('error: inchase and insearch both true')

            #investigate logic
            
            #patrol logic
            elif enemy.inPatrol == True and (enemy.inChase == True or enemy.inSearch == True):
                print(f'error: inpatrol and search:{enemy.inSearch} or chase:{enemy.inChase}')
            elif enemy.inPatrol == True and app.counter % 8 == 0:
                
                #generate a path if there isn't one
                if enemy.alreadyGeneratedPatrolPath == False:
                    path = []
                    visited = set()
                    pathFindingMap = enemy.makePathFindingMap(app)
                    start = (enemy.row,enemy.col)
                    end = enemy.patrolNodes[enemy.currPatrolNodeIndex]
                    enemy.currPatrolPath = findShortestPath(pathFindingMap, start, end, path,visited)
                    if enemy.currPatrolPath == None:
                        print('''I can't get there''')
                    enemy.alreadyGeneratedPatrolPath = True
                    
                #if at end of nodes reset to starting node and generate a new path at next step
                elif enemy.currPatrolPath == []:
                    if enemy.currPatrolNodeIndex < len(enemy.patrolNodes) - 1:
                        enemy.currPatrolNodeIndex += 1
                    else:
                        enemy.currPatrolNodeIndex = 0
                    enemy.alreadyGeneratedPatrolPath = False

                #if there is a pth, walk it until at the end
                else:
                    targetRow = enemy.currPatrolPath[0][0]
                    targetCol = enemy.currPatrolPath[0][1]
                    dRow = targetRow - enemy.row
                    dCol = targetCol - enemy.col
                    enemy.move(app,dRow,dCol)
                    enemy.currPatrolPath.pop(0)
                    print('took a step')
                    
                

            #search logic
            elif enemy.inSearch == True and enemy.inChase == False and app.counter % 5 == 0:
                enemy.firstDetection = False
                #generate LKL of player and start search the radius.firstDetection used to increase alertmeter when player spotted

                if app.lastKnownLocationOfPlayer == None:
                        app.lastKnownLocationOfPlayer = (app.playerRow,app.playerCol)

                print('we are here')
                if app.searchStarted == False:
                    app.searchStartCount = app.counter
                    app.searchStarted = True
                    print('we started search')
                else:
                    print('we are doing search')
                    app.searchCurrCount = app.counter
                    if app.searchCurrCount - app.searchStartCount > 50:
                        #when 50 steps passed call off search
                        print('we are calling off search')
                        for enemy in app.enemyList:
                            enemy.inSearch = False
                            app.lastKnownLocationOfPlayer = None
                            enemy.searchCurrStep = 0
                            enemy.currSearchPath = None
                            enemy.inPatrol = True
                            enemy.alreadyGeneratedPatrolPath = False
                            
                    else:
                        print('we are thinking about search')
                        #when no searchtile or arrived at searchtile, generate a new one
                        if enemy.searchTile == None or (enemy.row,enemy.col) == enemy.searchTile:
                            print('we are generating a search tile')
                            enemy.searchTile = enemy.generateRandomSearchTile(app,app.lastKnownLocationOfPlayer)
                        else:
                            print(f'This is the {enemy.searchCurrStep + 1} of 5 steps to go to search tile')
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
                                #if search path empty because less than 5 steps, just add searchCurrStep
                                if len(enemy.currSearchPath) == 0:
                                    enemy.searchCurrStep = 10
                                else:
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
# GameOver
############################################################  
def gameOverScreen_redrawAll(app):
    drawImage(app.gameOverScreen,0,0)
    drawLabel('Press Any Key To Continue', 50, 50,
          size=20, font='arial',
          bold=True, italic=False,
          fill='black', border=None, borderWidth=2,
          opacity=100, rotateAngle=0, align='center')

def gameOverScreen_onKeyPress(app, key):
    if key == 'space':
        app.playerHP = 100
        setActiveScreen('map1')

############################################################
# Main
############################################################

def main():

    runAppWithScreens(initialScreen='start')

main()
