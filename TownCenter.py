import Structure
class TownCenter(Structure):
	"""defines Town Center structure """
	resourcesRequired=None
	timeToBuild=0
	def __init__(self, imagePath, colorkey=None):
		Structure.__init__(self, imagePath, colorkey)

	def update(self):
		"""called each frame to update object"""

	def build(self):
		"""build first Unit in unitsBuilt queue"""

