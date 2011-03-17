import Entity

class NaturalObject(Entity):

description: description of behavior, abilities (inherited from Entity)
x: position (inherited from Entity)
y: position (inherited from Entity)
maxHealth: maximum/ default health points (inherited from Entity)
curHealth: current health (inherited from Entity)
size: radius of collision (inherited from Entity)


    def __init__(self):
        Entity.__init__(self)
        blockable=True
	

	Methods:
	update(): updates the Natural Object
	------------------inherited from superclasses
	die(self): entity is removed from map
	changeHealth(self, numHits): decreases the health of the entity based on number of hits
