import pygame

def createImageNotFound(dims=(100,80)):
    """
    Sets up an image to use when an image cannot be loaded
    and puts it in the cache as [None]
    """
    imageNotFound = pygame.Surface(dims)
    imageNotFound.fill((180,180,180))
        
    if not pygame.font.get_init():
        pygame.font.init()
        
    font=pygame.font.Font(pygame.font.get_default_font(),12)
    txt=font.render('Image not found.',False,(0,0,0))
    imageNotFound.blit(txt,(5,30))
    
    return imageNotFound

def getAverageColor(surface, colorkey=None):
    """
    Returns the average color of an image given an image filepath.
    The colorkey is used to determine which color should not be
    included in the determination of the average color.  If -1,
    the topleft-most pixel will be used to determine the average
    value.  If the colorkey is a tuple, this color value will be
    excluded from the calculation.
    
    Returned value is a tuple of r,g,b value on a 0-255 scale.
    """
    
    testPixel = surface.get_at((0,0))
    imageRect = surface.get_rect()
    imageWidth = imageRect.width
    imageHeight = imageRect.height

    if colorkey == -1:
        backgroundColor = testPixel
    elif isinstance(colorkey,tuple):
        backgroundColor = colorkey
    else:
        backgroundColor = None
    
    # Counts number of pixels in an image
    # partial pixels for alpha transparency
    fullPixelCounter = 0
    
    if len(testPixel) == 4:
        
        red,green,blue,alpha = 0,0,0,0
            
        for x in xrange(imageWidth):
            for y in xrange(imageHeight):
                rAdd,gAdd,bAdd,aAdd = surface.get_at((x,y))
                
                if not backgroundColor == (rAdd,gAdd,bAdd):
                    
                    pixelFrac = ((aAdd)/255.0)
                    
                    fullPixelCounter+=pixelFrac
                    
                    red+=rAdd*pixelFrac
                    green+=gAdd*pixelFrac
                    blue+=bAdd*pixelFrac
                    alpha+=aAdd
        
    else: return None
    
    if fullPixelCounter == 0:
        return backgroundColor
    else:
        return int((red/fullPixelCounter)), \
                int((green/fullPixelCounter)), \
                int((blue/fullPixelCounter))

def loadImage(imagePath, colorkey=None, status=None):

    # If there is a filepath given, load that file.
    if isinstance(imagePath,str):

        try:
            image = pygame.image.load(imagePath)
        except pygame.error, message:
            print 'Cannot load image:', imagePath
            #raise SystemExit, message
            blank = pygame.Surface((100,80))
            blank.fill((180,180,180))
            
            if not pygame.font.get_init():
                pygame.font.init()
            
            font=pygame.font.Font(pygame.font.get_default_font(),12)
            txt=font.render('Image not found.',False,(0,0,0))
            blank.blit(txt,(5,30))
            
            return blank
            
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
    return image
