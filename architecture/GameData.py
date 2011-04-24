import pygame
from specialImage import loadImage

class ImageBank(object):
    """
    The ImageBank is an image repository that handles image loading.
    The bank allows drawableObjects to load image paths. Instead of
    reloading a preexisting image, the bank returns pygame surfaces
    initialized previously. This makes the creation of a new
    sprite much faster and more memory efficient, as the filepath 
    does not have to be loaded each time.
    
    @param cache: a dictionary that maps from folder paths and image
    paths to AnimationDicts
    """
    def __init__(self):

        self.cache = {}
        self.setImageNotFound()
        
    def setImageNotFound(self):
        from specialImage import createImageNotFound
        self.cache[None] = createImageNotFound()

    def isCached(self,imagePath):
        """
        Checks if the imagePath has already been cached.
        
        NOTE: should we make this recursively check anim dicts or only
        top-level keys (like it is now)?
        """
        
        return imagePath in self.cache
    
    def loadImage(self, imagePath, colorkey):
        """
        Loads an image or animation into the cache as an AnimationDict
        """
        if isinstance(imagePath,str) and not self.isCached(imagePath):
            from os import listdir
            from os.path import isdir,join
            imagePathFull = join('imageData',imagePath)
            try:
                #Is this an anim, not a simple image?
                if isdir(imagePath):
                    images = listdir(imagePathFull)
                    images.sort()
                    animDict = AnimationDict(self.getDefaultImage())
                    for imageI in xrange(len(images)):
                        image = join(imagePathFull,images[imageI])
                        image = loadImage(image, colorkey)
                        animDict.addImage(image,colorkey,imageI)
                        if imageI == 0:
                            animDict.setDefaultImage(animDict.getImage(imageI))
                else:
                    animDict = AnimationDict(self.getDefaultImage())
                    image = loadImage(imagePathFull, colorkey)
                    animDict.addImage(image,colorkey)
                self.cache[imagePath] = animDict
            except:
                animDict = AnimationDict(self.getDefaultImage())
                animDict.addImage(self.getDefaultImage())
                print("UNABLE TO LOAD '"+imagePath+"'")

    def getDefaultImage(self):
        return self.cache[None]

    def getImage(self, imageName, colorkey=None, orientation=None):
        """
        Returns an image from the cache by key if it exists.  If 
        not, it attempts to load the image from the filesystem.
        If this fails, an "image not found" image is returned
        """
        if orientation == None:
            imageDict = self.cache.get(imageName,None)
            if imageDict == None:
                self.loadImage(imageName,colorkey)              
                imageDict = self.cache.get(imageName,None)
                if imageDict == None:
                    return self.getDefaultImage()
                else:
                    return imageDict.getDefaultImage()
            else:
                return imageDict.getImage()
        else:
            return self.cache.get(imageName,None).getImage(orientation)
        
    def getImageAndRect(self, imageName, orientation=None):
        """
        Returns a tuple of 2 elements from the dictionary by key
        if it exists.
        [0] - a pygame.Surface image
        [1] - the rectangle associated with said Surface
        If not, None is returned.
        """
        image = self.getImage(imageName, orientation)

        if image == None:
            default = self.getDefaultImage()
            return default,default.get_rect()
        else:
            return (image,image.get_rect())
            
    def getAverageColor(self, imageName, colorkey=None):
        return (255,0,0)
        from specialImage import getAverageColor
        if self.isCached(imageName):
            self.imageColorKeys[imageName] = \
                getAverageColor(self.getImage(imageName),colorkey)
        return self.imageColorKeys[imageName]

class AnimationDict():
    
    def __init__(self,default):
        self.data = {}
        self.setDefaultImage(default)
        
    def addImage(self,image,colorkey=None,orientationKey=None):
        if orientationKey == None:
            self.setDefaultImage(image,colorkey)
        else:        
            self.data[orientationKey] = loadImage(image, colorkey)
    
    def setDefaultImage(self,image,colorKey=None):
        self.data[None] = loadImage(image,colorKey)

    def getDefaultImage(self):
        return self.data[None]

    def getImage(self,orientationKey=None):
        """
        Returns an image associated with a status and an orientation.
        If it does not exist, return the default image.
        """
        return self.data.get(orientationKey,self.getDefaultImage())

class Locals:
    #Statuses
    IDLE = 0
    MOVING = 1
    BUILDING = 2
    GATHERING = 3
    ATTACKING = 4
    DEPOSITING=5

    status={IDLE: 'Idle', MOVING: 'Moving', BUILDING:'Building', GATHERING:'Gathering', ATTACKING: 'Attacking', DEPOSITING: 'Depositing Resources'}
    
    #Efficiency
    MOVE=0
    BUILD=1
    GATHER=2
    ATTACK=3
    DEPOSIT=4
