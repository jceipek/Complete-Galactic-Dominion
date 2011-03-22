#import useful modules here
import pygame.image

class DrawableObject():
    """This is the super class of all object that can be drawn to the screen"""
    def __init__(self, imagePath, colorkey=None):

        # First class to have image and rect objects
        self.image, self.rect = self.loadImage(imagePath,colorkey)

    # First loadImage method
    def loadImage(self, name, colorkey=None):
        try:
            image = pygame.image.load(name)
        except pygame.error, message:
            print 'Cannot load image:', name
            raise SystemExit, message
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey)
        return image, image.get_rect()

if __name__ == "__main__":
    screenSize = (width, height) = (1024, 768)
    screenLoc = [0.0, 0.0]

    RUNNING = True
    pygame.init()
    screen = pygame.display.set_mode(screenSize)
    screenZone = screen.get_rect()
    
    a = DrawableObject('ball.png',(255,255,255))
    
    while RUNNING:
        pygame.init()
        screen.blit(a.image,a.rect)
        pygame.display.flip()
    
