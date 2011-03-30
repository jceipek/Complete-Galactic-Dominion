from Entity import Entity

class World(object):
    """
    A World is an object that contains everything in the current environment
    that the player is able to see on the map by scrolling around. A World could
    thus be a planet, a spaceship, a building, etc... - Julian
    
    The boundaries for displaying a World are specified in the interface, which
    is capable of displaying a portion of a World. - Julian
    
    #Attributes:
    #   grid
    #   resource counts on a per-player basis
    #   resourceCountDerived = boolean explaining whether resources are 
                               dependent on sub-worlds
    """
    
    def __init__(self, grid=None): #FIXME got rid of a comma, did we lose something?
        
        # maps entityID of each entity to a pointer to the entity
        # may need to map tuple of entityID and ownerID later when
        # multiple players own units in a world
        
        self.allEntities = dict()
        
        self.grid = grid #Needs to be linked to a grid object, default None
        if self.grid == None:
            self.TEST_createGrid()
        self.gridDim = self.grid.getGridDimensions()
        
    def TEST_createGrid(self):
        from Grid import InfiniteGrid
        self.grid = InfiniteGrid((20,20),64)

    def update(self):
        """Sends an update message to all entities."""
        for entity in self.allEntities.values():
            entity.update()
    
    def getScreenEntities(self,viewRect1,viewRect2,viewRect3,viewRect4):
        """
        Receives the rectangle of the screen object (NOTE: MUST BE
        DEFINED IN THE SAME WAY AS THE RECT OBJECT OF ENTITIES ARE.
        EITHER MUST BE BOTH ABSOLUTE OR BOTH RELATIVE TO SCREEN!!!)
        Returns a list of references to entities which are visible
        in the viewport.
        """

        # List of tuples - y position of rectangle (bottom) and entity
        entitySortList = []
        
        '''
        xmod,ymod = self.gridDim
        left,top=viewRect.topleft
        right,bottom=viewRect.bottomright
        '''
        
        #print self.gridDim
        #viewRect.top = viewRect.top%ymod
        #viewRect.left = viewRect.left%xmod
        
        # Determines entities in the world which collide with the screen
        # and appends them to a list
        #print 'Viewing rect: ',viewRect
        
        for entity in self.allEntities.values():
            #if entity.collRect.colliderect(viewRect):
            if self.collideRectDiamond(entity.rect,viewRect1) \
            or self.collideRectDiamond(entity.rect,viewRect2) \
            or self.collideRectDiamond(entity.rect,viewRect3) \
            or self.collideRectDiamond(entity.rect,viewRect4):
                entitySortList.append((entity.rect.bottom,entity))
            if entity.entityID == 1:
                pass#print 'Collision rect of 1st entity: ',entity.collRect
        
        entitySortList.sort()
        
        if len(entitySortList) > 0:
            ypos, screenEntities = zip(*entitySortList)
        else:
            screenEntities = []
            
        return screenEntities
        
    def collideRectDiamond(self,rect1,diamond):
        left,top=rect1.topleft
        right,bottom=rect1.bottomright
        bottom,top=sorted((top,bottom))
        left,right=sorted((left,right))
        
        pHigh,pLow,pLeft,pRight=diamond
        
        pRight=max(diamond)
        pLeft=min(diamond)
        pHigh=pLow=diamond[0]
        for i in range(1,len(diamond)):
            if diamond[i][1]>pHigh[1]:
                pHigh=diamond[i]
            if diamond[i][1]<pLow[1]:
                pLow=diamond[i]
        
        def line(p1,p2,x):
            slope=(p1[1]-p2[1])/(p1[0]-p2[0])
            y=slope*(x-p1[0])+p1[1]
            return y
        
        if line(pHigh,pLeft,right)<=bottom:
            return False
        if line(pLow,pRight,left)>=top:
            return False
        if line(pHigh,pRight,left)<=bottom:
            return False
        if line(pLow,pLeft,right)>=top:
            return False
        return True
    
    def addEntity(self, entity):
        """
        Adds an entity to a world in the allEntities dictionary.
        maps entityID to an entity.
        """
        self.allEntities[entity.entityID] = entity

    def removeEntity(self, entity):
        """Removes an entity from the World."""
        if entity.entityID in self.allEntities:
            del self.allEntities[entity.entityID]
