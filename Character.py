from cmu_graphics import *

class Character:
    def __init__(self,name,left,top,width,height,row,col):
        self.name = name
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.row = row
        self.col = col
        
    def draw(self):
        drawRect(self.left,self.top,self.width,self.height,fill = 'green')



class Enemy(Character):
    def __init__(self,name,left,top,width,height,row,col,patrolLogic):
        super().__init__(name,left,top,width,height,row,col)
        self.HP = 100
        self.patrolLogic = patrolLogic
        self.dx = 1
        self.dy = 1
    
    '''def __repr(self):
        return f'{self.name}'''

    def draw(self):
        super().draw()

    def patrol(self,app):
        if self.patrolLogic == 'straightVertical':
            if self.row == 0 or self.row == len(app.map) - 1:
                self.dy = -1 * self.dy
            else:
                tile = app.map[self.row + self.dy][self.col]
                if tile.character == None:
                    app.map[self.row][self.col].character = None 
                    self.row += self.dy
                    self.top += self.dy * self.height
                    app.map[self.row][self.col].character = self
                else:
                    self.dy = -1 * self.dy
            

        elif self.patrolLogic == 'straightHorizontal':
            if self.col == 0 or self.row == len(app.map[0]) - 1:
                self.dx = -1 * self.dx
            else:
                tile = app.map[self.row][self.col + self.dx]
                if tile.character == None:
                    app.map[self.row][self.col].character = None 
                    self.col += self.dx
                    self.left += self.dx * self.width
                    app.map[self.row][self.col].character = self
                else:
                    self.dx = -1 * self.dx
        
    

class Player(Character):
    def __init__(self,name,left=0,top=0,width=0,height=0,row=0,col=0):
        super().__init__(name,left,top,width,height,row,col)
        self.HP = 100
    
    def draw(self):
        drawRect(self.left,self.top,self.width,self.height,fill = 'blue')
    
    def setLocation(self,left,top,width,height,row,col):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.row = row
        self.col = col

    #movement logic. the methods return true if the movement if legal
    def moveUp(self,app):
        if self.row != 0:
            tile = app.map[self.row - 1][self.col]
            if tile.character == None:
                app.map[self.row][self.col].character = None 
                self.row -= 1 
                self.top -= self.height
                app.map[self.row][self.col].character = self

                
    def moveDown(self,app):
        if self.row != len(app.map) - 1:
            tile = app.map[self.row + 1][self.col]
            if tile.character == None:
                app.map[self.row][self.col].character = None 
                self.row += 1 
                self.top += self.height
                app.map[self.row][self.col].character = self
    
    def moveRight(self,app):
        if self.col != len(app.map[0]) - 1:
            tile = app.map[self.row][self.col + 1]
            if tile.character == None:
                app.map[self.row][self.col].character = None 
                self.col += 1 
                self.left += self.width
                app.map[self.row][self.col].character = self
                

    def moveLeft(self,app):
        if self.col != 0:
            tile = app.map[self.row][self.col - 1]
            if tile.character == None:
                app.map[self.row][self.col].character = None 
                self.col -= 1 
                self.left -= self.width
                app.map[self.row][self.col].character = self

