import Unit

class Villager
    """A kind of Unit that can gather resources."""
    
    def __init__(self, imagePath, colorkey=None):
        Unit.__init__(self, imagePath, colorkey)
        
