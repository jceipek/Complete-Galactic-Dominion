from Unit import Builder, Unit, TestUnit
from Entity import Locals

import radialMenu
from Callback import Callback
from NaturalObject import Gold
from Overlay import HealthBar

from Event import NotificationEvent

class Structure(Builder):
    """Defines structues which are built by units"""

    acceptableResources = []

    def __init__(self, imagePath, x, y, world, colorkey=None,
                 description = 'No information available.', owner='tmp'):
        Builder.__init__(self, imagePath, x, y, world, colorkey, description,
            owner)

        self.status = Locals.IDLE
        self.maxHealth=100
        self.curHealth=self.maxHealth
        self.movable=False

    def __getstate__(self):
        state = self.__dict__.copy()
        
        if self.world != None:
            state['world']=self.world.worldID
            
        if state['image'] != None:
            del state['image']
            
        del state['healthBar']
        
        return state
        
    def __setstate__(self,state):
        self.__dict__ = state
        
        self.loadImage(self.imagePath,self.colorkey)
        self.healthBar = HealthBar(self)
        
        self.rect.center = self.realCenter
        self.selected = False
          
    '''Pickle functions for network transfer:'''
    def __getState__(self):
        stateDict = Builder.__getState__(self)
        stateDict['buildX'] = self.buildX
        stateDict['buildY'] = self.buildY
        stateDict['status'] = self.status
        return stateDict
    
class TestTownCenter(Structure):
    """Defines structues which are built by units"""

    acceptableResources = [Gold]
    costToBuild = [(Gold,500)]
    
    name = 'Town Center'
    
    def __init__(self, x, y, world, owner='tmp'):
        Structure.__init__(self, 'TownCenter.png', x, y, world, 'alpha', 'Test building.',owner)
            
        self.buildDict = {
            TestUnit: TestUnit
        }
        
    def getMiniMapColor(self):
        return (255,255,255)
