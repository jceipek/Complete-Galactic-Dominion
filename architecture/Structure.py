from Unit import Builder, Unit
from Entity import Locals

import radialMenu
from Callback import Callback

class Structure(Builder):
    """Defines structues which are built by units"""

    def __init__(self, imagePath, x, y, world, colorkey=None,
                 description = 'No information available.'):
        Builder.__init__(self, imagePath, x, y, world, colorkey, description)

        # first to define these attributes
        # sets where a new entity should be constructed
        self.buildX,self.buildY = self.rect.center

        self.status = Locals.IDLE
	self.maxHealth=9000
	self.curHealth=self.maxHealth
            
class TestTownCenter(Structure):
    """Defines structues which are built by units"""

    def __init__(self, x, y, world):
        Structure.__init__(self, 'TownCenter.png', x, y, world, 'alpha', 'Test building.')

        self.buildDict = {
            Unit: 
                lambda : Unit('testCraft.png',self.buildX,self.buildY,self.world,'alpha','A Unit.')
            }
            
        self.setupMenu()
    
    def setupMenu(self):
        #Set up the test menu:
        menu = radialMenu.RMenu()
        
        #print 'BuildDictLength ',len(self.buildDict)
        if len(self.buildDict) > 0:
            
            buildItem = radialMenu.RMenuItem(menu,
                image = "orbPurpleBlack.png",
                col = (255,0,255),
                title = 'Build Options')
            
            menu.addItem(buildItem)
            
            buildMenu = radialMenu.RMenu()
            buildItem.addSubmenu(buildMenu)
            
            tmpcounter = 0
            for buildType in self.buildDict:
                curCallback = Callback(self.addToBuildQueue,Unit)
                curItem = radialMenu.RMenuItem(menu,
                    image = "orbQBlack.png",
                    col = (255,0,0),
                    title = 'Item#'+str(tmpcounter),
                    callback = curCallback)
                    #callback = self.buildDict[buildType])
                buildMenu.addItem(curItem)
                tmpcounter+=1
        
        buildMenu.addItem(radialMenu.RMenuItem(menu,
                image = "orbPurpleBlack.png",
                col = (255,0,255),
                title = 'Build Options'))
        self.clickMenu = menu
    
    def getMenu(self):
        return self.clickMenu
    
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
