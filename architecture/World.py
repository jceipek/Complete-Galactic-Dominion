from Entity import Entity
from Structure import TestTownCenter
from NaturalObject import Gold

import specialMath

from Event import ResourceChangeEvent,GameOverEvent

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
    
    """
    NETWORKING DIRECTIONS
    
    To pickle:
        self.allEntities
        self.grid
        self.gridDim
        self.universe
        self.worldID
        self.resourceContainer
        
    To not-pickle:
        self.notifications
        self.deadEntities
    """
    
    def __init__(self, universe, grid=None):
        
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
        
        # holds time elapsed since last frame
        # updated every new frame by viewport with reference to this world
        self.elapsedTimeSinceLastFrame = 0
    
        #self._generateResources()
        #self._TMPmakeBuilding()
        
        self.resourceContainer = WorldResourceContainer(self)
        
        self.notifications = []
        
        # Contains a list of entities which have died, and called upon
        # the removeEntity method.
        self.deadEntities = []
        
        self.playerCount = {}
    
    def _setWorldID(self,ID):
        self.worldID = ID
        
    def _TMPmakeBuilding(self):
        from random import randint,choice
        xpos = randint(0,self.gridDim[0])
        ypos = randint(0,self.gridDim[1])
        TestTownCenter(xpos,ypos,self)
    
    def _generateResources(self):
        
        from random import randint,choice
        
        resourceType = [Gold]
        
        for i in xrange(randint(10,15)):
            # FIXME
            xpos = randint(100,self.gridDim[0]-100)
            ypos = randint(100,self.gridDim[1]-100)
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

        for entity in self.allEntities.values():
                  
            for view in viewRects:
                #if entity.collRect.colliderect(viewRect):
                if self.collideRectDiamond(entity.rect,view):
                    #entitySortList.append((entity.rect.bottom,entity))
                    entitySortList.append((specialMath.cartToIso(entity.rect.center),entity))
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
            return False
        if self.line(pLow,pRight,left)>=top:
            return False
        if self.line(pHigh,pRight,left)<=bottom:
            return False
        if self.line(pLow,pLeft,right)>=top:
            return False
        return True
    
    def addNotification(self,event):
        """
        Adds a NotificationEvent to a list of such events.
        """
        self.notifications.append(event)
    
    def getDeadEntities(self):
        """
        Returns the current list of dead entities, and resets the list.
        """
        self.deadEntities,deadEntities = [],self.deadEntities
        return deadEntities
    
    def addEntity(self, entity):
        """
        Adds an entity to a world in the allEntities dictionary.
        maps entityID to an entity.
        """
        self.universe.addEntity(entity)
        self.allEntities[entity.entityID] = entity
        
        self.playerCount.setdefault(entity.owner,[]).append(entity.entityID)
        #return entityID

    def removeEntity(self, entity):
        """Removes an entity from the World."""
        if entity.entityID in self.allEntities:
            self.deadEntities.append(entity)
            self.universe.removeEntity(entity)
            del self.allEntities[entity.entityID]
            
            try:
                self.playerCount[entity.owner].remove(entity)
            except ValueError: # thrown if entity not in list
                pass
            
            if len(self.playerCount[entity.owner]) == 0:
                self.addNotification(GameOverEvent())
            
    def addResource(self,playerID,resource,amount=1):
        deposited = self.resourceContainer.addResource(playerID,resource,amount)
        if deposited > 0:
            amountRemaining=self.resourceContainer.getResourceCount(playerID,resource)
            self.addNotification(ResourceChangeEvent(resource,amountRemaining))
        return deposited
        
    def removeResource(self,playerID,resource,amount=1):
        removed = self.resourceContainer.removeResource(playerID,resource,amount)
        if removed > 0:
            amountRemaining=self.resourceContainer.getResourceCount(playerID,resource)
            self.addNotification(ResourceChangeEvent(resource,amountRemaining))
        return removed
        
    def hasResources(self,playerID,resource,amount=1):
        return self.resourceContainer.hasResources(playerID,resource,amount)
    
    def sendEventToManager(self,event):
        """
        Sends an event to an event manager.
        """
        self.universe.sendEventToManager(event)

class WorldResourceContainer(object):
    """
    Maps from player ids to resouces.
    """
    def __init__(self,world):
        
        self.world = world
        self.resources = {}
        
    def addPlayer(self,playerID):
        self.resources[playerID] = PlayerResourceContainer(self.world)
    
    def hasPlayer(self,playerID):
        return playerID in self.resources
    
    def addResource(self,playerID,resource,amount=1):
        if self.hasPlayer(playerID):
            return self.resources[playerID].addResource(resource,amount)
        else:
            print 'Player %s not yet added'%playerID
            return None
        
    def removeResource(self,playerID,resource,amount=1):
        if self.hasPlayer(playerID):
            return self.resources[playerID].removeResouce(resource,amount)
        else:
            print 'Player %s not yet added'%playerID
            return None
    
    def getResourceCount(self,playerID,resource):
        if self.hasPlayer(playerID):
            return self.resources[playerID].getResourceCount(resource)
    
    def getResources(self,playerID,resource):
        if self.hasPlayer(playerID):
            return self.resources[playerID]
        else:
            print 'Player %s not yet added'%playerID
            return None
            
    def hasResources(self,playerID,resource,amount=1):
        if self.hasPlayer(playerID):
            return self.resources[playerID].hasResources(resource,amount)
        else:
            print 'Player %s not yet added'%playerID
            return None
        
class PlayerResourceContainer(object):
    
    def __init__(self,world):
        
        self.world = world
        self.resources = {}
        
        self._setupResourceDict()
        
    def _setupResourceDict(self):
        
        self.resources[Gold] = 0
        
    def addResource(self,resource,amount=1):
        
        if resource in self.resources:
            self.resources[resource]+=amount
            return amount
        else:
            return 0
            
    def removeResouce(self,resource,amount=1):
        
        if resource in self.resources:
            resourcesRemaining = self.resources[resource]
            
            if resourcesRemaining >= amount:
                self.resources[resource]-=amount
                return amount
            else:
                self.resources[resource]=0
                return resourcesRemaining
                
    def hasResources(self,resource,amount):
        
        if resource in self.resources:
            return self.resources[resource] >= amount
        return False
    
    def getResourceCount(self,resource):
        return self.resources.get(resource,None)
    
    def __str__(self):
		s='Player Resources: \n'
		for resource in self.resources:
			sitem=str(resources).rsplit('.',1)[1].strip(punctuation)
			s+= '%s : %d \n' % (sitem, self.resources[resources])
		return s	
