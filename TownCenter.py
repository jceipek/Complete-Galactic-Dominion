import Structure
class TownCenter(Structure):
	"""defines Town Center structure """
	resourcesRequired=None
	timeToBuild=0
	def __init__(self):
		Structure.__init__(self)

	def update(self):
		"""called each frame to update object"""

	def build(self):
		"""build first Unit in unitsBuilt queue"""

