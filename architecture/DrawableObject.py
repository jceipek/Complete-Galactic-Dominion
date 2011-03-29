#import useful modules here
import pygame
from GameData import loadImage, ImageBank

class DrawableObject():
    """This is the super class of all object that can be drawn to the screen"""
    
    imageBank = ImageBank()
    
    def __init__(self, imagePath, colorkey=None):
        
        # First class to have image and rect objects
        
        self.loadImage(imagePath,colorkey)

    # First loadImage method
    def loadImage(self, imagePath, colorkey=None):
        
        objImageAndRect = self.__class__.imageBank.getImageAndRect(imagePath)
        
        if objImageAndRect == None:
            self.__class__.imageBank.loadImage(imagePath,colorkey)
            self.image, self.rect = self.__class__.imageBank.getImageAndRect(imagePath)
        else:
            self.image, self.rect = objImageAndRect
        #return loadImage(imagePath,colorkey)

if __name__ == "__main__":
    screenSize = (width, height) = (1024, 768)
    screenLoc = [0.0, 0.0]

    RUNNING = True
    pygame.init()
    screen = pygame.display.set_mode(screenSize)
    screenZone = screen.get_rect()

    a = DrawableObject('newGrass.png',(255,0,255))
    
    while RUNNING:
        pygame.init()
        screen.blit(a.image,a.rect)
        pygame.display.flip()
