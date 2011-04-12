import pygame
import Event,specialMath
from GameData import Locals
from Overlay import DragBox, MakeBoundingBox, MiniMap

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
        
        if world is not None:
            self.minimap = MiniMap(self.world)
        else:
            self.minimap = None
        
        #FIXME - SHOULD COME FROM A CONFIG FILE
        self.scrollSensitivity=.001
        
        self.initDeadZoneBasedOnSize()
        self.surface = pygame.Surface(size)
        self.surface.set_clip(((0,0),size))
        self.scrollSpeed = [0,0]
        
        self.selectedEntities = []
        
        self.calcDistance = lambda a,b: (a**2 + b**2)**0.5
        
        self.viewportEntities = []
        
        self.dragRect = None
        
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
    
    def startDrag(self,event):
        self.dragRect = DragBox(event.pos)
        
    def continueDrag(self,event):
        if self.dragRect is not None:
            self.dragRect.update(event.curr)
            if self.dragRect.visible:
                self.drawDragRect()
    
    def completeDrag(self,event):
        if self.dragRect is not None:
            self.dragRect.update(event.curr)
            if self.dragRect.visible:
                self.drawDragRect()
        self.dragSelect(event)
        self.dragRect = None
    
    def drawMiniMap(self):
        if self.minimap is not None:
            self.minimap.update()
            self.minimap.draw(self.surface)
    
    def drawDragRect(self):   
        """
        Draws the drag rectangle from a mouse drag, if not None.
        """
        if not self.dragRect == None:
            self.dragRect.draw(self.surface)
           
    def setDestinationEvent(self, event):
        attacking=False
        pos = event.pos
        cartPos = specialMath.isoToCart(pos)
        
        destCart = self.cartScrollLoc[0] + cartPos[0], \
                    self.cartScrollLoc[1] + cartPos[1]

        clicked = specialMath.closestEntity(self.viewportEntities,pos)
        
        if clicked:
            drawRect = clicked.rect.move(clicked.drawOffset)
            drawRect.center = specialMath.cartToIso(drawRect.center)
        
            if not drawRect.collidepoint(pos):
                clicked = None
        
        if clicked:
            for selected in self.selectedEntities:
                attacking=True
                selected.initAction(clicked)
                       
        if not attacking:
            eCenter = specialMath.centerOfEntityList(self.selectedEntities)
            for entity in self.selectedEntities:
                entity.status=Locals.MOVING
                dx = entity.rect.center[0] - eCenter[0]
                dy = entity.rect.center[1] - eCenter[1]
                newLoc = (dx+destCart[0],dy+destCart[1])
                entity.addToPath(newLoc)
        
    def dragSelect(self,event):
        """
        Fill this in.
        """
        
        start = event.start
        end = event.curr
        
        if isinstance(event,Event.DragCompletedEvent):
            for e in self.selectedEntities:
                e.selected = False
            self.selectedEntities = []
        #else: pass # if it is an Event.AddDragCompletedEvent, do
        # # not deselect
        
        for entity in self.viewportEntities:
        
            drawRect = entity.rect.move(entity.drawOffset)
            drawRect.center = specialMath.cartToIso(drawRect.center)
        
            if drawRect.colliderect(MakeBoundingBox(start,end)):
                entity.selected = True
                self.selectedEntities.append(entity)
    
    def clickEvent(self,event):
        """
        What works:
        single - clicking on units
        click on ground to deselect all (without a modifier)
        click a unit while holding a modifier to add to the selection
        click a selected unit while holding a modifier to remove from the selection
        """
        
        pos = event.pos

        cartPos = specialMath.isoToCart(pos)
        destCart = self.cartScrollLoc[0] + cartPos[0], \
                       self.cartScrollLoc[1] + cartPos[1]
        clicked = specialMath.closestEntity(self.viewportEntities,pos)
        
        if clicked:
            drawRect = clicked.rect.move(clicked.drawOffset)
            drawRect.center = specialMath.cartToIso(drawRect.center)
            
            if not drawRect.collidepoint(pos):
                clicked = None
        
        if isinstance(event,Event.SelectionEvent):
            for e in self.selectedEntities:
                e.selected = False
            self.selectedEntities = []

        if clicked:
            # Determines if the closest entity is already selected.
            # If it is, it makes it no longer selected.
            if clicked.selected:
                clicked.selected = False
                self.selectedEntities.remove(clicked)
            else:
                clicked.selected = True
                self.selectedEntities.append(clicked)
    
    def scrollBasedOnElapsedTime(self,elapsedTime):
        
        if not self.world == None:# FIXME and self.dragRect == None:
            newScrollLoc = list(self.scrollLoc)
            scrollAddX = self.scrollSpeed[0]*elapsedTime
            scrollAddY = self.scrollSpeed[1]*elapsedTime
            if not self.dragRect == None:
                self.dragRect.scroll((scrollAddX,scrollAddY)) 
            newScrollLoc[0] = (newScrollLoc[0]+scrollAddX)
            newScrollLoc[1] = (newScrollLoc[1]+scrollAddY)
            
            # used to calculate corner of scroll location in cartesian grid
            self.cartScrollLoc = self.isoToWrappedCart(newScrollLoc)
            
            newScrollLoc = specialMath.cartToIso(self.cartScrollLoc)
            self.scrollLoc = tuple(newScrollLoc)
    
    def cartWrap(self,cartCoord):
        gridSizeX,gridSizeY = self.world.gridDim
        return cartCoord[0]%gridSizeX,cartCoord[1]%gridSizeY
    
    def isoToWrappedCart(self,isoCoord):
        """
        Returns a wrapped cartesian coordinate from an isometric
        coordinate.
        """
        return self.cartWrap(specialMath.isoToCart(isoCoord))
    
    def drawContainedEntities(self):
        """
        Draws all elements contained in the current viewport to
        self.surface.
        """
        for e in self.viewportEntities:
            e.draw(self.surface,self.scrollLoc)
  
    def draw(self,displaySurface):
        """
        Draws the map and all entities for the current world location.
        displaySurface is provided by the screen.
        """
        if not self.world == None:
            self.world.grid.draw(self.surface, self.scrollLoc, self.size)
            self.drawContainedEntities()
            self.drawDragRect()
            self.drawMiniMap()
            self.drawDebugFrames()
            displaySurface.blit(self.surface, (self.loc,self.size))

    def processUpdateEvent(self,event):
        self.setViewportEntities()
        timeElapsed = event.elapsedTimeSinceLastFrame
        self.scrollBasedOnElapsedTime(timeElapsed)
        self.world.__class__.elapsedTimeSinceLastFrame = timeElapsed
    
    def rectToCartWrappedRects(self,rect):
        isoLeftTop = rect.topleft
        cartLeftTop = self.isoToWrappedCart(isoLeftTop)
        
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

            worldWidth,worldHeight = self.world.grid.getCartGridDimensions()
            screen=[]
            
            #determine which screens to check
            xRange = [0]
            yRange = [0]
            
            if cartBottomLeft[0] >= 0:
                xRange.append(-1)
            if cartTopRight[0] <= worldWidth:
                xRange.append(1)
            
            if cartTopLeft[1] >= 0:
                yRange.append(-1)
            if cartBottomRight[1] <= worldHeight:
                yRange.append(1)
                
            for i in xRange:
                for j in yRange:
                    TL = cartTopLeft[0]+i*worldWidth,cartTopLeft[1]+j*worldHeight
                    TR = cartTopRight[0]+i*worldWidth,cartTopRight[1]+j*worldHeight
                    BR = cartBottomRight[0]+i*worldWidth,cartBottomRight[1]+j*worldHeight
                    BL = cartBottomLeft[0]+i*worldWidth,cartBottomLeft[1]+j*worldHeight
                    
                    screen.append((TL,TR,BR,BL))
            
            self.viewportEntities = self.world.getScreenEntities(screen)
    
    def drawDebugFrames(self):  
        """
        Draws frames on viewport which are useful for debugging.
        Defines the scrolling and non-scrolling regions.
        """
        rect = ((0,0),self.size)
        pygame.draw.rect(self.surface, (255,255,0), rect, 3)
        pygame.draw.rect(self.surface, (255,0,255), self.deadZoneRect, 2)
        
    def changeWorld(self,world):
        self.world = world
        self.minimap = MiniMap(self.world)
