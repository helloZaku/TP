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
        
        
        drawImage(app.wall,self.left,self.top,width=self.width, height=self.height)
    

    
