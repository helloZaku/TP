from cmu_graphics import *
class Tiles:

    def __init__(self,left,top,width,height,Character = None,Object = None):
        self.isInDetection = False
        self.Character = Character
        self.Object = Object
        self.left = left
        self.top = top
        self.width = width
        self.height = height
    
    def __repr__(self):
        return f'left = {self.left},top = {self.top}, width = {self.width}, height = {self.height}, character = {self.Character}'

    def draw(self):
        if self.Object != None:
            #self.Object.draw
            pass
        elif self.Character != None:
            self.Character.draw()
        elif self.isInDetection == True:
            drawRect(self.left,self.top,self.width,self.height,fill = 'yellow')
        
