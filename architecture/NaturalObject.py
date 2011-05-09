from Entity import Entity
from Overlay import HealthBar

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
    owner = 'gaia'
    
    def __init__(self, imagePath, x, y, world, colorkey=None,
                 description = 'No information available.'):
        Entity.__init__(self,imagePath,x,y,world,colorkey,description)
        self.blockable=True
        self.collectible=False
        self.maxHealth = self.curHealth = 0
       
    def __getState__(self):
        state = self.__dict__.copy()
        
        if self.world != None:
            state['world'] = self.world.worldID
            
        if state['image'] != None:
            del state['image']
        
        del state['healthBar']
      
        return state
        
    def __setstate__(self,state):
        self.__dict__ = state
        #the realCenter attribute will be overwritten in _imageInformationSetup()
        #this location needs to be preserved
        realCenter = self.realCenter
        self._imageInformationSetup()
        self.rect.center = self.realCenter = realCenter
        
        self.healthBar = HealthBar(self)
        self.selected = False

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
        self.collectible = True
        self.regenRate = 0
        self._regenHealth = 0

class Gold(Resource):
    """Gold."""
    
    name = 'Gold Ore'
    
    def __init__(self,x,y,world):
        desc = """Gold ore is highly valued for its wonderous sheen and usefulness as an interstellar currency."""
        Resource.__init__(self,'Gold-ore.png',x,y,world,'alpha',desc)
        
        self.regenRate = 1

    def getMiniMapColor(self):
        return (255,215,0)

    def __getstate__(self):
        return NaturalObject.__getState__(self)
        
    def __setstate__(self,state):
        return NaturalObject.__setstate__(self,state)

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
