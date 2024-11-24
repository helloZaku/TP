from cmu_graphics import *
class Tiles:

    def __init__(self,cx,cy,width,height,hasCharacter = None,hasObject = None):
        self.isInDetection = False
        self.hasCharacter = hasCharacter
        self.hasObject = hasObject
        self.cx = cx
        self.cy = cy
        self.width = width
        self.height = height

    def draw(self):
        if self.hasObject != None:
            drawRect(self.cx,self.cy,self.width,self.height,fill = 'yellow')
        elif self.hasCharacter != None:
            drawRect(self.cx,self.cy,self.width,self.height,fill = 'red')) 
        
