class World():
    """A container for everything that the player can see by scrolling
    around the map."""
    
    def __init__(self):
        """This will eventually need some kind of 
        view boundaries, and will probably overwrite
        the display method in drawable object to limit
        it to the viewing area"""

        # Represents number of WorldSquares to have
        self.worldColumns = 10
        self.worldRows = 10

        # Dictionary mapping tuples of world column/row indicies to
        # WorldSquares
        # May change this to a numpy style array of WorldSquares
        self.worldSquareDict = {}

        # Populate worldSquareDict.  Indicies start at 1.
        for c in range(1,worldColumns+1):
            for r in range(1,worldRows+1):
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
        self.positionDict = {}
