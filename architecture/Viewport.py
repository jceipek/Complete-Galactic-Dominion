import pygame
import Event,specialMath
from Unit import Unit
from Structure import Structure,TestTownCenter
from GameData import Locals
from Overlay import DragBox, MakeBoundingBox, MiniMap
from HUD import HUD

from Callback import Callback
from ContextualMenu import WayPoint

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
    
    @param clientID: identifying string or number given by the server
    when a client is created
    """
    
    def __init__(self,world,manager,scrollLoc,screenPos,size,clientID):
        self.world = world
        self.manager = manager
        self.scrollLoc = scrollLoc
        self.cartScrollLoc = specialMath.isoToCart(scrollLoc)
        self.loc = screenPos
        self.size = size
        self.rect = pygame.Rect(screenPos,size)
        self.hud=None
        self.clientID = clientID
        
        if world is not None:
            self.minimap = MiniMap(self.world)
            self.worldSize=self.world.grid.getCartGridDimensions()
        else:
            self.minimap = None
        
        #FIXME - SHOULD COME FROM A CONFIG FILE
        self.scrollSensitivity=.001
        
        self.initDeadZoneBasedOnSize()
        self.surface = pygame.Surface(size)
        self.surface.set_clip(((0,0),size))
        self.scrollSpeed = [0,0]

        self.selectedEntities = []
        
        #self.calcDistance = lambda a,b: (a**2 + b**2)**0.5
        
        self.viewportEntities = []
        self.myViewportEntities = []
        
        self.quickSelect = {}
        for i in xrange(pygame.K_0,pygame.K_9+1):
            self.quickSelect[i] = pygame.sprite.Group()
        
        self.dragRect = None
        
        self.currentMenu = None
        
        from ContextualMenu import getCGDcontextualMenu
        self.contextualMenu = getCGDcontextualMenu()
    
    def setClientID(self,clientID):
        self.clientID = clientID
    
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
        if self.rect.collidepoint(mousePos) and \
            not self.deadZoneRect.collidepoint(relMousePos) and \
            not self.minimap.hasFocus(mousePos):
            dx = (mousePos[0]-self.deadZoneRect.center[0]-self.loc[0])
            dy = (mousePos[1]-self.deadZoneRect.center[1]-self.loc[1])

            self.scrollSpeed[0]=dx*self.scrollSensitivity
            self.scrollSpeed[1]=dy*self.scrollSensitivity
        else:
            self.scrollSpeed = [0,0]
    
    def initiateActionEvent(self,event):
        pos = event.pos
        
        if self.minimap.rect.collidepoint(pos):
            mapClickPoint = self.minimap.clickToGridPos(pos)
            if mapClickPoint is not None:
                return 
            else:            
                cartPos = specialMath.isoToCart(pos)
                destCart = self.cartScrollLoc[0] + cartPos[0], \
                            self.cartScrollLoc[1] + cartPos[1]
        else:
            cartPos = specialMath.isoToCart(pos)
            destCart = self.cartScrollLoc[0] + cartPos[0], \
                        self.cartScrollLoc[1] + cartPos[1]
        
        clicked = specialMath.closestEntity(self.viewportEntities,pos)
        
        if clicked:
            drawRect = clicked.rect.move(clicked.drawOffset)
            drawRect.center = specialMath.cartToIso(drawRect.center)
        
            if not drawRect.collidepoint(pos):
                clicked = None
        
        if clicked is not None:
            self.currentMenu = self.contextualMenu.getMenu(self.selectedEntities,clicked)
        else:
            self.currentMenu = self.contextualMenu.getMenu(self.selectedEntities,WayPoint(*destCart))
            
        if self.currentMenu is not None:
            self.currentMenu.open(event.pos)
        
    def completeActionEvent(self,event):
        attacking = False
        pos = event.pos
        
        # Performs action indicated by menu if menu is visible
        # and exists.  Otherwise, the menu reference is destroyed.
        if self.currentMenu is not None and self.currentMenu.visible:
            self.selectMenu(pos)
            return # Do not do anything else if the menu is selected
        else:
            self.currentMenu = None
        
        # Sets destination in cartesian coordinates
        # Handles minimap clicks
        if self.minimap.rect.collidepoint(pos):
            mapClickPoint = self.minimap.clickToGridPos(pos)
            if mapClickPoint is not None:
                destCart = mapClickPoint
            else:
                cartPos = specialMath.isoToCart(pos)
                destCart = (self.cartScrollLoc[0] + cartPos[0])%self.worldSize[0], \
                            (self.cartScrollLoc[1] + cartPos[1])%self.worldSize[1]
        else:
            cartPos = specialMath.isoToCart(pos)
            destCart = (self.cartScrollLoc[0] + cartPos[0])%self.worldSize[0], \
                        (self.cartScrollLoc[1] + cartPos[1])%self.worldSize[1]
        
        # Determines closest entity to a click
        clicked = specialMath.closestEntity(self.viewportEntities,pos)
        
        if clicked:
            drawRect = clicked.rect.move(clicked.drawOffset)
            drawRect.center = specialMath.cartToIso(drawRect.center)
        
            if not drawRect.collidepoint(pos):
                clicked = None
        
        # clicked is now either None or the closest Entity to the click
        if clicked:
            for selected in self.selectedEntities:
                attacking=True
                if isinstance(selected,Unit):
                    selected.initAction(clicked)
       
        if not attacking:
            eCenter = specialMath.centerOfEntityList(self.selectedEntities, self.worldSize)
            for entity in self.selectedEntities:
                if not entity.status==Locals.MOVING:
                    entity.dest=entity.realCenter
                if entity.movable: entity.status=Locals.MOVING
                dx = entity.rect.center[0] - eCenter[0]
                dy = entity.rect.center[1] - eCenter[1]
                newLoc = (dx+destCart[0],dy+destCart[1])
                entity.addToPath(newLoc)
  
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
            self.minimap.update(self.cartPointTupleOfScreen())
            self.minimap.draw(self.surface)
    
    def drawDragRect(self):   
        """
        Draws the drag rectangle from a mouse drag, if not None.
        """
        if not self.dragRect == None:
            self.dragRect.draw(self.surface)
    
    def dragSelect(self,event):
        """
        Fill this in.
        """
        if self.dragRect is not None:
            start = event.start
            end = event.curr
            
            if isinstance(event,Event.DragCompletedEvent):
                for e in self.selectedEntities:
                    e.deselect()
                self.selectedEntities = []
            #else: pass # if it is an Event.AddDragCompletedEvent, do
            # # not deselect
            
            #if self.dragRect.isOffScreen(self.size):
            #    searchList = self.world.allEntities.values()
            #else:
            #    searchList = self.viewportEntities
            searchList = self.myViewportEntities
            
            for entity in searchList:
            
                drawRect = entity.rect.move(entity.drawOffset)
                drawRect.center = specialMath.cartToIso(drawRect.center)
                
                selectRect=entity.getSelectionRect(drawRect)
            
                if selectRect.colliderect(MakeBoundingBox(start,end)):

                    if isinstance(event,Event.DragCompletedEvent):
                        entity.select()
                        self.selectedEntities.append(entity)
                    else: # Add drag completed event
                        if entity not in self.selectedEntities:
                            entity.select()
                            self.selectedEntities.append(entity)
    
    def ownsEntity(self,entity):
        """
        Returns boolean indicating whether or not this client owns the
        provided entity.
        """
        return self.clientID == entity.owner
    
    def clickEvent(self,event):
        """
        What works:
        single - clicking on units
        click on ground to deselect all (without a modifier)
        click a unit while holding a modifier to add to the selection
        click a selected unit while holding a modifier to remove from the selection
        """
        
        pos = event.pos
        
        if self.minimap.rect.collidepoint(pos):
            mapClickPoint = self.minimap.clickToGridPos(pos)
            if mapClickPoint is not None:
                self._setCartScrollLocation(mapClickPoint)
                return
        cartPos = specialMath.isoToCart(pos)
        destCart = (self.cartScrollLoc[0] + cartPos[0])/self.worldSize[0], \
                       (self.cartScrollLoc[1] + cartPos[1])/self.worldSize[1]
        
        # MAY BREAK THINGS - CHECK
        #clicked = specialMath.closestEntity(self.viewportEntities,pos)
        clicked = specialMath.closestEntity(self.myViewportEntities,pos)
        
        if clicked:
            drawRect = clicked.rect.move(clicked.drawOffset)
            drawRect.center = specialMath.cartToIso(drawRect.center)
            
            selectRect=clicked.getSelectionRect(drawRect)
            
            if not selectRect.collidepoint(pos):
                clicked = None
        
        if isinstance(event,Event.SelectionEvent):
            for e in self.selectedEntities:
                e.deselect()
            self.selectedEntities = []

        if clicked and self.ownsEntity(clicked):
            # Determines if the closest entity is already selected.
            # If it is, it makes it no longer selected.
            if clicked.selected:
                clicked.deselect()
                self.selectedEntities.remove(clicked)
            else:
                clicked.select()
                self.selectedEntities.append(clicked)
                #print clicked.healthStr()
                #if isinstance(clicked, Unit): print '\n' + str(clicked.inventory)
    
    def updateMenu(self,eventPos):
        if self.currentMenu is not None:
            self.currentMenu.update(eventPos)
    
    def selectMenu(self,eventPos):
        if self.currentMenu is not None:
            self.currentMenu.select(eventPos)
        self.currentMenu = None
    
    def drawMenu(self):
        if self.currentMenu is not None:
            self.currentMenu.draw(self.surface)
    
    def mouseMoved(self,event):
        self.setScrollSpeed(event.pos)
        self.updateMenu(event.pos)
    
    def _setCartScrollLocation(self,newCartLoc):
        self.cartScrollLoc = tuple(newCartLoc)
        self.scrollLoc = specialMath.cartToIso(self.cartScrollLoc)
    
    def scrollBasedOnElapsedTime(self,elapsedTime):
        
        if not self.world == None and self.currentMenu == None:# FIXME and self.dragRect == None:
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
  
    def setFocusedEntities(self):
        rawMouseLoc = pygame.mouse.get_pos()
        viewportMouseLoc = rawMouseLoc[0]-self.loc[0],rawMouseLoc[1]-self.loc[1]
        
        for e in self.viewportEntities:
            
            drawRect = e.rect.move(e.drawOffset)
            drawRect.center = specialMath.cartToIso(drawRect.center)
            
            selectRect = e.getSelectionRect(drawRect)
            
            if selectRect.collidepoint(viewportMouseLoc):
                e.focused = True
  
    def draw(self,displaySurface):
        """
        Draws the map and all entities for the current world location.
        displaySurface is provided by the screen.
        """

        if not self.world == None:
            
            self.setFocusedEntities()
            self.world.grid.draw(self.surface, self.scrollLoc, self.size)
            self.drawContainedEntities()
            self.drawDragRect()
            self.drawMiniMap()
            self.drawDebugFrames()
            self.drawMenu()
            displaySurface.blit(self.surface, (self.loc,self.size))

    def processUpdateEvent(self,event):
        self.setViewportEntities()
        self.postNotification()
        timeElapsed = event.elapsedTimeSinceLastFrame
        
        # FIXME - NOT EFFICIENT
        for entity in self.world.getDeadEntities():
            if entity in self.selectedEntities:
                try:
                    self.selectedEntities.remove(entity)
                except ValueError: # thrown if entity not in selectedEntity list
                    pass
        
        if self.currentMenu is not None and not self.currentMenu.visible:
            self.currentMenu._delayedOpen(timeElapsed)
        
        self.scrollBasedOnElapsedTime(timeElapsed)
        self.world.elapsedTimeSinceLastFrame = timeElapsed
    
    def rectToCartWrappedRects(self,rect):
        isoLeftTop = rect.topleft
        cartLeftTop = self.isoToWrappedCart(isoLeftTop)
    
    def cartPointTupleOfScreen(self):
        """
        Returns a tuple of the Cartesian points of the current view
        into the world.  Order: topleft,topright,bottomright,bottomleft
        """
        l,t = self.cartScrollLoc
            
        w,h = self.size
        cartWidthVector=specialMath.isoToCart((w,0))
        cartHeightVector=specialMath.isoToCart((0,h))
        
        cartTopLeft=l,t
        cartTopRight=l+cartWidthVector[0],t+cartWidthVector[1]
        cartBottomRight=l+cartWidthVector[0]+cartHeightVector[0],t+cartWidthVector[1]+cartHeightVector[1]
        cartBottomLeft=l+cartHeightVector[0],t+cartHeightVector[1]
        
        return cartTopLeft,cartTopRight,cartBottomRight,cartBottomLeft
        
    def setViewportEntities(self):
        if not self.world == None:
            """FIXME to work with new coordinates."""
            
            cartTopLeft,cartTopRight,cartBottomRight,cartBottomLeft = \
                self.cartPointTupleOfScreen()
            
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
            
            self.myViewportEntities = []
            for entity in self.viewportEntities:
                if self.ownsEntity(entity):
                    self.myViewportEntities.append(entity)
    
    def drawDebugFrames(self):  
        """
        Draws frames on viewport which are useful for debugging.
        Defines the scrolling and non-scrolling regions.
        """
        rect = ((0,0),self.size)
        pygame.draw.rect(self.surface, (255,255,0), rect, 3)
        pygame.draw.rect(self.surface, (255,0,255), self.deadZoneRect, 2)
    
    def setQuickSelect(self,event):
        self.quickSelect[event.key].empty()
        for entity in self.selectedEntities:
            self.quickSelect[event.key].add(entity)
        
    def getQuickSelect(self,event):
        for entity in self.quickSelect[event.key].sprites():
            entity.select()
            if entity not in self.selectedEntities:
                self.selectedEntities.append(entity)
    
    def postNotification(self):
        """
        If the world has notifications, post the first 
        notification.
        """
        if len(self.world.notifications) > 0:
            self.manager.post(self.world.notifications.pop(0))
    
    def changeWorld(self,world):
        self.world = world
        self.minimap = MiniMap(self.world)
        self.worldSize=self.world.grid.getCartGridDimensions()
