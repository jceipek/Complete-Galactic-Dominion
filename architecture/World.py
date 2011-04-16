from Entity import Entity

from NaturalObject import Gold

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
    
    # class variable which holds time elapsed since last frame
    # updated every new frame by viewport with reference to this world
    elapsedTimeSinceLastFrame = 0
    
    def __init__(self, universe, grid=None): #FIXME got rid of a comma, did we lose something?
        
        # maps entityID of each entity to a pointer to the entity
        # may need to map tuple of entityID and ownerID later when
        # multiple players own units in a world
        
        self.allEntities = dict()
        
        if grid == None:
            self.TEST_createGrid()
        else:
            self.grid = grid #Needs to be linked to a grid object, default None
        self.gridDim = self.grid.getCartGridDimensions()
    
        self.universe=universe
        
        self.worldID = None
        # Sets world ID
        self.universe.addWorld(self)
    
        self._generateResources()
    
    def _setWorldID(self,ID):
        self.worldID = ID
    
    def _generateResources(self):
        
        from random import randint,choice
        
        resourceType = [Gold]
        
        for i in xrange(randint(10,15)):
            xpos = randint(0,self.gridDim[0])
            ypos = randint(0,self.gridDim[1])
            (choice(resourceType))(xpos, ypos, self)
    
    def TEST_createGrid(self):
        from Grid import InfiniteGrid
        self.grid = InfiniteGrid((30,30),64)

    def update(self):
        """Sends an update message to all entities."""
        for entity in self.allEntities.values():
            entity.update()
    
    def getScreenEntities(self,viewRects):
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
        
        entCount=0

        for entity in self.allEntities.values():
                  
            for view in viewRects:
                #if entity.collRect.colliderect(viewRect):
                if self.collideRectDiamond(entity.rect,view):
                    entitySortList.append((entity.rect.bottom,entity))
                    entCount+=1
                    entity.drawOffset=-view[0][0],-view[0][1]
                    break # if it collides, go to next loop

        entitySortList.sort()
        
        if len(entitySortList) > 0:
            ypos, screenEntities = zip(*entitySortList)
        else:
            screenEntities = []
            
        return screenEntities
    
    def line(self,p1,p2,x):
        run = p1[0]-p2[0]
        if not run == 0:
            slope=(p1[1]-p2[1])/run
            return slope*(x-p1[0])+p1[1]
        else:
            raise ValueError, 'Check the coordinate system.'
    
    def collideRectDiamond(self,rect1,diamond):
        left,top=rect1.topleft
        right,bottom=rect1.bottomright
        bottom,top=sorted((top,bottom))
        left,right=sorted((left,right))
        
        #pHigh,pLow,pLeft,pRight=diamond
        #print diamond
        
        # Point farthest to the right
        pRight=max(diamond)
        # Point farthest to the left
        pLeft=min(diamond)
        pHigh=pLow=diamond[0]
        
        # Finds lowest and highest point in diamond
        for i in xrange(1,len(diamond)):
            if diamond[i][1]>pHigh[1]:
                pHigh=diamond[i]
            if diamond[i][1]<pLow[1]:
                pLow=diamond[i]
        
        if self.line(pHigh,pLeft,right)<=bottom:
            #print 'fail1'
            return False
        if self.line(pLow,pRight,left)>=top:
            #print 'fail2'
            return False
        if self.line(pHigh,pRight,left)<=bottom:
            #print 'fail3'
            return False
        if self.line(pLow,pLeft,right)>=top:
            #print 'fail4'
            return False
        return True
    
    def addEntity(self, entity):
        """
        Adds an entity to a world in the allEntities dictionary.
        maps entityID to an entity.
        """
        self.universe.addEntity(entity)
        self.allEntities[entity.entityID] = entity
        
        #return entityID

    def removeEntity(self, entity):
        """Removes an entity from the World."""
        if entity.entityID in self.allEntities:
            self.universe.removeEntity(entity)
            del self.allEntities[entity.entityID]
