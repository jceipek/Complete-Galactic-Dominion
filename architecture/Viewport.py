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
		
        import pygame
        
        self.world = world
        self.scrollLoc = scrollLoc
        self.loc = screenPos
        self.size = size
        self.rect = pygame.Rect(screenPos,size)
        
        self.mouse = Mouse()
        
        self.initDeadZoneBasedOnSize()
        
    def initDeadZoneBasedOnSize(self):
        #CURRENT IMPLEMENTATION IS FAKE
        import pygame
        offset = int(0.3*float(self.size[0]))
        deadZoneSize = (self.size[0]-offset,self.size[1]-offset)
        self.deadZoneRect = pygame.Rect((0, 0), deadZoneSize)
        self.deadZoneRect.center = (self.size[0]/2.0+self.loc[0],\
                                    self.size[1]/2.0+self.loc[1])
    
    def scrollBasedOnMousePos(self):
        #Add to the scrollLoc if the mouse position in the move event is outside 
        #of the deadZone. Adapt Berit's algorithm from gridTest in internal
        #to deal with scroll distances properly
        #Right now, it always scrolls
        
        mousePos = self.mouse.getCurrentRelMousePos()
        
        ms_elapsed = 1 # THIS SHOULD COME FROM THE GAME LOOP
        scrollSpeed = 1 #SHOULD BE DEFINED IN THE MOUSE OBJECT (when it exists)\
                        #AND PASSED UP VIA EVENTS - Why like this?

        newScrollLoc = list(self.scrollLoc)
        deadZoneSize = self.deadZoneRect.size
        if self.rect.collidepoint(mousePos):
            dx = (mousePos[0]-self.deadZoneRect.center[0])
            dy = (mousePos[1]-self.deadZoneRect.center[1])
            magnitude=pow(dx**2+dy**2,0.5) #distance from center
            dirx=dx/magnitude #x component of unit direction
            diry=dy/magnitude #y component of unit direction
    
            dx=max([0, abs(dx)-deadZoneSize[0]/2.0])
            dy=max([0, abs(dy)-deadZoneSize[1]/2.0])
    
            speedCoeff=pow(dx**2+dy**2,0.5)/(self.rect.width-deadZoneSize[0])*2.0
            newScrollLoc[0] += dirx*scrollSpeed*speedCoeff*ms_elapsed
            newScrollLoc[1] += diry*scrollSpeed*speedCoeff*ms_elapsed
            
        self.scrollLoc = tuple(newScrollLoc)
        
    def draw(self,displaySurface):
        self.world.grid.draw(displaySurface,\
                                  self.scrollLoc,\
                                  self.size,
                                  self.loc)
        self.drawDebugFrames(displaySurface)
                                  
    def drawDebugFrames(self,displaySurface):                  
        import pygame
        rect = (self.loc,self.size)
        pygame.draw.rect(displaySurface, (255,255,0), rect, 3)
        pygame.draw.rect(displaySurface, (255,0,255), self.deadZoneRect, 2)
    
    def absMousePosition:
        """Returns absolute position of mouse in world."""
        relX, relY = self.mouse.getCurrentRelMousePos()
        return (self.loc[0]+relX, self.loc[1]+relY)

if __name__ == "__main__":
	pass
