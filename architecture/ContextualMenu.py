import radialMenu
from Callback import Callback, GroupCallback, SeriesCallback, ParallelCallback, networkClassCreator

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
        # Obj1 is normally a list
        
        # gets a list of lists of objects sorted by frequency of class
        if type(obj1) == list:
            sortedObjects = self._sortByClass(obj1)
        else:
            sortedObjects = [[obj1]]
            
        obj2Class = obj2.__class__
        
        for typeGroup in sortedObjects:
            curClass = typeGroup[0].__class__
            menu = self.menus.get((curClass,obj2Class),None)

            if menu is not None:
                return menu.getMenu(typeGroup,obj2)
                
        return None
            
    def _sortByClass(self,t):
        """
        Returns a list of lists of instances sorted by class.  The
        lists are ordered in the returned list by the length of the list.
        """
        d = {}
        
        for item in t:
            d.setdefault(item.__class__,[]).append(item)
        
        return self._mostCommonClass(d)
        
    def _mostCommonClass(self,d):
        """
        Receives a dictionary mapping classes to instances of the class,
        and returns a list of lists of instances sorted by these classes
        and ordered in the returned list by the length of the list.
        """
        mostCommonClass = []
        
        for key in d:
            mostCommonClass.append((len(d[key]),d[key]))
        mostCommonClass.sort(reverse=True)
        
        objList = []
        
        for number,objects in mostCommonClass:
            
            objList.append(objects)

        return objList
        
class ContextualMenu(object):
    
    def __init__(self,menuMakerFunction):
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
    """
    Object which defines a point in 2-D space.  It is meant to be
    used to represent a point in the internal Cartesian space of a
    World object in the game.
    """
    def __init__(self,x,y):
        object.__init__(self)
        
        self.x,self.y = x,y
    
    def getPoint(self):
        """
        Returns the point as a tuple.
        """
        return (self.x,self.y)

#### ENTER CUSTOM DEFINED MENU FUNCTIONS HERE ####

"""
Note: functions below of the form <class #1>_<class #2> create
contextual menus associated with the interaction between a group of
instances of class #1 acting on an instance of class #2.

See getCGDcontextualMenu() below for more information.
"""

from Structure import Structure,TestTownCenter
from Entity import Entity
from Unit import Unit,TestUnit, BuildTask
from NaturalObject import Gold
from GameData import Locals

from Event import NotificationEvent,WorldManipulationEvent

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
            if obj2._hasResourcesToBuild(buildType):
                curItem = radialMenu.RMenuItem(menu,
                    image = "orb.png",
                    col = (255,0,0),
                    title = 'Build Option #'+str(tmpcounter),
                    callback = Callback(obj2.addToBuildQueue,buildType))
                    #callback = self.buildDict[buildType])
                buildMenu.addItem(curItem)
                tmpcounter+=1
        if tmpcounter == 0:
            menu.removeItem(buildItem)

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
        #deposit resources
        gatherCallbacks = []
        for unit in obj1:
            #gatherCallbacks.append(unit.setStatusAndObjectOfAction)
            gatherCallbacks.append(unit.initAction)
        
        depositItem = radialMenu.RMenuItem(menu,
            image = "DepositOrb.png",
            col = (255,0,255),
            title = 'Deposit Resources',
            callback = GroupCallback(gatherCallbacks,obj2))
        menu.addItem(depositItem)
    
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
        
    showDesc = radialMenu.RMenuItem(menu,
        image = "orbQBlack.png",
        col = (255,0,255),
        title = 'Description',
        callback = Callback(obj2.showDescription))
    menu.addItem(showDesc)
        
    return menu
        
def Unit_WayPoint(obj1,obj2):
    
    # FIXME - DOES NOT CURRENTLY WORK WITH GROUPS
    
    menu = radialMenu.RMenu(openDelay=.2)

    #set destination of unit
    setDestCallbacks = []
    for unit in obj1:
        setDestCallbacks.append(unit.addToPath)
    
    setDestItem = radialMenu.RMenuItem(menu,
        image = "DestOrb.png",
        col = (255,255,255),
        title = 'Setting destination',
        callback = GroupCallback(setDestCallbacks,obj2.getPoint()))

    menu.addItem(setDestItem)

    #tells unit to build a structure
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
            if obj1[0]._hasResourcesToBuild(buildType):
                p=obj2.getPoint()
                buildTask=BuildTask(buildType, p,\
                            Callback(obj1[0].sendEventToManager,\
                            networkClassCreator(buildType,\
                            *obj1[0].getBuildArgs2(*p))))
                            
                #tells unit to build
                setBuildCallbacks=[]
                for unit in obj1:
                    setBuildCallbacks.append((unit.addToBuildQueue,[buildTask]))

                #subtracts cost of building from player's resources
                for resource,cost in buildType.costToBuild:
                    setBuildCallbacks.append((obj1[0].world.removeResource, (obj1[0].owner,resource,cost)))
                    
                func, args = setBuildCallbacks.pop()
                call=ParallelCallback(func, *args)
                for func, args in setBuildCallbacks:
                    call.addCallback(func, *args)
                             
                curItem = radialMenu.RMenuItem(menu,
                    image = "orb.png",
                    col = (255,0,0),
                    title = 'Build Option #'+str(tmpcounter),
                    callback = call)
                    
                buildMenu.addItem(curItem)
                tmpcounter+=1
        if tmpcounter == 0:
            menu.removeItem(buildItem)
    
    return menu
    
def Unit_Resource(obj1,obj2):
    
    menu = radialMenu.RMenu(openDelay=.2)
    #gathers resource
    setGatherCallbacks = []
    for unit in obj1:
        setGatherCallbacks.append(unit.initAction)
    
    gatherItem = radialMenu.RMenuItem(menu,
        image = "orbWhiteBlack.png",
        col = (255,255,255),
        title = 'Gathering',
        callback = GroupCallback(setGatherCallbacks,obj2))

    menu.addItem(gatherItem)
    
    showDesc = radialMenu.RMenuItem(menu,
        image = "orbQBlack.png",
        col = (255,0,255),
        title = 'Description',
        callback = Callback(obj2.showDescription))
    menu.addItem(showDesc)
        
    return menu
    
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
            if obj2._hasResourcesToBuild(buildType):
                curItem = radialMenu.RMenuItem(menu,
                    image = "orb.png",
                    col = (255,0,0),
                    title = 'Build Option #'+str(tmpcounter),
                    callback = Callback(obj2.addToBuildQueue,buildType,obj2.rect.center))
                buildMenu.addItem(curItem)
                tmpcounter+=1
        if tmpcounter == 0:
            menu.removeItem(buildItem)

    showDesc = radialMenu.RMenuItem(menu,
        image = "orbQBlack.png",
        col = (255,0,255),
        title = 'Description',
        callback = Callback(obj2.showDescription))
    menu.addItem(showDesc)

    return menu
    
def TestTownCenter_WayPoint(obj1,obj2):
    
    menu = radialMenu.RMenu(openDelay=.2)
    
    # FIXME - CAN ONLY ACCEPT 1 TESTTOWNCENTER
    
    if len(obj1[0].buildDict) > 0:
        
        buildItem = radialMenu.RMenuItem(menu,
            image = "RecruitOrb.png",
            col = (255,0,255),
            title = 'Build Options')
        
        menu.addItem(buildItem)
        
        buildMenu = radialMenu.RMenu()
        buildItem.addSubmenu(buildMenu)
        
        tmpcounter = 0
        p=obj2.getPoint()
        for buildType in obj1[0].buildDict:
            if obj1[0]._hasResourcesToBuild(buildType):
                makeAndMove = ParallelCallback(
                    obj1[0].sendEventToManager,
                    networkClassCreator(buildType,*obj1[0].getBuildArgs2())
                    )
                    
                #FIXME - Does not set path properly when many units created at once
                makeAndMove.addCallback(
                    obj1[0].world.universe.manager.post,
                    WorldManipulationEvent(['setpath',
                        obj1[0].world.universe.getNextEntityID(),p])
                    )

                for resource,cost in buildType.costToBuild:
                    makeAndMove.addCallback(obj1[0].world.removeResource, obj1[0].owner,resource,cost)

            
                queueMake = Callback(obj1[0].addToBuildQueue,
                    BuildTask(buildType,p,makeAndMove))
                
                curItem = radialMenu.RMenuItem(menu,
                    image = "orb.png",
                    col = (255,0,0),
                    title = 'Build Option #'+str(tmpcounter),
                    callback = queueMake)
                buildMenu.addItem(curItem)
                tmpcounter+=1
        if tmpcounter == 0:
            menu.removeItem(buildItem)
        
        # Has empty menu?
        if len(menu.root) > 0:    
            return menu
        else:
            return None 
    return None

def Unit_Unit(obj1,obj2):
    
    menu = radialMenu.RMenu(openDelay=.2)
    
    if obj1[0].owner!=obj2.owner:
    
        setAttackCallbacks = []
        for unit in obj1:
            setAttackCallbacks.append(unit.initAction)
        
        attackItem = radialMenu.RMenuItem(menu,
            image = "AttackOrb.png",
            col = (255,255,255),
            title = 'Attack!',
            callback = GroupCallback(setAttackCallbacks,obj2))
    
        menu.addItem(attackItem)
    
    showDesc = radialMenu.RMenuItem(menu,
        image = "orbQBlack.png",
        col = (255,0,255),
        title = 'Description',
        callback = Callback(obj2.showDescription))
    menu.addItem(showDesc)
        
    return menu

def getCGDcontextualMenu():
    """
    Defines all of the contextual menus for the CGD game.
    It returns a ContextualMenuMaster.

    ContextualMenuMaster has a getMenu method which takes a list of
    objects (#1) and a second, single object (#2) (a listed of selected objects
    and the object which has been clicked it).  The selected object list
    is sorted by class.  Starting with the most frequent class, if there
    is a defined interaction between that class and the class of the
    second object, the corresponding menu is returned.  If not,
    the next most frequent class is checked, and so on.  If there is
    no defined interaction, None is returned.

    The naming convention of custom-defined CGD functions above is of the
    form <Class of object #1>_<Class of object #2>

    ContextualMenus are made by passing these custom-defined CGD functions
    into the constructor.  _Menu is appended to the name.
    
    ContextualMenus are then added to a dictionary of contextual menus
    stored in the ContextualMenuMaster through the addMenu function.
    The class of objects #1 and the class of objects #1 which a 
    particular contextual menu can should respond to are passed as
    arguments.  These will be used to form a tuple (of length two)
    serving as a key to access the contextual menu.
    
    This function loads all of the contextual menus specific to CGD.
    """
    
    menuMaster = ContextualMenuMaster()
    
    Unit_TestTownCenter_Menu = ContextualMenu(Unit_TestTownCenter)
    menuMaster.addMenu(Unit,TestTownCenter,Unit_TestTownCenter_Menu)
    menuMaster.addMenu(TestUnit,TestTownCenter,Unit_TestTownCenter_Menu)
    
    None_TestTownCenter_Menu = ContextualMenu(None_TestTownCenter)
    menuMaster.addMenu(None,TestTownCenter,None_TestTownCenter_Menu)
    
    Unit_WayPoint_Menu = ContextualMenu(Unit_WayPoint)
    menuMaster.addMenu(Unit, WayPoint, Unit_WayPoint_Menu)
    menuMaster.addMenu(TestUnit, WayPoint, Unit_WayPoint_Menu)
    
    Unit_Resource_Menu = ContextualMenu(Unit_Resource)
    menuMaster.addMenu(Unit, Gold, Unit_Resource_Menu)
    menuMaster.addMenu(TestUnit, Gold, Unit_Resource_Menu)
    
    None_Unit_Menu = ContextualMenu(None_Unit)
    menuMaster.addMenu(None, Unit, None_Unit_Menu)
    menuMaster.addMenu(None, TestUnit, None_Unit_Menu)
    
    TestTownCenter_WayPoint_Menu = ContextualMenu(TestTownCenter_WayPoint)
    menuMaster.addMenu(TestTownCenter,WayPoint,TestTownCenter_WayPoint_Menu)
    
    Unit_Unit_Menu = ContextualMenu(Unit_Unit)
    menuMaster.addMenu(Unit,Unit,Unit_Unit_Menu)
    menuMaster.addMenu(TestUnit,TestUnit,Unit_Unit_Menu)
    
    return menuMaster

#### END CUSTOM DEFINED MENU FUNCTIONS HERE ####
