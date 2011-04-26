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
        Loads an image or animation into the cache as an AnimationDict.
        Accepts an imagePath as a file or directory, and a blendPath as
        a file, directory, or None.  The blendPath should be of the same
        type as imagePath (or None).  The blendPath folder should contain
        flags/masks which match images in the imagePath folder (or match
        the individual file if an individual filepath is given.  The given
        colorkey is used to load the image.  The playerID matches
        an image to a player, and provides a blending with the mask 
        specified by blendPath to the image.
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
                if isdir(blendPathFull): # directory
                    blendImages = listdir(blendPathFull)
                    blendImages.sort() # sort by order
                else: # str? - indicating an individual filepath
                    blendPathFull = 'imageData'
                    blendImages = join(blendPathFull,blendPath)
                blending = True
                from specialImage import idToColorHash, imageBlend
                blendColor = idToColorHash(playerID)
            else: # None - No blending
                blendImages = None
                blending = False
            
            try:
                #Is this an anim, not a simple image?
                if isdir(imagePathFull):
                    
                    images = listdir(imagePathFull)
                    
                    # Warn if number of flags is not the same as the number
                    # of images
                    if blendImages is not None and len(images) != len(blendImages):
                        raise ValueError, 'Length of images does not match length of blend images.'
                    
                    images.sort() # sort images
                    # set default image of a new animation dictionary
                    animDict = AnimationDict(self.getDefaultImage())
                    
                    for imageI in xrange(len(images)):
                        currentImagePath = join(imagePathFull,images[imageI])
                        image = loadImage(currentImagePath, colorkey)
                        
                        # Handles blending on the image
                        if blending:
                            currentBlendPath = join(blendPathFull,blendImages[imageI])
                            mask = loadImage(currentBlendPath,(0,0,0))
                            image = imageBlend(image,mask,blendColor)
                        
                        # Adds the image to the animation dictionary
                        # imageI -> orientation, playerID -> playerID
                        animDict.addImage(image,colorkey,imageI,playerID)
                        
                        # sets first image to the default
                        if imageI == 0:
                            animDict.setDefaultImage(animDict.getImage(imageI,playerID))
                else:
                    
                    # Makes sure that blendImages is a path like imagePathFull
                    if blendImages is not None and not isinstance(blendImages,str):
                        raise ValueError, 'Length of images does not match length of blend images.'
                    
                    animDict = AnimationDict(self.getDefaultImage())
                    
                    image = loadImage(imagePathFull, colorkey) 
                    if blending:
                        mask = loadImage(blendImages,(0,0,0))
                        image = imageBlend(image,mask,blendColor)
                    
                    animDict.addImage(image,colorkey)
                    
                # cache the animation dictionary result
                self.cache[imagePath] = animDict
                
            except:
                import traceback
                traceback.print_exc()
                
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

        imageDict = self.cache.get(imageName,None)
        if imageDict == None:
            self.loadImage(imageName,colorkey,playerID,blendPath)
            imageDict = self.cache.get(imageName,None)
            if imageDict == None:
                return self.getDefaultImage()
            else:
                return imageDict.getImage(orientation,playerID)#imageDict.getDefaultImage()
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
            
    def getAverageColor(self, imageName, colorkey=None, orientation=None, playerID=None):

        from specialImage import getAverageColor
        if self.isCached(imageName):
            if not (imageName,orientation,playerID) in self.averageColorCache:
                self.averageColorCache[(imageName,orientation,playerID)] = \
                    getAverageColor(self.getImage(imageName,colorkey,orientation,playerID=playerID),
                        colorkey)
            return self.averageColorCache[(imageName,orientation,playerID)]
        return (255,0,0) # default color
        
    def getMinimalRect(self, imageName, colorkey=None, orientation=None, playerID=None, **kwargs):
        
        from specialImage import getMinimalRect
        from copy import copy
        
        if self.isCached(imageName):
            
            if not (imageName,orientation) in self.minimalRectCache:

                self.minimalRectCache[(imageName,orientation)] = \
                    getMinimalRect(self.getImage(imageName,colorkey,orientation,playerID),
                        colorkey, **kwargs)

        return copy(self.minimalRectCache[(imageName,orientation)])

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
