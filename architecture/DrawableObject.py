#import useful modules here
#import pygame
import pygame.display
from GameData import loadImage, ImageBank

class DrawableObject(object):
    """This is the super class of all object that can be drawn to the screen"""
    
    imageBank = ImageBank()
    
    def __init__(self, imagePath, colorkey=None, blendPath=None, 
        owner='blarg'):
            
        self.isImageInitialized = False
        # First class to have image and rect objects
        self.imagePath = imagePath
        self.blendPath = blendPath
        self.colorkey = colorkey
        
        self.owner=owner
        self.orientation=0
        '''
        self.loadImage(imagePath,colorkey)
        self.setAverageColor(imagePath,colorkey)
        self.realCenter = self.rect.center
        '''

        self._imageInformationSetup()
        
    def _imageInformationSetup(self):
        if pygame.display.get_init():
            self.loadDefaultImage(self.imagePath,self.colorkey)
            self.setAverageColor(self.imagePath,self.colorkey)
            self.realCenter = self.rect.center
            self.isImageInitialized = True
    
    # First loadImage method
    def loadDefaultImage(self, imagePath, colorkey=None):

        objImage = self.imageBank.getImage(imagePath,colorkey,self.orientation,playerID=self.owner,blendPath=self.blendPath)

        self.image = objImage
        self.rect = self.image.get_rect()
        
    def setImageToOrientation(self,orientation):

        objImage = self.imageBank.getImage(self.imagePath,self.colorkey,orientation,playerID=self.owner)
        self.image = objImage

    def setAverageColor(self,imagePath,colorkey=None):
        """
        Sets the averageColor attribute of something with an image.
        """
        self.averageColor = self.imageBank.getAverageColor(imagePath,colorkey,playerID=self.owner)
        
    def getMiniMapColor(self):
        """
        By default, returns the average color.  Override.
        """
        return self.getAverageColor()

    def getAverageColor(self):
        """
        Returns the average color of the image.
        """
        return self.averageColor
        
    def draw(self,screen):
        """
        Blits the image onto the location of the rect on the given screen.
        """
        if self.isImageInitialized:
            screen.blit(self.image,self.rect)
        else:
            self._imageInformationSetup()

class DrawableObjectGroup(DrawableObject):
    
    def __init__(self,imageList,pos=(0,0)):
        #imageList is a list of tuples and values that indicate
        #image paths and colorkeys
        self.pos = pos
        self.drawableObjectList = []
        self.addObjectsFromImageList(imageList)
    
        self._imageInformationSetup()
        
    def _imageInformationSetup(self):
        if pygame.display.get_init():
            for drawableObjectTuple in self.drawableObjectList:
                drawableObject = drawableObjectTuple[0]
                drawableObject.loadDefaultImage(drawableObject.imagePath,drawableObject.colorkey)
                drawableObject.setAverageColor(drawableObject.imagePath,drawableObject.colorkey)
                drawableObject.realCenter = drawableObject.rect.center
                drawableObject.isImageInitialized = True
    
    def addObjectsFromImageList(self,aList):
        #aList is a list of tuples and values with the format:
        #       (imagePath, [colorKey, [offset]])
        
        for t in aList:
            
            if not isinstance(t,tuple):
                #Handle case where there is a single value, not a tuple
                self.drawableObjectList.append((DrawableObject(t,None),(0,0)))
            elif len(t) == 3:
                self.drawableObjectList.append((DrawableObject(t[0],t[1]),t[2]))
            elif len(t) == 2:
                self.drawableObjectList.append((DrawableObject(t[0],t[1]),(0,0)))
            elif len(t) == 1:
                self.drawableObjectList.append((DrawableObject(t[0],None),(0,0)))

    def draw(self,screen):
        
        for drawableObjectTuple in self.drawableObjectList:
            drawableObject = drawableObjectTuple[0]
            offset = drawableObjectTuple[1]
            if drawableObject.isImageInitialized:
                screen.blit(drawableObject.image,drawableObject.rect.move(*self.pos).move(*offset))
            else:
                self._imageInformationSetup()
                
    def move(self,x,y):
        self.pos[0] += x
        self.pos[1] += y

    def setPos(self,x,y):
        self.pos[0] = x
        self.pos[1] = y

if __name__ == "__main__":
    screenSize = (width, height) = (1024, 768)
    screenLoc = [0.0, 0.0]

    RUNNING = True
    pygame.init()
    screen = pygame.display.set_mode(screenSize)
    screenZone = screen.get_rect()
    
    screen.fill((100,100,100))
    
    from specialImage import loadImage
    
    a = DrawableObject('ship','alpha',blendPath='ShipFlags')
    #mask = loadImage('ShipFlags',(0,0,0))

    #a = DrawableObject('TownCenterGeneric.png','alpha')
    #mask = loadImage('imageData/TownCenterFlag.png',(0,0,0))
    
    def imageBlend(image,mask,color=None):
        if color==None:
            color = (255,0,255)
        rect = image.get_rect()
        maskBackground = pygame.Surface(rect.size)
        maskBackground.fill(color)
        maskBackground.blit(mask,rect,special_flags=pygame.BLEND_MULT)
        image.blit(maskBackground,rect,special_flags=pygame.BLEND_ADD)
        return image
    '''
    # GOOD
    tstSurface = pygame.Surface(a.rect.size)
    tstSurface.fill((255,255,0))
    tstSurface.blit(mask,a.rect,special_flags=pygame.BLEND_MULT)
    a.image.blit(tstSurface,a.rect,special_flags=pygame.BLEND_ADD)
    '''

    #minimalRect=DrawableObject.imageBank.getMinimalRect('ship/ship_0000.png','alpha',padding=30)
    #minimalRect.clamp_ip(a.rect)
    
    #a.image = imageBlend(a.image,mask,(255,0,0))
    
    pygame.init()

    while RUNNING:

        #screen.blit(a.image,a.rect)
        screen.blit(a.image,a.rect)

        #pygame.draw.rect(screen,(255,0,255),minimalRect,2)
        pygame.display.flip()
