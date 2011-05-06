import Builder
class Structure(Builder)
"""Defines structues which are built by units"""

        def __init__(self, imagePath, colorkey=None):
                Builder.__init__(self, imagePath, colorkey)

                self.status=IDLE

		def build(self):
            """builds first Unit in unitsBuilt queue"""

        def update(self):
            """called each frame to update object"""
