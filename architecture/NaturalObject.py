from Entity import Entity

class NaturalObject(Entity):
    """
    description: description of behavior, abilities (inherited from Entity)
    x: position (inherited from Entity)
    y: position (inherited from Entity)
    maxHealth: maximum/ default health points (inherited from Entity)
    curHealth: current health (inherited from Entity)
    size: radius of collision (inherited from Entity)
    """
    
    name = 'Natural Object'
    
    def __init__(self, imagePath, x, y, world, colorkey=None,
                 description = 'No information available.'):
        Entity.__init__(self,imagePath,x,y,world,colorkey,description)
        self.blockable=True
        self.collectable=False
        self.maxHealth = self.curHealth = 0
	
    def collect(self):
        if not self.collectable:
            pass

class Resource(NaturalObject):
    """
    Object on the map which can be collected.  Health may or may 
    not regenerate over time.
    """
    
    name = 'Generic Resource'
    
    def __init__(self, imagePath, x, y, world, colorkey=None,
                 description = 'No information available.'):
                     
        NaturalObject.__init__(self,imagePath,x,y,world,colorkey,
            description)
    
        self.maxHealth = self.curHealth = 500
        
        self.regenRate = 0
        self._regenHealth = 0

class Gold(Resource):
    """Gold."""
    
    name = 'Gold Ore'
    
    def __init__(self,x,y,world):
        Resource.__init__(self,'Gold-ore.png',x,y,world,'alpha',\
            'Gold ore.')
        
        self.regenRate = 1

class Obstacle(NaturalObject):
    """
    Object on the map which is only an obstacle.  Health may or may 
    not regenerate over time.
    
    If the obstacle can never be removed, we may want to add it to the
    background set of images at the initialization of the game...
    We may not want to have to look for it each time separately from
    the background.
    """
    def __init__(self, imagePath, x, y, world, colorkey=None,
                 description = 'No information available.'):
        NaturalObject.__init__(self,imagePath,x,y,world,colorkey,description)
	
    def update(self):
        pass
