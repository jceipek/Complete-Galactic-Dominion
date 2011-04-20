import radialMenu
from Callback import Callback, GroupCallback, SeriesCallback

class ContextualMenuMaster(object):
    """
    Allows for access to context-specific menus.
    """
    
    def __init__(self):
        """
        Creates a ContextualMenuMaster with a dictionary self.menus.
        This dictionary maps tuples of length two to menus.
        The first element in the tuple is the class which 
        are to perform the action, and the second element in the tuple
        is the class which is to be acted upon.
        """
        object.__init__(self)
        
        self.menus = {}
        
    def addMenu(self,obj1Class,obj2Class,menu):
        """
        Makes a given menu specific to the interaction of obj1Class
        acting on obj2Class.
        """
        self.menus[(obj1Class,obj2Class)] = menu
        
    def getMenu(self,obj1,obj2):
        """
        Returns context specific menu for obj1 acting on obj2.
        """
        # Obj1 is a list
        if type(obj1) == list:
            obj1 = self._sortByClass(obj1)
            if len(obj1) > 0:
                obj1Class = obj1[0].__class__
            else:
                obj1Class = None
        else:
            obj1Class = obj1.__class__
        obj2Class = obj2.__class__
        
        menu = self.menus.get((obj1Class,obj2Class),None)
        if menu is not None:
            return menu.getMenu(obj1,obj2)
        else:
            return None

    def _sortByClass(self,t):
        
        d = {}
        
        for item in t:
            d.setdefault(item.__class__,[]).append(item)
        
        return self._mostCommonClass(d)
            
    def _mostCommonClass(self,d):
        
        mostCommonClass = []
        
        for key in d:
            if len(d[key]) > len(mostCommonClass):
                mostCommonClass = d[key]

        return mostCommonClass
        
class ContextualMenu(object):
    
    def __init__(self,menuMakerFunction = lambda obj1,obj2: None):
        """
        Wrapper for a radialMenu maker.  menuMakerFunction takes
        a list of objects acting on an object to produce a menu.
        """
        object.__init__(self)
        
        self._menuMakerFunction = menuMakerFunction
        
    def getMenu(self,obj1,obj2):
        """
        Returns a radial menu as specified by the maker function.
        """
        return self._menuMakerFunction(obj1,obj2)

class WayPoint(object):
    
    def __init__(self,x,y):
        object.__init__(self)
        
        self.x,self.y = x,y
    
    def getPoint(self):
        return self.x,self.y

#### ENTER CUSTOM DEFINED MENU FUNCTIONS HERE ####

from Structure import Structure,TestTownCenter
from Entity import Entity
from Unit import Unit
from NaturalObject import Gold

from Event import NotificationEvent

def None_TestTownCenter(obj1,obj2):
    
    menu = radialMenu.RMenu(openDelay=.2)

    if len(obj2.buildDict) > 0:
        
        buildItem = radialMenu.RMenuItem(menu,
            image = "BuildOrb.png",
            col = (255,0,255),
            title = 'Build Options')
        
        menu.addItem(buildItem)
        
        buildMenu = radialMenu.RMenu()
        buildItem.addSubmenu(buildMenu)
        
        tmpcounter = 0
        for buildType in obj2.buildDict:
            curItem = radialMenu.RMenuItem(menu,
                image = "orb.png",
                col = (255,0,0),
                title = 'Build Option #'+str(tmpcounter),
                callback = Callback(obj2.addToBuildQueue,buildType))
                #callback = self.buildDict[buildType])
            buildMenu.addItem(curItem)
            tmpcounter+=1

    showDesc = radialMenu.RMenuItem(menu,
        image = "orbQBlack.png",
        col = (255,0,255),
        title = 'Description',
        callback = Callback(obj2.showDescription))
    menu.addItem(showDesc)

    return menu
    
def Unit_TestTownCenter(obj1,obj2):
    
    menu = radialMenu.RMenu(openDelay=.2)
    
    if isinstance(obj1,list):
        hasSameOwner = (obj1[0].owner == obj2.owner)
    else:
        hasSameOwner = (obj1.owner == obj2.owner)
        
    if hasSameOwner:
        
        depositItem = radialMenu.RMenuItem(menu,
            image = "DepositOrb.png",
            col = (255,0,255),
            title = 'Deposit Resources',
            callback = Callback(obj2.depositResources,obj1))
        menu.addItem(depositItem)
        
        return menu
    
    else: # not hasSameOwner
    
        # tell all units to attack
        attackCallbacks = []
        for unit in obj1:
            attackCallbacks.append(unit.initAction)
    
        attackBuilding = radialMenu.RMenuItem(menu,
            image = "AttackOrb.png",
            col = (255,0,0),
            title = 'Attack!',
            callback = GroupCallback(attackCallbacks,obj2))
        
        menu.addItem(attackBuilding)
        
        return menu
        
def Unit_WayPoint(obj1,obj2):
    
    # FIXME - DOES NOT CURRENTLY WORK WITH GROUPS
    
    menu = radialMenu.RMenu(openDelay=.2)
    
    setDestCallbacks = []
    for unit in obj1:
        setDestCallbacks.append(unit.addToPath)
    
    setDestItem = radialMenu.RMenuItem(menu,
        image = "DestOrb.png",
        col = (255,255,255),
        title = 'Setting destination',
        callback = GroupCallback(setDestCallbacks,obj2.getPoint()))

    menu.addItem(setDestItem)
    
    if len(obj1[0].buildDict) > 0:
        
        buildItem = radialMenu.RMenuItem(menu,
            image = "BuildOrb.png",
            col = (255,0,255),
            title = 'Build Options')
        
        menu.addItem(buildItem)
        
        buildMenu = radialMenu.RMenu()
        buildItem.addSubmenu(buildMenu)
        
        tmpcounter = 0
        for buildType in obj1[0].buildDict:
            curItem = radialMenu.RMenuItem(menu,
                image = "orb.png",
                col = (255,0,0),
                title = 'Build Option #'+str(tmpcounter),
                callback = Callback(obj1[0].addToBuildQueue,buildType,obj2.getPoint()))
            buildMenu.addItem(curItem)
            tmpcounter+=1
        
    return menu
    
def Unit_Resource(obj1,obj2):
    
    menu = radialMenu.RMenu(openDelay=.2)
    
    setGatherCallbacks = []
    for unit in obj1:
        setGatherCallbacks.append(unit.initAction)
    
    gatherItem = radialMenu.RMenuItem(menu,
        image = "orbWhiteBlack.png",
        col = (255,255,255),
        title = 'Gathering',
        callback = GroupCallback(setGatherCallbacks,obj2))

    menu.addItem(gatherItem)
        
    return menu
    
def None_Unit(obj1,obj2):
    
    menu = radialMenu.RMenu(openDelay=.2)

    if len(obj2.buildDict) > 0:
        
        buildItem = radialMenu.RMenuItem(menu,
            image = "BuildOrb.png",
            col = (255,0,255),
            title = 'Build Options')
        
        menu.addItem(buildItem)
        
        buildMenu = radialMenu.RMenu()
        buildItem.addSubmenu(buildMenu)
        
        tmpcounter = 0
        for buildType in obj2.buildDict:
            curItem = radialMenu.RMenuItem(menu,
                image = "orb.png",
                col = (255,0,0),
                title = 'Build Option #'+str(tmpcounter),
                callback = Callback(obj2.addToBuildQueue,buildType,obj2.rect.center))
            buildMenu.addItem(curItem)
            tmpcounter+=1

    showDesc = radialMenu.RMenuItem(menu,
        image = "orbQBlack.png",
        col = (255,0,255),
        title = 'Description',
        callback = Callback(obj2.showDescription))
    menu.addItem(showDesc)

    return menu
    
def TestTownCenter_WayPoint(obj1,obj2):
    
    menu = radialMenu.RMenu(openDelay=.2)
    
    # HACK - CAN ONLY ACCEPT 1 TESTTOWNCENTER
    
    if len(obj1[0].buildDict) > 0:
        
        buildItem = radialMenu.RMenuItem(menu,
            image = "BuildOrb.png",
            col = (255,0,255),
            title = 'Build Options')
        
        menu.addItem(buildItem)
        
        buildMenu = radialMenu.RMenu()
        buildItem.addSubmenu(buildMenu)
        
        tmpcounter = 0
        for buildType in obj1[0].buildDict:
            
            makeAndMove = SeriesCallback(obj1[0].buildDict[buildType], *obj1[0].rect.center)
            makeAndMove.addCallback(lambda entity : entity.addToPath(obj2.getPoint()))
        
            queueMake = Callback(obj1[0].addToBuildQueue,
                buildType,obj1[0].rect.center,makeAndMove)
            
            curItem = radialMenu.RMenuItem(menu,
                image = "orb.png",
                col = (255,0,0),
                title = 'Build Option #'+str(tmpcounter),
                callback = queueMake)
            buildMenu.addItem(curItem)
            tmpcounter+=1
            
    return menu

def Unit_Unit(obj1,obj2):
    
    menu = radialMenu.RMenu(openDelay=.2)
    
    setAttackCallbacks = []
    for unit in obj1:
        setAttackCallbacks.append(unit.initAction)
    
    attackItem = radialMenu.RMenuItem(menu,
        image = "AttackOrb.png",
        col = (255,255,255),
        title = 'Attack!',
        callback = GroupCallback(setAttackCallbacks,obj2))

    menu.addItem(attackItem)
        
    return menu
    

def getCGDcontextualMenu():
    
    menuMaster = ContextualMenuMaster()
    
    Unit_TestTownCenter_Menu = ContextualMenu(Unit_TestTownCenter)
    menuMaster.addMenu(Unit,TestTownCenter,Unit_TestTownCenter_Menu)
    
    None_TestTownCenter_Menu = ContextualMenu(None_TestTownCenter)
    menuMaster.addMenu(None,TestTownCenter,None_TestTownCenter_Menu)
    
    Unit_WayPoint_Menu = ContextualMenu(Unit_WayPoint)
    menuMaster.addMenu(Unit, WayPoint, Unit_WayPoint_Menu)
    
    Unit_Resource_Menu = ContextualMenu(Unit_Resource)
    menuMaster.addMenu(Unit, Gold, Unit_Resource_Menu)
    
    None_Unit_Menu = ContextualMenu(None_Unit)
    menuMaster.addMenu(None, Unit, None_Unit_Menu)
    
    TestTownCenter_WayPoint_Menu = ContextualMenu(TestTownCenter_WayPoint)
    menuMaster.addMenu(TestTownCenter,WayPoint,TestTownCenter_WayPoint_Menu)
    
    Unit_Unit_Menu = ContextualMenu(Unit_Unit)
    menuMaster.addMenu(Unit,Unit,Unit_Unit_Menu)
    
    return menuMaster

#### END CUSTOM DEFINED MENU FUNCTIONS HERE ####

if __name__=="__main__":
    
    class A(): pass
    class B(): pass

    mtestmaster = ContextualMenuMaster()
    
    mtest = ContextualMenu(lambda obj1,obj2: 'It worked')
    
    mtestmaster.addMenu(A,B,mtest)
    mtestmaster.addMenu(A,A,mtest)

    t1 = [A(),A(),B()]
    t3 = [None,B(),B()]
    t2 = B()
    
    print mtestmaster.getMenu(t1,t2)
    print mtestmaster.getMenu(t3,t2)
    
    getCGDcontextualMenu()
