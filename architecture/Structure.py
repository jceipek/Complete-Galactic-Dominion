from Unit import Builder, Unit
from Entity import Locals

class Structure(Builder):
    """Defines structues which are built by units"""

    def __init__(self, imagePath, x, y, world, colorkey=None,
                 description = 'No information available.'):
        Builder.__init__(self, imagePath, x, y, world, colorkey, description)

        # first to define these attributes
        # sets where a new entity should be constructed
        self.buildX,self.buildY = self.rect.center

        self.status = Locals.IDLE
            
class TestTownCenter(Structure):
    """Defines structues which are built by units"""

    def __init__(self, x, y, world):
        Structure.__init__(self, 'TownCenter.png', x, y, world, 'alpha', 'Test building.')

        self.buildDict = {
            Unit: 
                lambda : Unit('testCraft.png',self.buildX,self.buildY,self.world,'alpha','A Unit.')
            }


'''
class TownCenter(Structure):
	"""defines Town Center structure """
	resourcesRequired=None
	timeToBuild=0
	def __init__(self, imagePath, colorkey=None):
		Structure.__init__(self, imagePath, colorkey)
'''
