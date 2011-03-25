#import useful modules here
import pygame

class DrawableObject():
    """This is the super class of all object that can be drawn to the screen"""
    def __init__(self, imagePath, colorkey=None):

        # First class to have image and rect objects
        self.image, self.rect = self.loadImage(imagePath,colorkey)

    # First loadImage method
    def loadImage(self, imagePath, colorkey=None):
        
        # If there is a filepath given, load that file.
        if isinstance(imagePath,str):
            
            try:
                image = pygame.image.load(imagePath)
            except pygame.error, message:
                print 'Cannot load image:', imagePath
                raise SystemExit, message
                
            if colorkey == 'alpha':
                image = image.convert_alpha()  
            else:
                image = image.convert()
                
                if colorkey is not None:
                    if colorkey is -1:
                        colorkey = image.get_at((0,0))
                    image.set_colorkey(colorkey)
                
        # If there is a pygame.Surface given        
        elif isinstance(imagePath,pygame.Surface):
            
                image = imagePath
                
        else:
            raise TypeError, 'please provide pygame.Surface or filepath.'
        
        return image, image.get_rect()

if __name__ == "__main__":
    screenSize = (width, height) = (1024, 768)
    screenLoc = [0.0, 0.0]

    RUNNING = True
    pygame.init()
    screen = pygame.display.set_mode(screenSize)
    screenZone = screen.get_rect()
    
    a = DrawableObject('testBuilding.png','alpha')
    
    while RUNNING:
        pygame.init()
        screen.blit(a.image,a.rect)
        pygame.display.flip()
    
