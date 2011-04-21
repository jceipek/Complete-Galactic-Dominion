#import useful modules here
#import pygame
import pygame.display
from GameData import loadImage, ImageBank

class DrawableObject(object):
    """This is the super class of all object that can be drawn to the screen"""
    
    imageBank = ImageBank()
    isImageInitialized = False
    
    def __init__(self, imagePath, colorkey=None):
        
        # First class to have image and rect objects
        self.imagePath = imagePath
        self.colorkey = colorkey
        self.colorkey = colorkey
        
        '''
        self.loadImage(imagePath,colorkey)
        self.setAverageColor(imagePath,colorkey)
        self.realCenter = self.rect.center
        '''
        
        self._imageInformationSetup()
        
    def _imageInformationSetup(self):
        if pygame.display.get_init():
            self.loadImage(self.imagePath,self.colorkey)
            self.setAverageColor(self.imagePath,self.colorkey)
            self.realCenter = self.rect.center
            self.isImageInitialized = True
    
    # First loadImage method
    
    def loadImage(self, imagePath, colorkey=None):
        
        objImageAndRect = self.imageBank.getImageAndRect(imagePath)
        
        if objImageAndRect == None:
            self.imageBank.loadImage(imagePath,colorkey)
            self.image, self.rect = self.imageBank.getImageAndRect(imagePath)
        else:
            self.image, self.rect = objImageAndRect
          
    def setAverageColor(self,imagePath,colorkey=None):
        """
        Sets the averageColor attribute of something with an image.
        """
        self.averageColor = self.imageBank.getAverageColor(imagePath,colorkey)

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
        
    def draw(self,screen):
        """
        Blits the image onto the location of the rect on the given screen.
        """
        if self.isImageInitialized:
            screen.blit(self.image,self.rect)
        else:
            self._imageInformationSetup()

class DrawableObjectGroup(DrawableObject):
    
    def __init__(self,imageList):
        #imageList is a list of tuples and values that indicate
        #image paths and colorkeys
        
        self.drawableObjectList = []
        self.addObjectsFromImageList(imageList)
    
        self._imageInformationSetup()
        
    def _imageInformationSetup(self):
        if pygame.display.get_init():
            for drawableObject in self.drawableObjectList:
                drawableObject.loadImage(drawableObject.imagePath,drawableObject.colorkey)
                drawableObject.setAverageColor(drawableObject.imagePath,drawableObject.colorkey)
                drawableObject.realCenter = drawableObject.rect.center
                drawableObject.isImageInitialized = True
    
    def addObjectsFromImageList(self,aList):
        #aList is a list of tuples and values that indicate
        #image paths and colorkeys
        
        for t in aList:
            if isinstance(t,tuple):
                self.drawableObjectList.append(DrawableObject(t[0], t[1]))
            else:
                self.drawableObjectList.append(DrawableObject(t,None))

    def draw(self,screen):
        
        for drawableObject in self.drawableObjectList:
            if drawableObject.isImageInitialized:
                #print drawableObject.rect
                screen.blit(drawableObject.image,drawableObject.rect)
            else:
                self._imageInformationSetup()

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
