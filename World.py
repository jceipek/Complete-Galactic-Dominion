import DrawableObject

class World
    """A container for everything that the player can see by scrolling around the map."""
    
    def __init__(self):
        DrawableObject.__init__(self)
        """This will eventually need some kind of 
        view boundaries, and will probably overwrite
        the display method in drawable object to limit
        it to the viewing area"""