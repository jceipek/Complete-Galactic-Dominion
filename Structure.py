import Builder
class Structure(Builder)
"""Defines structues which are built by units"""

        def __init__(self, imagePath, colorkey=None):
                Builder.__init__(self, imagePath, colorkey)

                # first definition of resourcesRequired
                self.resourcesRequired = []

                # first definition of timeToBuild
                self.timeToBuild = 0
		
