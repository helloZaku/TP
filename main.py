#snake and enemy sprites: https://www.spriters-resource.com/fullview/22527/
#ground and tiles sprites: https://www.gog.com/en/game/metal_gear
#winscreen: https://www.istockphoto.com/video/you-win-glitch-4k-video-animation-footage-pixel-message-design-glitch-effect-gm1447471637-485264495


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
    
    app.removeTileImage = False

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
    app.ground = CMUImage(Image.open('ground.png'))
    app.wall = CMUImage(Image.open('wall.png'))
    app.tutorialScreen = CMUImage(Image.open('tutorialScreen.png'))
    app.eliteUp = CMUImage(Image.open('eliteUp.png'))
    app.eliteDown = CMUImage(Image.open('eliteDown.png'))
    app.eliteRight = CMUImage(Image.open('eliteRight.png'))
    app.eliteLeft = CMUImage(Image.open('eliteLeft.png'))
    app.eliteDead = CMUImage(Image.open('eliteDead.png'))
    app.winScreen = CMUImage(Image.open('winScreen.png'))
############################################################
# Start Screen
############################################################

def start_redrawAll(app):
    drawImage(app.titleScreen,0,0,width = 700, height = 700)

def start_onKeyPress(app, key):
    if key == 'space':
        setActiveScreen('tutorialScreen')

############################################################
# tutorialScreen
############################################################
def tutorialScreen_redrawAll(app):
    drawImage(app.tutorialScreen,0,0,width = 800,height = 700)

def tutorialScreen_onKeyPress(app, key):
    if key == 'space':
        setActiveScreen('map1')

############################################################
# map1 Screen
############################################################
def map1_onScreenActivate(app):
    #win condition
    app.startTime = time.time()
    app.currTime = time.time()
    app.timeDifference = 0
    app.winTime = 10

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
    app.paused = False
    
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
    drawTimer(app)
    
def drawTimer(app):
    drawLabel('Timer',790,110,size = 30)
    drawLabel(app.timeDifference,900,145,size = 30)

def drawHP(app):
    drawLabel('HP',780,200,size = 30)
    if app.playerHP > 0:

        drawRect(760,240,app.playerHP * 2, 50, fill = 'red')

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
        app.removeTileImage = not app.removeTileImage
    
            
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

def makePathFindingMap(app):
        
        pathFindingMap = []
        for row in range(app.rows):
            pathFindingMap.append([])
            for col in range(app.cols):
                tile = app.map[row][col]
                if tile.object != None:
                    pathFindingMap[row].append(1)
                else:
                    pathFindingMap[row].append(0)
        
        return pathFindingMap

# initializing and running the app


def map1_onStep(app):
    if not app.paused: 
        map1_takeStep(app)

def map1_takeStep(app):
    app.currTime = time.time()
    app.timeDifference = app.currTime - app.startTime
    if app.timeDifference > app.winTime:
        setActiveScreen ('map2')

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
                    
                        
                    
             #patrol logic
            elif enemy.inPatrol == True and app.counter % 8 == 0:
                
                #generate a path if there isn't one
                if enemy.alreadyGeneratedPatrolPath == False:
                    path = []
                    visited = set()
                    pathFindingMap = makePathFindingMap(app)
                    
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
            elif enemy.inSearch == True and enemy.inChase == False and app.counter % 7 == 0:
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
                    if app.searchCurrCount - app.searchStartCount > 150:
                        #when 150 steps passed call off search
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
# map2 Screen
############################################################
def map2_onScreenActivate(app):
    #win condition
    app.startTime = time.time()
    app.currTime = time.time()
    app.timeDifference = 0
    app.winTime = 10

    #reinitialize variables
    app.playerHP = 100
    app.enemyList = []
    app.playerHP = 100
    app.rows = 20
    app.cols = 20
    app.boardLeft = 50
    app.boardTop = 75
    app.boardWidth = 700
    app.boardHeight = 900
    app.cellBorderWidth = 2
    app.map = []
    app.player = Player('snake')
    makeMap2(app)
    app.stepPerSecond = 1
    
    app.counter = 0
    app.paused = False
    
    app.searchStartStep = 0
    app.searchStarted = False
    app.searchCurrStep = 0

    #player position
    app.playerRow = 0
    app.playerCol = 0
    app.lastKnownLocationOfPlayer = None

def map2_redrawAll(app):
    drawBoard(app)
    drawBoardBorder(app)
    drawTiles(app)
    drawHP(app)
    drawTimer(app)
    
def drawTimer(app):
    drawLabel('Timer',790,110,size = 30)
    drawLabel(app.timeDifference,900,145,size = 30)

def drawHP(app):
    drawLabel('HP',780,200,size = 30)
    if app.playerHP > 0:

        drawRect(760,240,app.playerHP * 2, 50, fill = 'red')

def drawTiles(app):
    for row in app.map:
        for tile in row:
            tile.draw(app)



#player movement logic and various commands.

def map2_onKeyPress(app, key):
    if key == 'p':
        app.paused = not app.paused
    elif key == 's':
        map1_takeStep(app)
    elif key == 'f':
        #takedown enemy
        app.player.CQC(app)
    elif key == 'd':
        app.removeTileImage = True
    
            
def map2_onKeyHold(app,keys):
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


def map2_onStep(app):
    if not app.paused: 
        map1_takeStep(app)

def map2_takeStep(app):
    app.currTime = time.time()
    app.timeDifference = app.currTime - app.startTime
    if app.timeDifference > app.winTime:
        setActiveScreen ('winScreen')

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
             
            #patrol logic
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
# winScreen
############################################################  
def winScreen_redrawAll(app):
    drawImage(app.winScreen,0,0)
    
def winScreen_onKeyPress(app, key):
    if key == 'space':
        app.playerHP = 100
        setActiveScreen('start')
############################################################
# GameOver
############################################################  
def gameOverScreen_redrawAll(app):
    drawImage(app.gameOverScreen,0,0)
    
def gameOverScreen_onKeyPress(app, key):
    if key == 'space':
        app.playerHP = 100
        setActiveScreen('start')

############################################################
# Main
############################################################

def main():

    runAppWithScreens(initialScreen='start')

main()
