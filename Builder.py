import Entity
Attributes:
description: description of behavior, abilities (inherited from Entity)
x: position (inherited from Entity)
y: position (inherited from Entity)
maxHealth: maximum/ default health points (inherited from Entity)
curHealth: current health (inherited from Entity)
size: radius of collision (inherited from Entity)

---------------------methods inherited from SuperClasses
die(self): entity is removed from map
changeHealth(self, numHits): decreases the health of the entity based on number of hits


class Builder
    """A kind of entity that can create things (units or structures)."""
    
    def __init__(self, imagePath, colorkey=None):
        Entity.__init__(self, imagePath, colorkey)
	

	def Build(builder1): the default build function that serves as a base for the local build functions in the sub classes
	"""A particular builder creates builder1 after a certain timeToBuild"""	
		if builder1 == unit:
			newUnit=unit()
			return newUnit()
		elif builder1 == structure:
			newStructure=structure()
			return newStructure 
	

	unitsBuilt: queue of type of each unit to be built
	canBuild: list of units that can be built
	player: the player this unit belongs
	creationStatus: status of the unit the villager is building
	timeToBuild: amount of time it takes from structure to be built
	resourcesRequired: (numWood): tuple of amount of each resource needed



