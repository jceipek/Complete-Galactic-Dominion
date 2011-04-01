import pygame
import Event,specialMath
#from Mouse import Mouse

class Viewport(object):  #SHOULD PROBABLY INHERIT FROM DRAWABLE OBJECT
    """
    Acts as a "window" into the world it contains. Includes deadzone dimensions
    so that it can be scrolled with the mouse.
    
    @param world: the world the viewport can see
    @param scrollLoc: (x,y) #World coordinates of the corner of the viewport
    @param loc: (x,y) #Corner of the viewport in screen coordinates
    @param size: (width,height) #Dimensions in screen coordinates
    @param mouse: the mouse controlling it
    @param deadZoneRect:
    @param selectedEntities:
    @param selector: a selection rectangle that is activated and drawn when necessary #FIXME: NOT YET IMPLEMENTED
    """
    
    def __init__(self,world,scrollLoc,screenPos,size):
        self.world = world
        self.scrollLoc = scrollLoc
        self.cartScrollLoc = specialMath.isoToCart(scrollLoc)
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
        
    def dragEvent(self,event):
        #pass
        startPos = event.startPos
        curPos = event.curPos
        dragRect = BBoxToRect(startPos,curPos)
        dragColor = (150,150,0)
        dragBoxThickness = 3
        pygame.draw.rect(self.screen,dragBoxColor,dragRect,dragBoxThickness)
    
    def clickEvent(self,event):
        """"
        What works:
        single - clicking on units
        click on ground to deselect all (without a modifier)
        click a unit while holding a modifier to add to the selection
        click a selected unit while holding a modifier to remove from the selection
        """
        
        pos = event.pos        
        #FIXME - VERY INEFFICIENT/UGLY IMPLEMENTATION RIGHT NOW
        def distBetween(p1,p2):
            return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**.5
    
        worldX, worldY = self.scrollLoc

        cartOffset = self.world.grid.isoToCart((-worldX,-worldY))
        
        # list of tuples containing distance between the center of the
        # rectangle and the mouseclick position, and the entity itself
        clicked = []
        for entity in self.viewportEntities:
        
            drawRect = entity.rect.move(cartOffset)
            drawRect.center = self.world.grid.cartToIso(drawRect.center)
        
            if drawRect.collidepoint(pos):
                clicked.append((distBetween(drawRect.center,pos),entity))
        
        if isinstance(event,Event.SelectionEvent):
            for e in self.selectedEntities:
                e.selected = False
            self.selectedEntities = []

        if len(clicked):
            clicked.sort()
            # Determines if the closest entity is already selected.
            # If it is, it makes it no longer selected.
            if clicked[0][1].selected:
                clicked[0][1].selected = False
                self.selectedEntities.remove(clicked[0][1])
            else:
                clicked[0][1].selected = True
                self.selectedEntities.append(clicked[0][1])
    
    def scrollBasedOnElapsedTime(self,elapsedTime):
        if not self.world == None:
            newScrollLoc = list(self.scrollLoc)
            newScrollLoc[0] = (newScrollLoc[0]+self.scrollSpeed[0]*elapsedTime)
            newScrollLoc[1] = (newScrollLoc[1]+self.scrollSpeed[1]*elapsedTime)
            
            #FIXME - used to calculate corner of scroll location in cartesian grid
            newCartScrollLoc = self.world.grid.isoToCart(newScrollLoc)
            gridSizeX,gridSizeY = self.world.gridDim
            self.cartScrollLoc = newCartScrollLoc[0]%gridSizeX,newCartScrollLoc[1]%gridSizeY
            
            newScrollLoc = specialMath.cartToIso(self.cartScrollLoc)
            
            self.scrollLoc = tuple(newScrollLoc)
    
    def drawContainedEntities(self):
        """
        Draws all elements contained in the current viewport to
        self.surface.
        """
        worldWidth,worldHeight = self.world.grid.getGridDimensions()
        ### FIXME!! Wrapping of objects does not currently work correctly!
        sL=self.scrollLoc
        for i in range(-1,2):
            for j in range(-1,2):
                for entity in self.viewportEntities:
                    s1=(sL[0]+i*worldWidth,sL[1]+j*worldHeight)
                    entity.draw(self.surface,s1)
    
    def draw(self,displaySurface):
        """
        Draws the map and all entities for the current world location.
        displaySurface is provided by the screen.
        """
        if not self.world == None:
            self.world.grid.draw(self.surface, self.scrollLoc, self.size)
            self.drawContainedEntities()
            self.drawDebugFrames(self.surface)
            displaySurface.blit(self.surface, (self.loc,self.size))
    
    def processDragSelectionEvent(self,event):
        pass
    
    def processUpdateEvent(self,event):
        self.setViewportEntities()
        self.scrollBasedOnElapsedTime(event.elapsedTimeSinceLastFrame)
        
    def setViewportEntities(self):
        if not self.world == None:
            """FIXME to work with new coordinates."""
            l,t = self.cartScrollLoc
            w,h = self.size
            cartWidthVector=specialMath.isoToCart((w,0))
            cartHeightVector=specialMath.isoToCart((0,h))
            cartTopLeft=l,t
            cartTopRight=l+cartWidthVector[0],t+cartWidthVector[1]
            cartBottomRight=l+cartWidthVector[0]+cartHeightVector[0],t+cartWidthVector[1]+cartHeightVector[1]
            cartBottomLeft=l+cartHeightVector[0],t+cartHeightVector[1]
            print 'TL: ',cartTopLeft
            print 'TR: ',cartTopRight
            print 'BR: ',cartBottomRight
            print 'BL: ',cartBottomLeft
            '''
            r=l+t
            b=t+h
            
            cartTopLeft = (l,t)
            cartTopRight = (r,t)
            cartBottomRight = (r,b)
            cartBottomLeft = (l,b)
            '''
            '''
            isoTopLeft = specialMath.cartToIso((l,t))
            isoTopRight = specialMath.cartToIso((r,t))
            isoBottomRight = specialMath.cartToIso((r,b))
            isoBottomLeft = specialMath.cartToIso((l,b))
            '''
            '''
            cartW = cartTopRight[0]-cartBottomLeft[0]
            cartH = cartBottomRight[1]-cartTopLeft[1]
            cartL = cartBottomLeft[0]
            cartT = cartTopLeft[1]
            
            curScreenRect = pygame.Rect(cartL,cartT,cartW,cartH)
            #curScreenRect = pygame.Rect(self.scrollLoc,self.size)
            
            self.viewportEntities = self.world.getScreenEntities(curScreenRect)
            '''
            worldWidth,worldHeight = self.world.grid.getGridCartDimensions()
            screen=[]
            for i in range(-1,2):
                for j in range(-1,2):
                    TL = cartTopLeft[0]+i*worldWidth,cartTopLeft[1]+j*worldHeight
                    TR = cartTopRight[0]+i*worldWidth,cartTopRight[1]+j*worldHeight
                    BR = cartBottomLeft[0]+i*worldWidth,cartBottomLeft[1]+j*worldHeight
                    BL = cartBottomRight[0]+i*worldWidth,cartBottomRight[1]+j*worldHeight
                    
                    screen.append((TL,TR,BR,BL))
                    #print (TL,TR,BR,BL)
                    
            #print screen
            
            self.viewportEntities = self.world.getScreenEntities(screen)
    
    def drawDebugFrames(self,displaySurface):  
        """
        Draws frames on viewport which are useful for debugging.
        Defines the scrolling and non-scrolling regions.
        """
        rect = ((0,0),self.size)
        pygame.draw.rect(displaySurface, (255,255,0), rect, 3)
        pygame.draw.rect(displaySurface, (255,0,255), self.deadZoneRect, 2)
        
        if not self.world == None:
            """FIXME to work with new coordinates."""
            l,t = self.cartScrollLoc
            w,h = self.size
            cartWidthVector=specialMath.isoToCart((w,0))
            cartHeightVector=specialMath.isoToCart((0,h))
            cartTopLeft=l,t
            cartTopRight=l+cartWidthVector[0],t+cartWidthVector[1]
            cartBottomRight=l+cartWidthVector[0]+cartHeightVector[0],t+cartWidthVector[1]+cartHeightVector[1]
            cartBottomLeft=l+cartHeightVector[0],t+cartHeightVector[1]
            print 'TL: ',cartTopLeft
            print 'TR: ',cartTopRight
            print 'BR: ',cartBottomRight
            print 'BL: ',cartBottomLeft
            '''
            r=l+t
            b=t+h
            
            cartTopLeft = (l,t)
            cartTopRight = (r,t)
            cartBottomRight = (r,b)
            cartBottomLeft = (l,b)
            '''
            '''
            isoTopLeft = specialMath.cartToIso((l,t))
            isoTopRight = specialMath.cartToIso((r,t))
            isoBottomRight = specialMath.cartToIso((r,b))
            isoBottomLeft = specialMath.cartToIso((l,b))
            '''
            '''
            cartW = cartTopRight[0]-cartBottomLeft[0]
            cartH = cartBottomRight[1]-cartTopLeft[1]
            cartL = cartBottomLeft[0]
            cartT = cartTopLeft[1]
            
            curScreenRect = pygame.Rect(cartL,cartT,cartW,cartH)
            #curScreenRect = pygame.Rect(self.scrollLoc,self.size)
            
            self.viewportEntities = self.world.getScreenEntities(curScreenRect)
            '''
            worldWidth,worldHeight = self.world.grid.getGridCartDimensions()
            screen=[]
            for i in range(1):
                for j in range(1):
                    TL = cartTopLeft[0]+i*worldWidth,cartTopLeft[1]+j*worldHeight
                    TR = cartTopRight[0]+i*worldWidth,cartTopRight[1]+j*worldHeight
                    BR = cartBottomLeft[0]+i*worldWidth,cartBottomLeft[1]+j*worldHeight
                    BL = cartBottomRight[0]+i*worldWidth,cartBottomRight[1]+j*worldHeight
                    
                    pygame.draw.polygon(displaySurface,(255,0,0),[specialMath.cartToIso(TL),specialMath.cartToIso(TR),specialMath.cartToIso(BL),specialMath.cartToIso(BR)],2)
        
    def changeWorld(self,world):
        self.world = world

def BBoxToRect(p1,p2):
    """
    Takes two screen positions and returns the bounding box as a 
    pygame.Rect object.
    """
    x1,y1 = p1
    x2,y2 = p2
    bboxRect = (pygame.Rect(p1,(x2-x1,y2-y1)))
    bboxRect.normalize() # Normalizes to remove negative sizes.
    return bboxRect
