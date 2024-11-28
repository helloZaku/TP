from cmu_graphics import *
from Tiles import *
from Character import *
from Node import *
class Tiles:

    def __init__(self,left,top,width,height,Character = None,Object = None):
        self.isInDetection = False
        self.character = Character
        self.Object = Object
        self.left = left
        self.top = top
        self.width = width
        self.height = height
    
    def __repr__(self):
        return f'left = {self.left},top = {self.top}, width = {self.width}, height = {self.height}, character = {self.character}'

    def draw(self):
        if self.Object != None:
            self.Object.draw
        elif self.character != None:
            self.character.draw()
        elif self.isInDetection == True:
            drawRect(self.left,self.top,self.width,self.height,fill = 'yellow')
        
