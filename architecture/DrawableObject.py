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
        
    # First loadImage method
    def loadImage(self, imagePath, colorkey=None):
        
        objImageAndRect = self.__class__.imageBank.getImageAndRect(imagePath)
        
        if objImageAndRect == None:
            self.__class__.imageBank.loadImage(imagePath,colorkey)
            self.image, self.rect = self.__class__.imageBank.getImageAndRect(imagePath)
        else:
            self.image, self.rect = objImageAndRect
    '''       
    def setAverageColor(self,imagePath,colorkey=None):
        """
        Sets the averageColor attribute of something with an image.
        """
        self.averageColor = self.__class__.imageBank.getAverageColor(imagePath,colorkey)

    def getAverageColor(self):
        """
        Returns the average color of the image.
        """
        return self.averageColor
    '''

if __name__ == "__main__":
    screenSize = (width, height) = (1024, 768)
    screenLoc = [0.0, 0.0]

    RUNNING = True
    pygame.init()
    screen = pygame.display.set_mode(screenSize)
    screenZone = screen.get_rect()

    a = DrawableObject('orbPurpleBlack.png',(255,255,255))
    #print a.getAverageColor()
    
    while RUNNING:
        pygame.init()
        screen.blit(a.image,a.rect)
        pygame.display.flip()
