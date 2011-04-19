from Unit import Builder, Unit
from Entity import Locals

import radialMenu
from Callback import Callback
from NaturalObject import Gold

class Structure(Builder):
    """Defines structues which are built by units"""

    acceptableResources = []

    def __init__(self, imagePath, x, y, world, colorkey=None,
                 description = 'No information available.', owner='tmp'):
        Builder.__init__(self, imagePath, x, y, world, colorkey, description,
            owner)

        self.status = Locals.IDLE
        self.maxHealth=9000
        self.curHealth=self.maxHealth
        
    def depositResources(self,unitList):
        print 'Depositing...: ',unitList
        for unit in unitList:
            if isinstance(unit,Unit):
                inventory = unit.inventory
    
                for resource in inventory.items:
                    
                    if resource in self.acceptableResources:
                        amountToDeposit = inventory.removeAll(resource)
                        amountDeposited = self.world.addResource(self.owner,resource,amountToDeposit)
                        if amountToDeposit != amountDeposited:
                            print 'Warning: did not deposit correct amount of resources.'
                            
    '''Pickle functions for network transfer:'''
    def __getState__(self):
        stateDict = Builder.__getState__(self)
        stateDict['buildX'] = self.buildX
        stateDict['buildY'] = self.buildY
        stateDict['status'] = self.status
        stateDict['buildX'] = self.buildX
        return stateDict
    

class TestTownCenter(Structure):
    """Defines structues which are built by units"""

    acceptableResources = [Gold]
    
    def __init__(self, x, y, world, owner='tmp'):
        Structure.__init__(self, 'TownCenter.png', x, y, world, 'alpha', 'Test building.',owner)
        
        self.buildDict = {
            Unit: 
                lambda : Unit('testCraft.png',self.buildX,self.buildY,self.world,'alpha','A Unit.')
            }
