from DrawableObject import loadImage

class ImageBank():
    """
    Contains a dictionary which maps image names to 
    pygame.surface.Surface objects.  This makes the creation of a new
    sprite much faster, as the filepath does not have to be loaded each
    time.
    """
    def __init__(self):

        self.images = dict()
        
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
            
    def getImage(self, imageName):
        """
        Returns an image from the dictionary by key if it exists.  If 
        not, None is returned.
        """
        return self.images.get(imageName,None)

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
