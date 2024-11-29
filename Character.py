from cmu_graphics import *
from Tiles import *
from Character import *
from Node import *
import time

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
        for i in range(3):
            if self.orientation == 'up':
                if self.row - i >= 0:
                    tile = app.map[self.row - i][self.col]
                    if tile.object == None and tile.character == None:
                        app.map[self.row - i][self.col].isInFOV = True
                        self.currFOV.append((self.row - i,self.col))
            elif self.orientation == 'down':
                if self.row + i != len(app.map) - 1:
                    tile = app.map[self.row + i][self.col]
                    if tile.object == None and tile.character == None:
                        app.map[self.row + i][self.col].isInFOV = True
                        self.currFOV.append((self.row + i,self.col))
            elif self.orientation == 'right':
                if self.col + i != len(app.map[0]) - 1:
                    tile = app.map[self.row][self.col + i]
                    if tile.object == None and tile.character == None:
                        app.map[self.row][self.col + i].isInFOV = True
                        self.currFOV.append((self.row,self.col + i))
            elif self.orientation == 'left':
                if self.col - i != 0:
                    tile = app.map[self.row][self.col - i]
                    if tile.object == None and tile.character == None:
                        app.map[self.row][self.col - i].isInFOV = True
                        self.currFOV.append((self.row,self.col - i))
    
    def clearCurrFOV(self,app):
        for (row,col) in self.currFOV:
            app.map[row][col].isInFOV = False
    
    

    #def draw(self):
        #drawPolygon(x, y, x+size, y, x+size/2, topY, fill='black')
        #drawRect(self.left,self.top,self.width,self.height,fill = 'red')
        #



class Enemy(Character):
    def __init__(self,name,left,top,width,height,row,col,patrolLogic):
        super().__init__(name,left,top,width,height,row,col)
        self.HP = 100
        self.patrolLogic = patrolLogic
        self.dx = 1
        self.dy = 1
        self.inChase = False
        self.inPatrol = False
        self.inInvestigate = False
        self.speed = 10
        self.alertMeter = 0
        self.susCounter = 0
        

    '''def __repr(self):
        return f'{self.name}'''

    def draw(self,app):
        '''if self.orientation == 'up':
            drawImage(app.enemyPicUp,self.left,self.top,width=self.width, height=self.height)
        elif self.orientation == 'down':
            drawImage(app.enemyPicDown,self.left,self.top,width=self.width, height=self.height)
        elif self.orientation == 'right':
            drawImage(app.enemyPicRight,self.left,self.top,width=self.width, height=self.height)
        elif self.orientation == 'left':
            drawImage(app.enemyPicLeft,self.left,self.top,width=self.width, height=self.height)'''
        drawRect(self.left,self.top,self.width,self.height,fill = 'red')
        self.createFOV(app)
        
        #because this function is called on step in redrawall, use it to check if player is in fov
        self.checkFOV(app)


    #investigate. is sus counter is 0, just look around before resume normal. if more than 1, start searching
    def investigate(self,app,susTile):
        self.moveToLocation((self.row,self.col),susTile)
        orientations = ['up','right','down','left']
        if self.susCounter == 0:
            if app.counter % 5 == 0:
                self.orientation = 'up'
                startTime = time.time()
                currTime = time.time()

            elif app.counter % 10 == 0:
                self.orientation = 'up'
            elif app.counter % 15 == 0:
                self.orientation = 'up'
            elif app.counter % 20 == 0:
                self.orientation = 'up'
            
        

    #known feature: enemy teleport back to starting position when cannot move forward
    def patrol(self,app):
        if self.patrolLogic == 'straightVertical':
            if self.row == 0 or self.row == len(app.map) - 1:
                self.dy = -self.dy
            nextTile = app.map[self.row + self.dy][self.col]
            if nextTile.character == None:
                app.map[self.row][self.col].character = None 
                self.row += self.dy
                self.top += self.dy * self.height
                app.map[self.row][self.col].character = self
            else:
                self.dy = -self.dy

        elif self.patrolLogic == 'straightHorizontal':
            if self.col == 0 or self.col == len(app.map[0]) - 1:
                self.dx = -self.dx

            nextTile = app.map[self.row][self.col + self.dx]
            if nextTile.character == None:
                app.map[self.row][self.col].character = None 
                self.col += self.dx
                self.left += self.dx * self.width
                app.map[self.row][self.col].character = self
            else:
                self.dx = -self.dx
    #pathfinding
    
    def chase(self,app):
        
        maze = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ]

               
        start = (self.row,self.col)
        end = (app.playerRow, app.playerCol)

        self.moveToLocation(maze,start,end)

    def moveToLocation(maze,start,end):
        path = astar(maze, start, end)
        if len(path) > 2:
            targetRow = path[1][0]
            targetCol = path[1][1]
            dRow = targetRow - self.row
            dCol = targetCol - self.col

            #speed
            #if app.counter % 10 == 0:
            self.move(app,dRow,dCol)

    #FOV related stuff
    def createFOV(self, app):
        super().createFOV(app)
    
    def clearCurrFOV(self, app):
        super().clearCurrFOV(app)
    
    def checkFOV(self,app):
        print(self.alertMeter)
        if (app.playerRow, app.playerCol) in self.currFOV:
            self.alertMeter += 1
        else:
            self.alertMeter -= 1
            if self.alertMeter < 0:
                self.alertMeter = 0

        #top cap of alertmeter
        if self.alertMeter > 300:
            self.alertMeter = 299

        #if player is detected start chase and chase will last while
        if self.alertMeter >= 50:
            self.alertMeter = 200
            self.inInvestigate = False
            self.inPatrol = False
            self.inChase = True

        #player out of FOV, start investigating
        if self.alertMeter < 100:
            self.inInvestigate = True
            self.inPatrol = False
            self.inChase = False

        #must have been the wind
        if self.alertMeter == 0:
            self.inInvestigate = False
            self.inPatrol = True
            self.inChase = False

    #have not implemented collision logic for objects and characters
    def move(self,app,dRow,dCol):
        if app.counter % 10 == 0:
            if dRow > 0:
                self.orientation = 'down'
            elif dRow < 0:
                self.orientation = 'up'
            elif dCol > 0:
                self.orientation = 'right'
            elif dCol < 0:
                self.orientation = 'left'

            app.map[self.row][self.col].character = None 
            self.row += dRow
            self.top += dRow * self.height
            self.col += dCol
            self.left += dCol * self.width
            app.map[self.row][self.col].character = self
            self.clearCurrFOV(app)



class Player(Character):
    def __init__(self,name,left=0,top=0,width=0,height=0,row=0,col=0):
        super().__init__(name,left,top,width,height,row,col)
        self.HP = 100
        self.speed = 10
        
    
    def draw(self,app):
        drawRect(self.left,self.top,self.width,self.height,fill = 'blue')
        
    
    def setLocation(self,left,top,width,height,row,col):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.row = row
        self.col = col
    
    def createFOV(self, app):
        super().createFOV(app)
    
    def clearCurrFOV(self, app):
        super().clearCurrFOV(app)

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
                self.clearCurrFOV(app)

                
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
                self.clearCurrFOV(app)
    
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
                self.clearCurrFOV(app)
                

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
                self.clearCurrFOV(app)

