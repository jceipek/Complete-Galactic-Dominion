import pygame
#from Mouse import Mouse

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
    #   selectedEntities
    """
    
    def __init__(self,world,scrollLoc,screenPos,size):
        self.world = world
        self.scrollLoc = scrollLoc
        self.loc = screenPos
        self.size = size
        self.rect = pygame.Rect(screenPos,size)
        
        #FIXME - SHOULD COME FROM A CONFIG FILE
        self.scrollSensitivity=.001
        
        self.initDeadZoneBasedOnSize()
        self.surface = pygame.Surface(size)
        self.surface.set_clip(((0,0),size))
        self.scrollSpeed = [0,0]
        
        self.selectedEntities = []
        
        self.calcDistance = lambda a,b: (a**2 + b**2)**0.5
        
        self.viewportEntities = []
        
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

            self.scrollSpeed[0]=dx*self.scrollSensitivity
            self.scrollSpeed[1]=dy*self.scrollSensitivity
            
        else:
            self.scrollSpeed = [0,0]
        
    def clickAt(self,pos):
        #FIXME - VERY INEFFICIENT/UGLY IMPLEMENTATION RIGHT NOW
        def distBetween(p1,p2):
            return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**.5
    
        worldX, worldY = self.scrollLoc
        posX = pos[0] + worldX
        posY = pos[1] + worldY
        curScreenRect = pygame.Rect(worldX,worldY,*self.size)
        clicked = []
        for entity in self.viewportEntities:
            if entity.rect.collidepoint((posX,posY)) and not entity.selected:
                entityRectOnScreen=entity.rect.move(posX,posY)
                print entity.rect.center,pos,distBetween(entity.rect.center,pos)
                print entityRectOnScreen.center,pos,distBetween(entityRectOnScreen.center,pos)
                clicked.append((distBetween(entityRectOnScreen.center,pos),entity))
        for e in self.selectedEntities:
            e.selected = False
        if len(clicked):
            clicked.sort(reverse=True)
            clicked[0][1].selected = True
            self.selectedEntities = [clicked[0][1]]
    
    
    def scrollBasedOnElapsedTime(self,elapsedTime):
        newScrollLoc = list(self.scrollLoc)
        newScrollLoc[0] += self.scrollSpeed[0]*elapsedTime
        newScrollLoc[1] += self.scrollSpeed[1]*elapsedTime
        self.scrollLoc = tuple(newScrollLoc)
    
    def drawContainedEntities(self):
        """
        Draws all elements contained in the current viewport to
        self.surface.
        """

        ### FIXME!! Wrapping of objects does not currently work correctly!

        for entity in self.viewportEntities:
            entity.draw(self.surface,self.scrollLoc)
    
    def draw(self,displaySurface):
        """
        Draws the map and all entities for the current world location.
        displaySurface is provided by the screen.
        """
        self.world.grid.draw(self.surface, self.scrollLoc, self.size)
        self.drawContainedEntities()
        self.drawDebugFrames(self.surface)
        displaySurface.blit(self.surface, (self.loc,self.size))
    
    def processUpdateEvent(self,event):
        self.world.update()
        self.setViewportEntities()
        self.scrollBasedOnElapsedTime(event.elapsedTimeSinceLastFrame)
        
    def setViewportEntities(self):
        curScreenRect = pygame.Rect(self.scrollLoc,self.size)
        self.viewportEntities = self.world.getScreenEntities(curScreenRect)
    
    def drawDebugFrames(self,displaySurface):  
        """
        Draws frames on viewport which are useful for debugging.
        Defines the scrolling and non-scrolling regions.
        """
        rect = ((0,0),self.size)
        pygame.draw.rect(displaySurface, (255,255,0), rect, 3)
        pygame.draw.rect(displaySurface, (255,0,255), self.deadZoneRect, 2)
