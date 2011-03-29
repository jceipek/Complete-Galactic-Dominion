import pygame

class ImageBank():
    """
    Contains a dictionary which maps image names to 
    pygame.surface.Surface objects.  This makes the creation of a new
    sprite much faster, as the filepath does not have to be loaded each
    time.
    """
    def __init__(self):

        self.images = dict()
        self.imagesAndRects = dict()
        
    def hasImageKey(self, image):
        """
        Returns whether or not an image is in the dictionary by key.
        """
        return image in self.images
        
    def hasImageValue(self, image):
        """
        Returns whether or not an image instance is in the dictionary.
        """
        return image in self.images.values()
        
    def loadImage(self, imageName, colorkey):
        """
        Loads an image into the image dictionary if filepath specified.
        """
        if isinstance(imageName,str) and not self.hasImageKey(imageName):
            
            image, imageRect = loadImage(imageName, colorkey)
            
            self.images[imageName] = image
            self.imagesAndRects[imageName] = (image,image.get_rect())
            
    def getImage(self, imageName):
        """
        Returns an image from the dictionary by key if it exists.  If 
        not, None is returned.
        """
        return self.images.get(imageName,None)
        
    def getImageAndRect(self, imageName):
        """
        Returns a tuple of 2 elements from the dictionary by key
        if it exists.
        [0] - a pygame.Surface image
        [1] - the rectangle associated with said Surface
        If not, None is returned.
        """
        return self.imagesAndRects.get(imageName,None)

def loadImage(imagePath, colorkey=None):
    
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
    elif isinstance(imagePath, pygame.Surface):
        image = imagePath
    else:
        raise TypeError, 'please provide pygame.Surface or filepath.'
    return image, image.get_rect()

class Locals:
    #Statuses
    IDLE = 0
    MOVING = 1
    BUILDING = 2
    GATHERING = 3
    ATTACKING = 4
    #Efficiency
    MOVE=0
    BUILD=1
    GATHER=2
    ATTACK=3
