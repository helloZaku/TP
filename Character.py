from cmu_graphics import *

class Character:
    def __init__(self,name,left,top,width,height):
        self.name = name
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        
    
    def draw(self):
        drawRect(self.left,self.top,self.width,self.height,fill = 'green')

class Enemy(Character):
    def __init__(self,name,left,top,width,height):
        super().__init__(name,left,top,width,height)
        self.HP = 100
    
    def draw(self):
        super().draw()
