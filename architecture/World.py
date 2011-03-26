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
        
    def TEST_createGrid(self):
        from Grid import InfiniteGrid
        self.grid = InfiniteGrid((100,100),64)

    def update(self):
        """Sends an update message to all entities."""
        for entity in self.allEntities.values():
            entity.update()
    
    def getScreenEntities(self,playerScreenRect):
        """
        Receives the rectangle of the screen object (NOTE: MUST BE
        DEFINED IN THE SAME WAY AS THE RECT OBJECT OF ENTITIES ARE.
        EITHER MUST BE BOTH ABSOLUTE OR BOTH RELATIVE TO SCREEN!!!)
        Creates a list of tuples containing y-coordinate and entity
        reference to sort in the order of which the entities should be 
        drawn for the provided playerScreenRect
        """

        playerScreenEntities = []
        
        # Determines entities in the world which collide with the screen
        # and appends them to a list
        for entity in self.allEntities.values():
            if entity.collRect.colliderect(playerScreenRect):
                playerScreenEntities.append((entity.rect.bottom,entity))
        
        # sorts in order in which to draw entities        
        playerScreenEntities.sort()
        
        return playerScreenEntities
    
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
