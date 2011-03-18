import Unit

class Villager(Unit)
    """A kind of Unit that can gather resources."""

    buildType=None
    def __init__(self, imagePath, colorkey=None):
        Unit.__init__(self, imagePath, colorkey)
        self.status=IDLE
        
    def gather(self, resource):
         """gathers resource"""

    def attack(self, enemy):
        """attacks enemy unit"""

    def build(self, struct, position):
        """builds structure at position"""

    def update(self):
        """called each frame to update object"""
