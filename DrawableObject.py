#import useful modules here
import pygame.image

class DrawableObject():
    """This is the super class of all object that can be drawn to the screen"""
    def __init__(self, imagePath, colorkey=None):

        # First class to have image and rect objects
        self.image, self.rect = self.loadImage(imagePath,colorkey)

    # First loadImage method
    def loadImage(self, name, colorkey=None):
        fullname = os.path.join('data', name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error, message:
            print 'Cannot load image:', name
            raise SystemExit, message
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image, image.get_rect()
