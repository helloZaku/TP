from cmu_graphics import *

class Object():
    def __init__(self,left,top,width,height,row,col):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.row = row
        self.col = col
    
    def draw(self,app):
        drawCircle(self.left,self.top,self.width/2,fill = 'black')

class Wall(Object):
    def __init__(self,left,top,width,height,row,col):
        super().__init__(left,top,width,height,row,col)

    def __repr__(self):
        return f'Wall'
    
    def draw(self,app):
        drawRect(self.left,self.top,self.width,self.height,fill = 'purple')
    
class Dumpster(Object):
    def __init__(self,left,top,width,height,row,col):
        super().__init__(left,top,width,height,row,col)

    def __repr__(self):
        return f'Dumpster'
    
    def draw(self,app):
        drawRect(self.left,self.top,self.width,self.height,fill = 'green')
        drawCircle(self.left + self.width/2,self.top + self.width/2,self.width/2,fill = 'white',align = 'center')
    
class Door(Object):
    def __init__(self,left,top,width,height,row,col):
        super().__init__(left,top,width,height,row,col)
        self.isClosed = True
    
    def draw(self,app):
        if self.isClosed == True:
            drawRect(self.left,self.top,self.width,self.height,fill=None, border='grey',
            borderWidth=self.width / 5)
        
        else:
            drawRect(self.left,self.top,self.width,self.height,fill='grey')
    
