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
    def __init__(self,name,left,top,width,height,row,col):
        super().__init__(name,left,top,width,height,row,col)
        self.HP = 100
    
    def draw(self):
        super().draw()

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
            if tile.Character == None:
                app.map[self.row][self.col].character = None 
                self.row -= 1 
                self.top -= self.height
                app.map[self.row][self.col].character = self

                
    def moveDown(self,app):
        if self.row != len(app.map) - 1:
            tile = app.map[self.row + 1][self.col]
            if tile.Character == None:
                app.map[self.row][self.col].character = None 
                self.row += 1 
                self.top += self.height
                app.map[self.row][self.col].character = self
    
    def moveRight(self,app):
        if self.col != len(app.map[0]) - 1:
            tile = app.map[self.row][self.col + 1]
            if tile.Character == None:
                app.map[self.row][self.col].character = None 
                self.col += 1 
                self.left += self.width
                app.map[self.row][self.col].character = self
                

    def moveLeft(self,app):
        if self.col != 0:
            tile = app.map[self.row][self.col - 1]
            if tile.Character == None:
                app.map[self.row][self.col].character = None 
                self.col -= 1 
                self.left -= self.width
                app.map[self.row][self.col].character = self

