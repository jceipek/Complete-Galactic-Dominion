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
    NETWORKING DIRECTIONS (World networking not yet implemented.)
    
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
        
        # defines the grid space for the world upon which all entities
        # will exist
        if grid == None:
            self.TEST_createGrid()
        else:
            self.grid = grid #Needs to be linked to a grid object, default None
        
        # stores the cartesian dimensions of the grid
        self.gridDim = self.grid.getCartGridDimensions()
    
        # a reference to the universe which stores all of the worlds
        self.universe=universe
        
        self.worldID = None
        # Sets world ID and adds the world to the universe
        self.universe.addWorld(self)
        
        # holds time elapsed since last frame
        # updated every new frame by viewport with reference to this world
        self.elapsedTimeSinceLastFrame = 0
    
        # WorldResourceContainer object which serves to store all
        # of the information about the resources owned by each player
        # in this particular world
        self.resourceContainer = WorldResourceContainer(self)
        
        # a list of notifications to be posted to the manager
        self.notifications = []
        
        # Contains a list of entities which have died, and called upon
        # the removeEntity method.
        self.deadEntities = []
    
    def _setWorldID(self,ID):
        """
        Sets the worldID attribute of the World.  Called by the Universe.
        """
        self.worldID = ID
        
    def _TMPmakeBuilding(self):
        """
        Creates a TestTownCenter placed randomly on the cartesian space
        of the world.
        """
        from random import randint,choice
        xpos = randint(0,self.gridDim[0])
        ypos = randint(0,self.gridDim[1])
        TestTownCenter(xpos,ypos,self)
    
    def _generateResources(self):
        """
        Creates a random amount of resources placed randomly on the 
        cartesian space of the world.
        """
        from random import randint,choice
        
        resourceType = [Gold]
        
        for i in xrange(randint(10,15)):
            # FIXME
            xpos = randint(100,self.gridDim[0]-100)
            ypos = randint(100,self.gridDim[1]-100)
            (choice(resourceType))(xpos, ypos, self)
    
    def TEST_createGrid(self):
        """
        Creates an InfiniteGrid and sets it to the grid attribute
        of the WOrld.
        """
        from Grid import InfiniteGrid
        self.grid = InfiniteGrid((100,100),64)

    def update(self):
        """Sends an update message to all entities."""
        for entity in self.allEntities.values():
            entity.update()
    
    def getScreenEntities(self,viewRects):
        """
        Receives a list of lists of coordinate tuples which define the
        coordinates of one view rectangle (the screen) in cartesian
        coordinates.
        
        Returns a list of references to entities which are visible
        in the given rectangles (called by the viewport).
        """

        # List of tuples - y position of rectangle (bottom) and entity
        entitySortList = []

        for entity in self.allEntities.values():
            
            # check all view rectangles
            for view in viewRects:
                
                # does the entity rectangle (cartesian) collide with
                # the rectangle of the screen transformed from isometric
                # to cartesian?
                if self.collideRectDiamond(entity.rect,view):
                    
                    # if it does, append it to the list
                    entitySortList.append((specialMath.cartToIso(entity.rect.center),entity))
                    
                    # set the drawOffset attribute of the entity for
                    # ease of drawing in the correct spot by the viewport
                    # once the list of references is returned
                    entity.drawOffset=-view[0][0],-view[0][1]
                    
                    break # if it collides, go to next loop

        # sort the list by y-position, such that the returned list
        # is in the correct order for drawing
        entitySortList.sort()
        
        # return only the list of entity references
        if len(entitySortList) > 0:
            ypos, screenEntities = zip(*entitySortList)
        else:
            screenEntities = []
            
        return screenEntities
    
    def line(self,p1,p2,x):
        """
        Returns the y-coordinate of a point between points p1 and p2
        (both two-element tuples) at the given x-coordinate.
        A linear interpolator.
        """
        run = p1[0]-p2[0]
        if not run == 0:
            slope=(p1[1]-p2[1])/run
            return slope*(x-p1[0])+p1[1]
        else:
            raise ValueError, 'Check the coordinate system.'
    
    def collideRectDiamond(self,rect1,diamond):
        """
        Returns a boolean value indicating whether or not a rectangle
        collides with a set of four points (represented as 2-element
        tuples in a) in a list.
        """
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
        
        # decide whether or not the rectangle and the diamond collide
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
        Adds an event (from Event/NotificationEvent.py) to the notifications
        list to be posted to a manager.
        """
        self.notifications.append(event)
    
    def getDeadEntities(self):
        """
        Returns the current list of dead entities, and resets the list.
        Used by the Viewport to clear out its references to entities
        which have died.
        """
        self.deadEntities,deadEntities = [],self.deadEntities
        return deadEntities
    
    def addEntity(self, entity, entityID=None):
        """
        Adds an entity to a world in the allEntities dictionary.
        maps entityID to an entity.
        entityID not yet implemented.
        """
        self.universe.addEntity(entity)
        self.allEntities[entity.entityID] = entity

    def removeEntity(self, entity):
        """
        Removes an entity from the World.
        """
        if entity.entityID in self.allEntities:
            self.deadEntities.append(entity)
            self.universe.removeEntity(entity)
            del self.allEntities[entity.entityID]
            
    def addResource(self,playerID,resource,amount=1):
        """
        Adds the given amount of a specific Resource to the 
        PlayerResourceContainer owned by the player represented by
        playerID in the WorldResourceContainer.
        
        If some resources are deposited, a ResourceChangeEvent is added
        to the notifications list with the amount deposited.
        
        Returns the amount of resources deposited.
        """
        deposited = self.resourceContainer.addResource(playerID,resource,amount)
        if deposited > 0:
            amountRemaining=self.resourceContainer.getResourceCount(playerID,resource)
            self.addNotification(ResourceChangeEvent(resource,amountRemaining,playerID))
        return deposited
        
    def removeResource(self,playerID,resource,amount=1):
        """
        Removes the given amount of a specific Resource to the 
        PlayerResourceContainer owned by the player represented by
        playerID in the WorldResourceContainer.
        
        If some resources are removed, a ResourceChangeEvent is added
        to the notifications list with the amount removed.
        
        Returns the amount of resources removed.
        """
        removed = self.resourceContainer.removeResource(playerID,resource,amount)
        if removed > 0:
            amountRemaining=self.resourceContainer.getResourceCount(playerID,resource)
            self.addNotification(ResourceChangeEvent(resource,amountRemaining,playerID))
        return removed
        
    def hasResources(self,playerID,resource,amount=1):
        """
        Returns a boolean indicating whether or not the player represented
        by playerID (to access its PlayerResourceContainer) has the
        given amount (at least) of the given resource.
        """
        return self.resourceContainer.hasResources(playerID,resource,amount)
    
    def sendEventToManager(self,event):
        """
        Sends an event to an event manager through the Universe.
        """
        self.universe.sendEventToManager(event)

class WorldResourceContainer(object):
    """
    Holds all of the information pertaining to the resources owned
    by each player in the confines of a specific world.
    """
    def __init__(self,world):
        
        self.world = world
        
        # dictionary mapping between playerIDs and PlayerResourceContainers
        self.resources = {}
        
    def addPlayer(self,playerID):
        """
        Adds a new PlayerSourceContainer to the resources dictionary with
        the given playerID as the key.
        """
        self.resources[playerID] = PlayerResourceContainer(self.world)
    
    def hasPlayer(self,playerID):
        """
        Returns boolean indicating whether or not a playerID has been
        added to the WorldResourceContainer.
        """
        return playerID in self.resources
    
    def addResource(self,playerID,resource,amount=1):
        """
        Adds the given amount of the given resource to the
        PlayerResourceContainer owned by the playerID.
        
        If the given playerID is not yet added, it will be added.
        """
        if self.hasPlayer(playerID):
            return self.resources[playerID].addResource(resource,amount)
        else:
            print 'Player %s not yet added'%playerID
            print 'Now adding Player %s'%playerID
            self.addPlayer(playerID)
            return self.addResource(playerID,resource,amount)
        
    def removeResource(self,playerID,resource,amount=1):
        """
        Removes the given amount of the given resource to the
        PlayerResourceContainer owned by the playerID.
        
        If the given playerID is not yet added, it will be added.
        """
        if self.hasPlayer(playerID):
            return self.resources[playerID].removeResouce(resource,amount)
        else:
            print 'Player %s not yet added'%playerID
            print 'Now adding Player %s'%playerID
            self.addPlayer(playerID)
            return self.removeResource(playerID,resource,amount)
    
    def getResourceCount(self,playerID,resource):
        """
        Returns the amount of a specific resource owned by a given
        playerID.
        """
        if self.hasPlayer(playerID):
            return self.resources[playerID].getResourceCount(resource)
    
    def getResources(self,playerID):
        """
        Returns the PlayerResourceContainer owned by the given playerID.
        """
        if self.hasPlayer(playerID):
            return self.resources[playerID]
        else:
            print 'Player %s not yet added'%playerID
            print 'Now adding Player %s'%playerID
            self.addPlayer(playerID)
            return self.getResources(playerID)
            
    def hasResources(self,playerID,resource,amount=1):
        """
        Returns boolean indicating whether or not a playerID
        has the given amount of the given resource.
        """
        if self.hasPlayer(playerID):
            return self.resources[playerID].hasResources(resource,amount)
        else:
            print 'Player %s not yet added'%playerID
            print 'Now adding Player %s'%playerID
            self.addPlayer(playerID)
            return self.hasResources(playerID,resource,amount)
        
class PlayerResourceContainer(object):
    """
    Holds all of the information pertaining to the resources owned
    by a specific player in a specific world.
    """
    def __init__(self,world):
        
        self.world = world
        
        # dictionary mapping between Resources (classes) and integers,
        # indicating the amount of that Resource owned
        self.resources = {}
        
        # sets up the resource dictionary for a player according to
        # the current interactions available in CGD
        self._setupResourceDict()
        
    def _setupResourceDict(self):
        """
        Sets up the resource dictionary to accept Gold resources.
        """
        self.resources[Gold] = 0
        
    def addResource(self,resource,amount=1):
        """
        Attempts to add the given amount of a given resource to the 
        resources dictionary.  Returns the amount added if the resource
        is already in the resource dictionary.  Otherwise, returns 0.
        """
        if resource in self.resources:
            self.resources[resource]+=amount
            return amount
        else:
            return 0
            
    def removeResouce(self,resource,amount=1):
        """
        Attempts to remove the given amount of a given resource from
        the resources dictionary.  Returns the amount of resources
        actually removed as an integer.
        """
        if resource in self.resources:
            resourcesRemaining = self.resources[resource]
            
            # Checks to see if the amount given to remove is greater
            # than the amount of that resource remaining.  If so,
            # it will return the amount remaining, rather than the
            # desired amount to remove
            if resourcesRemaining >= amount:
                self.resources[resource]-=amount
                return amount
            else:
                self.resources[resource]=0
                return resourcesRemaining
        else:
            return 0
                
    def hasResources(self,resource,amount):
        """
        Returns a boolean indicating whether or not the player has a 
        given amount of a given resource.
        """
        if resource in self.resources:
            return self.resources[resource] >= amount
        return False
    
    def getResourceCount(self,resource):
        """
        Returns the amount of a specific resource owned.
        """
        return self.resources.get(resource,0)
    
    def __str__(self):
		s='Player Resources: \n'
		for resource in self.resources:
			sitem=str(resources).rsplit('.',1)[1].strip(punctuation)
			s+= '%s : %d \n' % (sitem, self.resources[resources])
		return s	
