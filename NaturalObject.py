import Entity

class NaturalObject(Entity):

"""
description: description of behavior, abilities (inherited from Entity)
x: position (inherited from Entity)
y: position (inherited from Entity)
maxHealth: maximum/ default health points (inherited from Entity)
curHealth: current health (inherited from Entity)
size: radius of collision (inherited from Entity)
"""


    def __init__(self, imagePath, colorkey=None):
        Entity.__init__(self, imagePath, colorkey)
        blockable=True
	

    def update():
	"""called each frame to update object"""
	pass
	
