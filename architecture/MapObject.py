from DrawableObject import DrawableObject
import pygame

class MapObject(DrawableObject, pygame.sprite.Sprite):
    """
    Represents any object which is located in the L{World}.
    First class to implement position in the world.
    """
    def __init__(self, imagePath, x, y, colorkey=None, blendPath=None,
        owner='gaia'):
        # sets image and rect attributes
        # First class to inherit from Sprite
        
        DrawableObject.__init__(self, imagePath, colorkey, blendPath=blendPath,
            owner=owner)
        pygame.sprite.Sprite.__init__(self)
        
        # sets the topleft corner of the rectangle to (x,y)
        self.rect.topleft = (x,y)
        #self.realCenter=[x,y]
        #self.rect.center = (x,y)
        
        # this is the first initialization of owner
        #self.owner=owner # default to no owner
        
        # this is the first initialization of blockable
        # determines whether or not an object can be walked through
        # FUNCTIONALITY NOT CURRENTLY IMPLEMENTED
        self.blockable=False
        
        # rectangle used EXCLUSIVELY for collision detection
        # defaults to the image rectangle
        # NOTE: update methods need to move collRect with rect!
        # FUNCTIONALITY NOT CURRENTLY IMPLEMENTED
        self.collRect = self.rect

    def draw(self,surface):
        # Override
        pass

if __name__ == "__main__":
    screenSize = (width, height) = (1024, 768)
    screenLoc = [0.0, 0.0]

    RUNNING = True
    pygame.init()
    screen = pygame.display.set_mode(screenSize)
    screenZone = screen.get_rect()

    a = MapObject('newGrass.png',100,100,(255,0,255))
    
    pygame.init()
    
    while RUNNING:
        
        screen.blit(a.image,a.rect)
        pygame.display.flip()
