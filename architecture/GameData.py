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

        # Cache for images
        self.cache = {}
        self.setImageNotFound()
        
        self.averageColorCache = {}
        self.minimalRectCache = {}
        
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
    
    def loadImage(self, imagePath, colorkey, playerID=None, blendPath=None):
        """
        Loads an image or animation into the cache as an AnimationDict
        """
        if isinstance(imagePath,str) and not self.isCached(imagePath):
            from os import listdir
            from os.path import isdir,join
            imagePathFull = join('imageData',imagePath)
            
            # Sets the blending bool and blendImages
            # Proven to accept directories.  Not sure if it will
            # work with non-directories yet.  Works with None.
            if blendPath is not None:
                blendPathFull = join('imageData',str(blendPath))
                if isdir(blendPathFull):
                    blendImages = listdir(blendPathFull)
                    blendImages.sort()
                else: # str?
                    blendPathFull = 'imageData'
                    blendImages = join(blendPathFull,blendPath)
                blending = True
                from specialImage import idToColorHash, imageBlend
                blendColor = idToColorHash(playerID)
            else: # None
                blendImages = None
                blending = False
            
            try:
                #Is this an anim, not a simple image?
                if isdir(imagePathFull):
                    images = listdir(imagePathFull)
                    
                    if blendImages is not None and len(images) != len(blendImages):
                        print 'PROBLEM WITH LENGTH OF BLEND + IMAGES'
                    
                    images.sort()
                    animDict = AnimationDict(self.getDefaultImage())
                    
                    for imageI in xrange(len(images)):
                        image = join(imagePathFull,images[imageI])
                        image = loadImage(image, colorkey)
                        
                        # Handles blending.
                        if blending:
                            blendPath = join(blendPathFull,blendImages[imageI])
                            mask = loadImage(blendPath,(0,0,0))
                            image = imageBlend(image,mask,blendColor)
                            
                        animDict.addImage(image,colorkey,imageI,playerID)
                        if imageI == 0:
                            animDict.setDefaultImage(animDict.getImage(imageI))
                else:
                    if blendImages is not None and len(blendImages) != 1:
                        print 'PROBLEM WITH LENGTH OF BLEND + IMAGES'
                    
                    animDict = AnimationDict(self.getDefaultImage())
                    
                    image = loadImage(imagePathFull, colorkey) 
                    if blending:
                        mask = loadImage(blendImages,(0,0,0))
                        image = imageBlend(image,mask,blendColor)
                    
                    animDict.addImage(image,colorkey)
                self.cache[imagePath] = animDict
            except:
                animDict = AnimationDict(self.getDefaultImage())
                animDict.addImage(self.getDefaultImage())
                print("UNABLE TO LOAD '"+imagePath+"'")

    def getDefaultImage(self):
        return self.cache[None]

    def getImage(self, imageName, colorkey=None, orientation=None, playerID=None, blendPath=None):
        """
        Returns an image from the cache by key if it exists.  If 
        not, it attempts to load the image from the filesystem.
        If this fails, an "image not found" image is returned
        """
        
        #print imageName,orientation,playerID,blendPath
        #return self.cache.get(imageName,None).getImage((orientation,playerID))
        imageDict = self.cache.get(imageName,None)
        if imageDict == None:
            self.loadImage(imageName,colorkey,playerID=playerID,blendPath=blendPath)
            imageDict = self.cache.get(imageName,None)
            if imageDict == None:
                return self.getDefaultImage(playerID)
            else:
                return imageDict.getDefaultImage(playerID)
        else:
            return imageDict.getImage(orientation,playerID)
        
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
            
    def getAverageColor(self, imageName, colorkey=None, orientation=None):

        from specialImage import getAverageColor
        if self.isCached(imageName):
            if not (imageName,orientation) in self.averageColorCache:
                self.averageColorCache[(imageName,orientation)] = \
                    getAverageColor(self.getImage(imageName,colorkey,orientation),
                        colorkey)
            return self.averageColorCache[(imageName,orientation)]
        return (255,0,0) # default color
        
    def getMinimalRect(self, imageName, colorkey=None, orientation=None, **kwargs):
        
        from specialImage import getMinimalRect
        if self.isCached(imageName):
            if not (imageName,orientation) in self.minimalRectCache:
                self.minimalRectCache[(imageName,orientation)] = \
                    getMinimalRect(self.getImage(imageName,colorkey,orientation),
                        colorkey, **kwargs)
            from copy import copy
            return copy(self.minimalRectCache[(imageName,orientation)])
        return self.getImage(imageName, orientation).get_rect()

class AnimationDict():
    
    def __init__(self,default):
        self.data = {}
        self.setDefaultImage(default)
        
    def addImage(self,image,colorkey=None,orientationKey=None,playerID=None):
        if orientationKey == None:
            self.setDefaultImage(image,colorkey,playerID)
        else:        
            self.data[(orientationKey,playerID)] = loadImage(image, colorkey)
    
    def setDefaultImage(self,image,colorKey=None,playerID=None):
        self.data[(None,playerID)] = loadImage(image,colorKey)

    def getDefaultImage(self,playerID=None):
        return self.data[(None,playerID)]

    def getImage(self,orientationKey=None,playerID=None):
        """
        Returns an image associated with a status and an orientation.
        If it does not exist, return the default image.
        """
        return self.data.get((orientationKey,playerID),self.getDefaultImage())

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
