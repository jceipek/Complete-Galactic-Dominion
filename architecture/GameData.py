import pygame

class ImageBank():
    """
    Contains a dictionary which maps image names to 
    pygame.surface.Surface objects.  This makes the creation of a new
    sprite much faster, as the filepath does not have to be loaded each
    time.
    """
    def __init__(self):

        # Contains all images
        self.images = dict()
        
        # Contains color keys of images
        self.imageColorKeys = dict()
        
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
        
    def getImageAndRect(self, imageName):
        """
        Returns a tuple of 2 elements from the dictionary by key
        if it exists.
        [0] - a pygame.Surface image
        [1] - the rectangle associated with said Surface
        If not, None is returned.
        """
        image = self.images.get(imageName,None)
        if image == None:
            return None
        else:
            return (image,image.get_rect())
    '''        
    def getAverageColor(self, imageName, colorkey=None):
        
        if imageName in self.imageColorKeys:
            return self.imageColorKeys[imageName]
        else:
            self.imageColorKeys[imageName]=getAverageColor(imageName,colorkey)
            return self.imageColorKeys[imageName]
    '''
    
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

'''
def getAverageColor(imagePath, colorkey=None):
    """
    Returns the average color of an image given an image filepath.
    The colorkey is used to determine which color should not be
    included in the determination of the average color.  If -1,
    the topleft-most pixel will be used to determine the average
    value.  If the colorkey is a tuple, this color value will be
    excluded from the calculation.
    
    Returned value is a tuple of r,g,b value on a 0-255 scale.
    """
    
    from PIL import Image
    
    pic = Image.open(imagePath)
    imgData = pic.load()
    
    testPixel = imgData[0,0]
    picSize = pic.size

    if colorkey == -1:
        backgroundColor = testPixel
    elif isinstance(colorkey,tuple):
        backgroundColor = testPixel
    else:
        backgroundColor = None
    
    # Counts number of pixels in an image
    # partial pixels for alpha transparency
    fullPixelCounter = 0
    
    # FIXME - NOT VERY PRETTY.  COULD BE REFACTORED.  LOW PRIORITY THOUGH.
    
    if len(testPixel) == 4:
        
        red,green,blue,alpha = 0,0,0,0
            
        for x in xrange(picSize[0]):
            for y in xrange(picSize[1]):
                rAdd,gAdd,bAdd,aAdd = imgData[x,y]
                
                if not backgroundColor == (rAdd,gAdd,bAdd,aAdd):
                    
                    pixelFrac = ((aAdd)/255.0)
                    
                    fullPixelCounter+=pixelFrac
                    red+=rAdd*pixelFrac
                    green+=gAdd*pixelFrac
                    blue+=bAdd*pixelFrac
                    alpha+=aAdd
        
    elif len(testPixel) == 3:
        
        red,green,blue = 0,0,0
        
        for x in xrange(pic.size[0]):
            for y in xrange(pic.size[1]):
                rAdd,gAdd,bAdd = imgData[x,y]
                
                if not backgroundColor == (rAdd,gAdd,bAdd):
                    fullPixelCounter+=1
                    red+=rAdd
                    green+=gAdd
                    blue+=bAdd
        
    else: return None
    
    return int((red/fullPixelCounter)), \
            int((green/fullPixelCounter)), \
            int((blue/fullPixelCounter))
'''

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
