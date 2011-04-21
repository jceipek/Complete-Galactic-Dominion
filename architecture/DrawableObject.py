#import useful modules here
import pygame
from GameData import loadImage, ImageBank

class DrawableObject():
    """This is the super class of all object that can be drawn to the screen"""
    
    imageBank = ImageBank()
    
    def __init__(self, imagePath, colorkey=None):
        
        # First class to have image and rect objects
        
        self.loadImage(imagePath,colorkey)
        self.setAverageColor(imagePath,colorkey)
        self.realCenter = self.rect.center
        
    # First loadImage method
    def loadImage(self, imagePath, colorkey=None):
        
        objImageAndRect = self.__class__.imageBank.getImageAndRect(imagePath)
        
        if objImageAndRect == None:
            self.__class__.imageBank.loadImage(imagePath,colorkey)
            self.image, self.rect = self.__class__.imageBank.getImageAndRect(imagePath)
        else:
            self.image, self.rect = objImageAndRect
          
    def setAverageColor(self,imagePath,colorkey=None):
        """
        Sets the averageColor attribute of something with an image.
        """
        self.averageColor = self.__class__.imageBank.getAverageColor(imagePath,colorkey)

    def getMiniMapColor(self):
        """
        By default, returns the average color.  Override.
        """
        return self.getAverageColor()

    def getAverageColor(self):
        """
        Returns the average color of the image.
        """
        return self.averageColor

class DrawableObjectGroup(DrawableObject):
    
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

    def drawObjects(self,screen):
        for o in self.drawableObjectList:
            print o.rect
            screen.blit(o.image,o.rect)

if __name__ == "__main__":
    screenSize = (width, height) = (1024, 768)
    screenLoc = [0.0, 0.0]

    RUNNING = True
    pygame.init()
    screen = pygame.display.set_mode(screenSize)
    screenZone = screen.get_rect()

    a = DrawableObject('orbPurpleBlack.png',(255,255,255))
    print a.getAverageColor()
    
    while RUNNING:
        pygame.init()
        screen.blit(a.image,a.rect)
        pygame.display.flip()
