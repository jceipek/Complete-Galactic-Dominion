class World(object):
    """A World is an object that contains everything in the current environment
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
    
    def __init__(self):
        self.resourceCountDict = dict() #Maps from player IDs to ResourceCount objects
        self.grid = None #Needs to be linked to a grid object

    def TEST_createGrid(self):
        from Grid import InfiniteGrid
        self.grid = InfiniteGrid((100,100),64)

    def update(self):
        pass
