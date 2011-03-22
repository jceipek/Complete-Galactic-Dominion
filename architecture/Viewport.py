import pygame
from Mouse import Mouse

class Viewport(object):  #SHOULD PROBABLY INHERIT FROM DRAWABLE OBJECT
    """
    Acts as a "window" into the world it contains. Includes deadzone dimensions
    so that it can be scrolled with the mouse.
    
    #Attributes:
    #   world = the world the viewport can see
    #   scrollLoc = (x,y) #World coordinates of the corner of the viewport
    #   loc = (x,y) #Corner of the viewport in screen coordinates
    #   size = (width,height) #Dimensions in screen coordinates
    #   mouse = the mouse controlling it
    #   deadZoneRect
    """
    
    def __init__(self,world,scrollLoc,screenPos,size):
        self.world = world
        self.scrollLoc = scrollLoc
        self.loc = screenPos
        self.size = size
        self.rect = pygame.Rect(screenPos,size)
        
        self.initDeadZoneBasedOnSize()
        self.surface = pygame.Surface(size)
        self.surface.set_clip(((0,0),size))
        self.scrollSpeed = [0,0]
        
        self.calcDistance = lambda a,b: (a**2 + b**2)**0.5
        
    def initDeadZoneBasedOnSize(self):
        #CURRENT IMPLEMENTATION IS FAKE
        offset = int(0.3*float(self.size[0]))
        deadZoneSize = (self.size[0]-offset,self.size[1]-offset)
        self.deadZoneRect = pygame.Rect((0, 0), deadZoneSize)
        self.deadZoneRect.center = (self.size[0]/2.0,\
                                    self.size[1]/2.0)

    def setScrollSpeed(self,mousePos):
        deadZoneHeight,deadZoneWidth = self.deadZoneRect.size
        relMousePos = (mousePos[0]-self.loc[0],mousePos[1]-self.loc[1])
        if self.rect.collidepoint(mousePos) and not self.deadZoneRect.collidepoint(relMousePos):
            dx = (mousePos[0]-self.deadZoneRect.center[0]-self.loc[0])
            dy = (mousePos[1]-self.deadZoneRect.center[1]-self.loc[1])
##            mag = self.calcDistance(dx,dy)
##            direction = (dx/mag,dy/mag)
##            speedCoeffX = abs(dx)-deadZoneHeight
##            speedCoeffY = abs(dy)-deadZoneWidth
##    
##            self.scrollSpeed[0]=direction[0]*speedCoeffX*scrollSensitivity
##            self.scrollSpeed[1]=direction[1]*speedCoeffY*scrollSensitivity
            #self.scrollSpeed[0]=dx*self.mouse.scrollSensitivity
            #self.scrollSpeed[1]=dy*self.mouse.scrollSensitivity
            ### FIX TO NOT HAVE MOUSE
            self.scrollSpeed[0]=dx*0.001
            self.scrollSpeed[1]=dy*0.001
            
        else:
            self.scrollSpeed = [0,0]
            
    def scrollBasedOnElapsedTime(self,elapsedTime):
        newScrollLoc = list(self.scrollLoc)
        newScrollLoc[0] += self.scrollSpeed[0]*elapsedTime
        newScrollLoc[1] += self.scrollSpeed[1]*elapsedTime
        self.scrollLoc = tuple(newScrollLoc)

    def scrollBasedOnMousePos(self,mousePos):
        #Add to the scrollLoc if the mouse position in the move event is outside 
        #of the deadZone. Adapt Berit's algorithm from gridTest in internal
        #to deal with scroll distances properly
        #Right now, it always scrolls
        
        ms_elapsed = 1 # THIS SHOULD COME FROM THE GAME LOOP
        
        newScrollLoc = list(self.scrollLoc)
        deadZoneSize = self.deadZoneRect.size
        if self.rect.collidepoint(mousePos):
            dx = (mousePos[0]-self.deadZoneRect.center[0])
            dy = (mousePos[1]-self.deadZoneRect.center[1])
            magnitude=self.calcDistance(dx, dy) #distance from center
            dirx=dx/magnitude #x component of unit direction
            diry=dy/magnitude #y component of unit direction
    
            dx=max([0, abs(dx)-deadZoneSize[0]/2.0])
            dy=max([0, abs(dy)-deadZoneSize[1]/2.0])
    
            speedCoeff=self.calcDistance(dx,dy)/(self.rect.width-deadZoneSize[0])*2.0
            newScrollLoc[0] += dirx*self.scrollSpeed[0]*speedCoeff*ms_elapsed
            newScrollLoc[1] += diry*self.scrollSpeed[1]*speedCoeff*ms_elapsed
            
        self.scrollLoc = tuple(newScrollLoc)
        
    def draw(self,displaySurface):
        
        self.world.grid.draw(self.surface,\
                                  self.scrollLoc,\
                                  self.size)
        self.drawDebugFrames(self.surface)
        displaySurface.blit(self.surface, (self.loc,self.size))
                                  
    def drawDebugFrames(self,displaySurface):                  
        rect = ((0,0),self.size)
        pygame.draw.rect(displaySurface, (255,255,0), rect, 3)
        pygame.draw.rect(displaySurface, (255,0,255), self.deadZoneRect, 2)
    
    def absMousePosition(self):
        """Returns absolute position of mouse in world."""
        relX, relY = pygame.mouse.get_pos()
        return (self.scrollLoc[0]+relX, self.scrollLoc[1]+relY)

if __name__ == "__main__":
	pass
