from Unit import Builder, Unit
from Entity import Locals

import radialMenu
from Callback import Callback
from NaturalObject import Gold

class Structure(Builder):
    """Defines structues which are built by units"""

    acceptableResources = []

    def __init__(self, imagePath, x, y, world, colorkey=None,
                 description = 'No information available.'):
        Builder.__init__(self, imagePath, x, y, world, colorkey, description)

        # first to define these attributes
        # sets where a new entity should be constructed
        self.buildX,self.buildY = self.rect.center

        self.status = Locals.IDLE
        self.maxHealth=9000
        self.curHealth=self.maxHealth

    def __getstate__(self):
        state = self.__dict__.copy()
        if self.world != None:
            state['world']=self.world.worldID
        state['image']=None
        
    def __setstate__(self,state):
        pass
        
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
            
class TestTownCenter(Structure):
    """Defines structues which are built by units"""

    acceptableResources = [Gold]
    
    def __init__(self, x, y, world):
        Structure.__init__(self, 'TownCenter.png', x, y, world, 'alpha', 'Test building.')

        self.buildDict = {
            Unit: 
                lambda : Unit('testCraft.png',self.buildX,self.buildY,self.world,'alpha','A Unit.')
            }
            
        self.menuActors = []
        self.menus = {}
        
        self.setupMenus()
    '''        
    def setupMenu(self):
        #Set up the test menu:
        menu = radialMenu.RMenu()
        
        #print 'BuildDictLength ',len(self.buildDict)
        if len(self.buildDict) > 0:
            
            buildItem = radialMenu.RMenuItem(menu,
                image = "orbQBlack.png",
                col = (255,0,255),
                title = 'Build Options')
            
            menu.addItem(buildItem)
            
            buildMenu = radialMenu.RMenu()
            buildItem.addSubmenu(buildMenu)
            
            tmpcounter = 0
            for buildType in self.buildDict:
                curItem = radialMenu.RMenuItem(menu,
                    image = "orbQBlack.png",
                    col = (255,0,0),
                    title = 'Build Option #'+str(tmpcounter),
                    callback = Callback(self.addToBuildQueue,Unit))
                    #callback = self.buildDict[buildType])
                buildMenu.addItem(curItem)
                tmpcounter+=1
        
        self.clickMenu = menu
    '''
    def setupMenus(self):
        self._setupNoneMenu()
        self._setupSelfMenu()
        #self._setupOtherMenu()

    def _setupNoneMenu(self):
        #Set up the None menu:
        menu = radialMenu.RMenu()
        
        if len(self.buildDict) > 0:
            
            buildItem = radialMenu.RMenuItem(menu,
                image = "orbQBlack.png",
                col = (255,0,255),
                title = 'Build Options')
            
            menu.addItem(buildItem)
            
            buildMenu = radialMenu.RMenu()
            buildItem.addSubmenu(buildMenu)
            
            tmpcounter = 0
            for buildType in self.buildDict:
                curItem = radialMenu.RMenuItem(menu,
                    image = "orbQBlack.png",
                    col = (255,0,0),
                    title = 'Build Option #'+str(tmpcounter),
                    callback = Callback(self.addToBuildQueue,Unit))
                    #callback = self.buildDict[buildType])
                buildMenu.addItem(curItem)
                tmpcounter+=1

        self.menus[None] = menu
    
    def _TMPsetupSelfMenu(self):
        self._setupSelfMenu()
    
    def _setupSelfMenu(self):
        #Set up the Self menu
        menu = radialMenu.RMenu()
        
        depositItem = radialMenu.RMenuItem(menu,
            image = "orbQBlack.png",
            col = (255,0,255),
            title = 'Deposit Resources',
            callback = Callback(self.depositResources,self.menuActors))
        menu.addItem(depositItem)
        
        self.menus['self'] = menu
    
    '''    
    def _setupOtherMenu(self):
        #Set up the Other menu
        menu = radialMenu.RMenu()
    '''
    #def getMenu(self):
    #    return self.clickMenu
    
    def getMenu2(self,selected=None):
        self.menuActors = selected
        
        if selected is None or selected == []:
            return self.menus[None]
        
        # FIXME - Assumes all units selected are of the same class
        if isinstance(selected[0],Unit):
            if selected[0].owner == self.owner:
                print 'Want to deposit from...: ',self.menuActors
                self._TMPsetupSelfMenu()
                return self.menus['self']
            #else:
            #    return self.menus['other']
            
        return None
        
    def draw(self,screen,worldOffset=(0,0)):
        
        """
        Draws the entity to the given surface.  The screen should be
        the same which the world grid is drawn on.  The worldOffset is
        the current location of the corner of the viewport in the 
        activeworld.
        """
        
        #gridWidth,gridHeight = self.world.gridDim
        '''
        drawOffset = \
        specialMath.isoToCart((-worldOffset[0],-worldOffset[1]))
        drawRect = self.rect.move(drawOffset)
        '''
        drawRect = self.rect.move(self.drawOffset)
        #left,top=self.world.grid.cartToIso(drawRect.topleft)
        #right,bottom=self.world.grid.cartToIso(drawRect.bottomright)
        #drawRect = pygame.Rect(left,top,right-left,bottom-top)
        
        drawRect.center = self.world.grid.cartToIso(drawRect.center)
        
        #drawRect.top = drawRect.top%gridHeight
        #drawRect.left = drawRect.left%gridWidth
        
        if self.selected:
            self.drawSelectionRing(screen,drawRect)
        if self.selected or self.focused:
            self.drawHealthBar(screen,drawRect)
            self.focused = False
        
        screen.blit(self.image,drawRect)
        
        #self.clickMenu.draw(screen)  

'''
class TownCenter(Structure):
	"""defines Town Center structure """
	resourcesRequired=None
	timeToBuild=0
	def __init__(self, imagePath, colorkey=None):
		Structure.__init__(self, imagePath, colorkey)
'''
