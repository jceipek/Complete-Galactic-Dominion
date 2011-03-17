import NaturalObject

class Resource(NaturalObject):
    """Gatherable by villagers that is used to make builders"""
	Attributes:
	description: description of behavior, abilities (inherited from Entity)
	x: position (inherited from Entity)
	y: position (inherited from Entity)
	maxHealth: maximum/ default health points (inherited from Entity)
	curHealth: current health (inherited from Entity)
	size: radius of collision (inherited from Entity)
	
    def __init__(self):
        NaturalObject.__init__(self)
        resourceType=none
                
	type: type of resource

	Methods:
	update(): updates the resource
	-----------------inherited from superclasses
	die(self): entity is removed from map
	changeHealth(self, numHits): decreases the health of the entity based on number of hits


