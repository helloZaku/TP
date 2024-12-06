
from cmu_graphics import *
from Tiles import *
from Character import *
from Node import *
import time
from MyNode import *
import random

class Character:
    def __init__(self,name,left,top,width,height,row,col):
        self.name = name
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.row = row
        self.col = col
        self.orientation = 'up'
        self.currFOV = []
    
    def createFOV(self,app):


        #create FOV in the middle and store locations of all FOV as tuples in 2D list so when on movement can clear current FOV
        #when blocked by boundaires or object, the subsequent tiles should break
        for i in range(6):
            if self.orientation == 'up':
                if self.row - i >= 0:
                    tile = app.map[self.row - i][self.col]
                    if tile.object == None:
                        app.map[self.row - i][self.col].isInFOV = True
                        self.currFOV.append((self.row - i,self.col))
                    else:
                        break
            elif self.orientation == 'down':
                if self.row + i <= len(app.map) - 1:
                    tile = app.map[self.row + i][self.col]
                    if tile.object == None:
                        app.map[self.row + i][self.col].isInFOV = True
                        self.currFOV.append((self.row + i,self.col))
                    else:
                        break
            elif self.orientation == 'right':
                if self.col + i <= len(app.map[0]) - 1:
                    tile = app.map[self.row][self.col + i]
                    if tile.object == None:
                        app.map[self.row][self.col + i].isInFOV = True
                        self.currFOV.append((self.row,self.col + i))
                    else:
                        break
            elif self.orientation == 'left':
                if self.col - i >= 0:
                    tile = app.map[self.row][self.col - i]
                    if tile.object == None:
                        app.map[self.row][self.col - i].isInFOV = True
                        self.currFOV.append((self.row,self.col - i))
                    else:
                        break
            
            #the 2 lines at the side of the middle line
            leftMiddleNoDrawCt = 0
            rightMiddleNoDrawCt = 0
            for i in range(6):
                if self.orientation == 'up':
                    targetRow,targetCol = self.row - i,self.col - 1
                    if self.isInBounds(targetRow,targetCol,app):
                        tile = app.map[targetRow][targetCol]
                        if tile.object == None:
                            if leftMiddleNoDrawCt < 2:
                                leftMiddleNoDrawCt += 1
                            else:
                                app.map[targetRow][targetCol].isInFOV = True
                                self.currFOV.append((targetRow,targetCol))
                        else:
                            break
                    else:
                        break
                elif self.orientation == 'down':
                    targetRow,targetCol = self.row + i,self.col - 1
                    if self.isInBounds(targetRow,targetCol,app):
                        tile = app.map[targetRow][targetCol]
                        if tile.object == None:
                            if leftMiddleNoDrawCt < 2:
                                leftMiddleNoDrawCt += 1
                            else:
                                app.map[targetRow][targetCol].isInFOV = True
                                self.currFOV.append((targetRow,targetCol))
                        else:
                            break
                elif self.orientation == 'right':
                    targetRow,targetCol = self.row - 1,self.col + i
                    if self.isInBounds(targetRow,targetCol,app):
                        tile = app.map[targetRow][targetCol]
                        if tile.object == None:
                            if leftMiddleNoDrawCt < 2:
                                leftMiddleNoDrawCt += 1
                            else:
                                app.map[targetRow][targetCol].isInFOV = True
                                self.currFOV.append((targetRow,targetCol))
                        else:
                            break
                elif self.orientation == 'left':
                    targetRow,targetCol = self.row - 1,self.col - i
                    if self.isInBounds(targetRow,targetCol,app):
                        tile = app.map[targetRow][targetCol]
                        if tile.object == None:
                            if leftMiddleNoDrawCt < 2:
                                leftMiddleNoDrawCt += 1
                            else:
                                app.map[targetRow][targetCol].isInFOV = True
                                self.currFOV.append((targetRow,targetCol))
                        else:
                            break
            
            for i in range(6):
                if self.orientation == 'up':
                    targetRow,targetCol = self.row - i,self.col + 1
                    if self.isInBounds(targetRow,targetCol,app):
                        tile = app.map[targetRow][targetCol]
                        if tile.object == None:
                            if rightMiddleNoDrawCt < 2:
                                rightMiddleNoDrawCt += 1
                            else:
                                app.map[targetRow][targetCol].isInFOV = True
                                self.currFOV.append((targetRow,targetCol))
                        else:
                            break
                    else:
                        break
                elif self.orientation == 'down':
                    targetRow,targetCol = self.row + i,self.col + 1
                    if self.isInBounds(targetRow,targetCol,app):
                        tile = app.map[targetRow][targetCol]
                        if tile.object == None:
                            if rightMiddleNoDrawCt < 2:
                                rightMiddleNoDrawCt += 1
                            else:
                                app.map[targetRow][targetCol].isInFOV = True
                                self.currFOV.append((targetRow,targetCol))
                        else:
                            break
                elif self.orientation == 'right':
                    targetRow,targetCol = self.row + 1,self.col + i
                    if self.isInBounds(targetRow,targetCol,app):
                        tile = app.map[targetRow][targetCol]
                        if tile.object == None:
                            if rightMiddleNoDrawCt < 2:
                                rightMiddleNoDrawCt += 1
                            else:
                                app.map[targetRow][targetCol].isInFOV = True
                                self.currFOV.append((targetRow,targetCol))
                        else:
                            break
                elif self.orientation == 'left':
                    targetRow,targetCol = self.row + 1,self.col - i
                    if self.isInBounds(targetRow,targetCol,app):
                        tile = app.map[targetRow][targetCol]
                        if tile.object == None:
                            if rightMiddleNoDrawCt < 2:
                                rightMiddleNoDrawCt += 1
                            else:
                                app.map[targetRow][targetCol].isInFOV = True
                                self.currFOV.append((targetRow,targetCol))
                        else:
                            break


        #the 2 far end lines
            leftMiddleNoDrawCt = 0
            rightMiddleNoDrawCt = 0
            for i in range(6):
                if self.orientation == 'up':
                    targetRow,targetCol = self.row - i,self.col - 2
                    if self.isInBounds(targetRow,targetCol,app):
                        tile1 = app.map[targetRow][targetCol]
                        tile2 = app.map[targetRow][targetCol + 1]
                        if tile1.object == None and tile2.object == None:
                            if leftMiddleNoDrawCt < 3:
                                leftMiddleNoDrawCt += 1
                            else:
                                app.map[targetRow][targetCol].isInFOV = True
                                self.currFOV.append((targetRow,targetCol))
                        else:
                            break
                    else:
                        break
                elif self.orientation == 'down':
                    targetRow,targetCol = self.row + i,self.col - 2
                    if self.isInBounds(targetRow,targetCol,app):
                        tile1 = app.map[targetRow][targetCol]
                        tile2 = app.map[targetRow][targetCol + 1]
                        if tile1.object == None and tile2.object == None:
                            if leftMiddleNoDrawCt < 3:
                                leftMiddleNoDrawCt += 1
                            else:
                                app.map[targetRow][targetCol].isInFOV = True
                                self.currFOV.append((targetRow,targetCol))
                        else:
                            break
                elif self.orientation == 'right':
                    targetRow,targetCol = self.row - 2,self.col + i
                    if self.isInBounds(targetRow,targetCol,app):
                        tile1 = app.map[targetRow][targetCol]
                        tile2 = app.map[targetRow + 1][targetCol]
                        if tile1.object == None and tile2.object == None:
                            if leftMiddleNoDrawCt < 3:
                                leftMiddleNoDrawCt += 1
                            else:
                                app.map[targetRow][targetCol].isInFOV = True
                                self.currFOV.append((targetRow,targetCol))
                        else:
                            break
                elif self.orientation == 'left':
                    targetRow,targetCol = self.row - 2,self.col - i
                    if self.isInBounds(targetRow,targetCol,app):
                        tile1 = app.map[targetRow][targetCol]
                        tile2 = app.map[targetRow + 1][targetCol]
                        if tile1.object == None and tile2.object == None:
                            if leftMiddleNoDrawCt < 3:
                                leftMiddleNoDrawCt += 1
                            else:
                                app.map[targetRow][targetCol].isInFOV = True
                                self.currFOV.append((targetRow,targetCol))
                        else:
                            break
            
            for i in range(6):
                if self.orientation == 'up':
                    targetRow,targetCol = self.row - i,self.col + 2
                    if self.isInBounds(targetRow,targetCol,app):
                        tile1 = app.map[targetRow][targetCol]
                        tile2 = app.map[targetRow][targetCol - 1]
                        if tile1.object == None and tile2.object == None:
                            if rightMiddleNoDrawCt < 3:
                                rightMiddleNoDrawCt += 1
                            else:
                                app.map[targetRow][targetCol].isInFOV = True
                                self.currFOV.append((targetRow,targetCol))
                        else:
                            break
                    else:
                        break
                elif self.orientation == 'down':
                    targetRow,targetCol = self.row + i,self.col + 2
                    if self.isInBounds(targetRow,targetCol,app):
                        tile1 = app.map[targetRow][targetCol]
                        tile2 = app.map[targetRow][targetCol - 1]
                        if tile1.object == None and tile2.object == None:
                            if rightMiddleNoDrawCt < 3:
                                rightMiddleNoDrawCt += 1
                            else:
                                app.map[targetRow][targetCol].isInFOV = True
                                self.currFOV.append((targetRow,targetCol))
                        else:
                            break
                elif self.orientation == 'right':
                    targetRow,targetCol = self.row + 2,self.col + i
                    if self.isInBounds(targetRow,targetCol,app):
                        tile1 = app.map[targetRow][targetCol]
                        tile2 = app.map[targetRow - 1][targetCol]
                        if tile1.object == None and tile2.object == None:
                            if rightMiddleNoDrawCt < 3:
                                rightMiddleNoDrawCt += 1
                            else:
                                app.map[targetRow][targetCol].isInFOV = True
                                self.currFOV.append((targetRow,targetCol))
                        else:
                            break
                elif self.orientation == 'left':
                    targetRow,targetCol = self.row + 2,self.col - i
                    if self.isInBounds(targetRow,targetCol,app):
                        tile1 = app.map[targetRow][targetCol]
                        tile2 = app.map[targetRow - 1][targetCol]
                        if tile1.object == None and tile2.object == None:
                            if rightMiddleNoDrawCt < 3:
                                rightMiddleNoDrawCt += 1
                            else:
                                app.map[targetRow][targetCol].isInFOV = True
                                self.currFOV.append((targetRow,targetCol))
                        else:
                            break
            
    def clearCurrFOV(self,app):
        for (row,col) in self.currFOV:
            app.map[row][col].isInFOV = False




class Enemy(Character):
    def __init__(self,name,left,top,width,height,row,col,patrolNodes):
        super().__init__(name,left,top,width,height,row,col)
        self.isStabbing = False
        self.HP = 100
        self.patrolLogic = patrolNodes
        self.dx = 1
        self.dy = 1
        self.inChase = False
        self.inPatrol = True
        self.inInvestigate = False
        self.inSearch = False
        self.speed = 10
        self.alertMeter = 0
        self.susCounter = 0
        self.hearingRadius = 4
        self.currHearing = []
        self.startedChase = False
        self.firstDetection = False
        self.searchedTiles = 0
        self.searchMap = []
        self.searchTile = None
        self.numberOfTileSearched = 0
        self.searchCurrStep = 0
        self.currSearchPath = None
        self.patrolNodes = patrolNodes
        self.currPatrolNodeIndex = 0
        self.alreadyGeneratedPatrolPath = False
        self.currPatrolPath = None

        

    def __repr(self):
        return f'{self.name}'
    
    def __hash__(self):
        return hash(str(self))

    def draw(self,app):
        '''if self.orientation == 'up':
            drawImage(app.enemyPicUp,self.left,self.top,width=self.width, height=self.height)
        elif self.orientation == 'down':
            drawImage(app.enemyPicDown,self.left,self.top,width=self.width, height=self.height)
        elif self.orientation == 'right':
            drawImage(app.enemyPicRight,self.left,self.top,width=self.width, height=self.height)
        elif self.orientation == 'left':
            drawImage(app.enemyPicLeft,self.left,self.top,width=self.width, height=self.height)'''
        if self.HP > 0 and self.isStabbing == True:
            #draw stabbing animation
            pass
        elif self.HP > 0:
            if self.orientation == 'up':
                drawImage(app.enemyUp,self.left,self.top,width=self.width, height=self.height)
            elif self.orientation == 'down':
                drawImage(app.enemyDown ,self.left,self.top,width=self.width, height=self.height)
            elif self.orientation == 'right':
                drawImage(app.enemyRight,self.left,self.top,width=self.width, height=self.height)
            elif self.orientation == 'left':
                drawImage(app.enemyLeft,self.left,self.top,width=self.width, height=self.height)
            
        elif self.HP == 0:
            
            drawImage(app.enemyDead,self.left,self.top,width=self.width, height=self.height)
        
        #because this function is called on step in redrawall, use it to check if player is in fov
        

    def die(self):
        self.HP = 0

    def isInBounds(self,row,col,app):
        if row >= 0 and row < app.rows and col >= 0 and col < app.cols:
            return True
        return False
    
    #Perception:

    #Hearing
    #yes if I can hear my roommate dancing enemies can hear through wall
    

    #FOV related stuff
    def createFOV(self, app):
        super().createFOV(app)
    
    def clearCurrFOV(self, app):
        super().clearCurrFOV(app)
    
    def checkFOV(self,app):
        
        #how fast alertMeter buildup is exponential to how close player is to enemy
        if (app.playerRow, app.playerCol) in self.currFOV:
            distance = (app.playerRow - self.row)**2 + (app.playerCol - self.col)**2
            increment = 1 - distance * 0.01
            self.alertMeter += increment
        else:
            self.alertMeter -= 1
            if self.alertMeter < 0:
                self.alertMeter = 0

        #top cap of alertmeter
        if self.alertMeter > 50:
            self.alertMeter = 49

        #if player is detected start chase and chase will last while
        elif self.alertMeter >= 20 and self.firstDetection == False:
            self.alertMeter = 100
            self.firstDetection = True
            self.alreadyGeneratedPatrolPath = False
            self.inInvestigate = False
            self.inPatrol = False
            self.inChase = True

        #player out of FOV, start searching
        elif self.alertMeter < 20 and self.firstDetection == True:
            self.firstDetection = False
            self.inSearch = True
            self.alreadyGeneratedPatrolPath = False
            #self.searchRadius
            self.inPatrol = False
            self.inChase = False

            #check if player out of all enemies' view
        
        
                    
                    

    #randomly select a tile in a square of 4 around the LKL
    def generateRandomSearchTile(self,app,searchTileTuple):
        valid = False
        while not valid:
            dR = random.randint(-10,10)
            targetRow = dR + searchTileTuple[0]
            dC = random.randint(-10,10)
            targetCol = dC + searchTileTuple[1]
            if self.isInBounds(targetRow,targetCol,app) and (targetRow, targetCol) != (self.row,self.col):
                tile = app.map[targetRow][targetCol]
                if tile.object == None:
                    return (targetRow,targetCol)

        

        
    def heardSomething(self,targetTileRowAndCol):
        print("I heard something")
        self.investigate(app,targetTileRowAndCol)

    #investigate. is sus counter is 0, just look around before resume normal. if more than 1, start searching
    def investigate(self,app,susTile):
        print('investigating!')
        
        self.moveToLocation((self.row,self.col),susTile)
        if self.susCounter == 0:
            self.lookAround()
            
            
    def lookAround(self):
        print('looking around!')
        A = time.time()
        B = time.time()
        timer = B - A
        while timer < 4:
            if timer < 1:
                self.orientation = 'up'
            elif 1 < timer < 2:
                self.orientation = 'right'
            elif 2 < timer < 3:
                self.orientation = 'down'
            elif 3 < timer < 4:
                self.orientation = 'left'
            B = time.time()
            timer = B - A
                 

    #patrol logic
    def patrol(self,app):
        pass
        
    #chase logic
    def startChase(self,app):
        self.startedChase = True
        while self.inChase == True:
            distance = abs(self.row - app.playerRow) + abs(self.col - app.playerCol)
            #while distance more than 5, take 5 steps than recalculate position
            if distance > 5:
                #take 5 steps while take 1 when closer
                self.takeXStepsTowardsLocation((self.row,self.col),(app.playerRow, app.playerCol),5)
            elif 3 < distance <= 5:
                self.takeXStepsTowardsLocation((self.row,self.col),(app.playerRow, app.playerCol),1)
            else:
            #distance = abs(self.row - app.playerRow) + abs(self.col - app.playerCol)
                self.inChase = False
                self.startedChase = False
                self.alertMeter = -10

            #melee logic
            #if isRightNextToEachOther((self.row,self.col),(app.player.row,app.player.col)):
                #self.melee(app)

    def takeAStep(self,app,targetRow,targetCol):
        path = []
        visited = set()
        pathFindingMap = self.makePathFindingMap(app)
        start = (self.row,self.col)
        end = (targetRow,targetCol)
        path = findShortestPath(pathFindingMap, start, end, path,visited)
        
        if path == None:
            print('''I can't get there''')
        else:
            targetRow = path[0][0]
            targetCol = path[0][1]
            dRow = targetRow - self.row
            dCol = targetCol - self.col
            self.move(app,dRow,dCol)
            path.pop(0)
            print('took a step')
                

    def stabPlayer(self,app):
        self.playMeleeAnimation()
        app.playerHP -= 50
    
    def playMeleeAnimation(self):
        self.isStabbing = True

    #pathfinding

    #make a 2D pathfinding map where 0 is walkable and 1 is not. The same row and col as the game map
    def makePathFindingMap(self,app):
        pathFindingMap = []
        for row in range(app.rows):
            pathFindingMap.append([])
            for col in range(app.cols):
                tile = app.map[row][col]
                #if (tile.character != None and tile.character != self and tile.character != Player) or tile.object != None:
                if (tile.character == Enemy and (tile.row,tile.col) != (self.row,self.col)) or tile.object != None:
                    pathFindingMap[row].append(1)
                else:
                    pathFindingMap[row].append(0)
        
        return pathFindingMap

    
    #move to location
    def takeXStepsTowardsLocation(self,start,end,X):
        print(f'taking {X} steps!')
        path = []
        visited = set()
        pathFindingMap = self.makePathFindingMap(app)
        path = findShortestPath(pathFindingMap, start, end, path,visited)
        currStep = 0
        print('we are here')
        if path == None:
            print('''I can't get there''')
        else:
            while currStep < X and len(path) > 0:
                if app.counter % 10 == 0: 
                    targetRow = path[0][0]
                    targetCol = path[0][1]
                    dRow = targetRow - self.row
                    dCol = targetCol - self.col
                    self.move(app,dRow,dCol)
                    path.pop(0)
                    currStep += 1
    

    def moveToLocation(self,start,end):
        path = []
        visited = set()
        pathFindingMap = self.makePathFindingMap(app)
        path = findShortestPath(pathFindingMap, start, end, path,visited)
        if path == None:
            print('''I can't get there''')
        else:
            while self.inChase == False and len(path) > 0:
                targetRow = path[0][0]
                targetCol = path[0][1]
                dRow = targetRow - self.row
                dCol = targetCol - self.col    
                self.move(app,dRow,dCol)
                path.pop(0)
    

    #have not implemented collision logic for objects and characters
    def move(self,app,dRow,dCol):
        #if app.counter % 10 == 0:
        if dRow > 0:
            self.orientation = 'down'
        elif dRow < 0:
            self.orientation = 'up'
        elif dCol > 0:
            self.orientation = 'right'
        elif dCol < 0:
            self.orientation = 'left'
        
        self.clearCurrFOV(app)
         
        app.map[self.row][self.col].character = None 
        self.row += dRow
        self.top += dRow * self.height
        self.col += dCol
        self.left += dCol * self.width
        app.map[self.row][self.col].character = self
        


class Player(Character):
    def __init__(self,name,left=0,top=0,width=0,height=0,row=0,col=0):
        super().__init__(name,left,top,width,height,row,col)
        self.speed = 10
        self.isCrouched = False
        
    
    def draw(self,app):
        if self.orientation == 'up':
            drawImage(app.playerUp,self.left,self.top,width=self.width, height=self.height)
        elif self.orientation == 'down':
            drawImage(app.playerDown ,self.left,self.top,width=self.width, height=self.height)
        elif self.orientation == 'right':
            drawImage(app.playerRight,self.left,self.top,width=self.width, height=self.height)
        elif self.orientation == 'left':
            drawImage(app.playerLeft,self.left,self.top,width=self.width, height=self.height)

    #detection related:

    def checkIfInHearingRadius(self,app):
        pass
        '''if (self.row,self.col) in enemy.currHearing and enemy.inChase == False:
                enemy.heardSomething((self.row,self.col))'''
                

    #action:
    def CQC(self,app):
        for enemy in app.enemyList:
            if abs(self.row - enemy.row) + abs(self.col - enemy.col) == 1:
                self.playCQCAnimation()
                enemy.die()

    def playCQCAnimation(self):
        pass

    #movement:
    def setLocation(self,left,top,width,height,row,col):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.row = row
        self.col = col
    
    def moveUp(self,app):
        if self.row != 0:
            tile = app.map[self.row - 1][self.col]
            if tile.character == None and tile.object == None:
                self.orientation = 'up'
                app.map[self.row][self.col].character = None 
                self.row -= 1 
                self.top -= self.height
                app.map[self.row][self.col].character = self
                app.playerRow = self.row
                app.playerCol = self.col
                if self.isCrouched == False:
                    self.checkIfInHearingRadius(app)
                

                
    def moveDown(self,app):
        if self.row != len(app.map) - 1:
            tile = app.map[self.row + 1][self.col]
            if tile.character == None and tile.object == None:
                self.orientation = 'down'
                app.map[self.row][self.col].character = None 
                self.row += 1 
                self.top += self.height
                app.map[self.row][self.col].character = self
                app.playerRow = self.row
                app.playerCol = self.col
                if self.isCrouched == False:
                    self.checkIfInHearingRadius(app)
                
    
    def moveRight(self,app):
        if self.col != len(app.map[0]) - 1:
            tile = app.map[self.row][self.col + 1]
            if tile.character == None and tile.object == None:
                self.orientation = 'right'
                app.map[self.row][self.col].character = None 
                self.col += 1 
                self.left += self.width
                app.map[self.row][self.col].character = self
                app.playerRow = self.row
                app.playerCol = self.col
                if self.isCrouched == False:
                    self.checkIfInHearingRadius(app)
                
                

    def moveLeft(self,app):
        if self.col != 0:
            tile = app.map[self.row][self.col - 1]
            if tile.character == None and tile.object == None:
                self.orientation = 'left'
                app.map[self.row][self.col].character = None 
                self.col -= 1 
                self.left -= self.width
                app.map[self.row][self.col].character = self
                app.playerRow = self.row
                app.playerCol = self.col
                if self.isCrouched == False:
                    self.checkIfInHearingRadius(app)
                
