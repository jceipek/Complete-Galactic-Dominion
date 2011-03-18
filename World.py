import numpy as n

class World():
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

        # Represents number of WorldSquares to have
        self.worldColumns = 10
        self.worldRows = 10

        # Dictionary mapping tuples of world column/row indicies to
        # WorldSquares
        # May change this to a numpy style array of WorldSquares
        self.worldSquareDict = {}

        # Populate worldSquareDict.  Indicies start at 0.
        for c in range(worldColumns):
            for r in range(worldRows):
                ### Currently empty instances
                self.worldSquareDict[(c,r)] = WorldSquare()

        
class WorldSquare():
    """A container for each large discrete segment of the map.  Will contain
    terrain features, structures, and groups of Sprites."""

    def __init__(self):

        # Represents number of discrete positions within WorldSquare
        self.positionColumns = 30
        self.positionRows = 30

        # Dictionary mapping tuples of world column/row indicies to
        # WorldSquares.  Should only contain static objects (not units)
        # Will be used for many functions, including pathfinding.
        self.positionDict = n.array()
