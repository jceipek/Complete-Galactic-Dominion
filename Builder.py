import Entity

class Builder
    """A kind of entity that can create things (units or structures)."""
    
    def __init__(self, imagePath, colorkey=None):
        Entity.__init__(self, imagePath, colorkey)
