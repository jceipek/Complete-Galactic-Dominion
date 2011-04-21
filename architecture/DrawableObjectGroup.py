import pygame
from DrawableObject import DrawableObject

class DrawableObjectGroup():
    def __init__(self,imageList):
        #imageList is a list of tuples and values that indicate
        #image paths and colorkeys
        self.drawableObjectList = []
        self.addObjectsFromImageList(imageList)
        
    def addObjectsFromImageList(self,aList):
        #aList is a list of tuples and values that indicate
        #image paths and colorkeys
        
        for t in aList:
            if isinstance(t,tuple):
                self.drawableObjectList.append(DrawableObject(t[0], t[1]))
            else:
                self.drawableObjectList.append(DrawableObject(t,None))
