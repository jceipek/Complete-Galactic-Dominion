import MapObject

class Entity
    """A foreground MapObject with which one can interact."""
    
    def __init__(self):    
        MapObject.__init__(self)
        """Here we need to define some kind of
        variable that keeps track of what
        an entity can do."""