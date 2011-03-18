import Unit

class Villager(Unit)
    """A kind of Unit that can gather resources."""

    buildType=None
    def __init__(self, imagePath, colorkey=None):
        Unit.__init__(self, imagePath, colorkey)
        self.status=IDLE
        self.efficieny=1
        
    def gather(self, resource):
         """gathers resource"""

    def attack(self, enemy):
        """attacks enemy unit"""

    def build(self):
        """keeps villiager in place while structure is being built"""
        pass

    def update(self):
        """called each frame to update object"""
