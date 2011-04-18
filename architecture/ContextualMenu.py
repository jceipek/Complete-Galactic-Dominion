import radialMenu

class ContextualMenuMaster(object):
    
    def __init__(self):
        object.__init__(self)
        
        self.menus = {}
        self.setupMenus()
        
    def setupMenus(self):
        """
        Adds menus using addMenu method
        """
        pass
        
    def addMenu(self,obj1Class,obj2Class,menu):
        self.menus[(obj1Class,obj2Class)] = menu
        
    def getMenu(self,obj1,obj2):
        """
        Returns context specific menu
        """
        # Obj1 is a list
        if isinstance(obj1,list) and not obj1 == []:
            obj1 = self._sortByClass(obj1)
            obj1Class = obj1[0].__class__
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
            if len(mostCommonClass) < d[key]:
                mostCommonClass = d[key]
        
        return mostCommonClass
        
class ContextualMenu(object):
    
    def __init__(self,menuMakerFunction = lambda obj1,obj2: None):
        object.__init__(self)
        
        self._menuMakerFunction = menuMakerFunction
        
    def getMenu(self,obj1,obj2):
        return self._menuMakerFunction(obj1,obj2)

#### ENTER CUSTOM DEFINED MENU FUNCTIONS HERE ####

def None_TestTownCenter(obj1,obj2):
    
    menu = radialMenu.RMenu(openDelay=.5)

    if len(self.buildDict) > 0:
        
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
                callback = Callback(obj2.addToBuildQueue,Unit))
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
    
    menu = radialMenu.RMenu(openDelay=.5)
    
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
            attackCallbacks.append(unit.initAction(obj2))
    
        attackBuilding = radialMenu.RMenuItem(menu,
            image = "AttackOrb.png",
            col = (255,0,0),
            title = 'Attack!',
            callback = GroupCallback(attackCallbacks))
        
        menu.addItem(attackBuilding)
        
        return menu
    
def getCGDcontextualMenu():
    
    from Structure import Structure,TestTownCenter
    from Entity import Entity
    from Unit import Unit
    
    menuMaster = ContextualMenuMaster()
    
    Unit_TestTownCenter_Menu = ContextualMenu(Unit_TestTownCenter)
    menuMaster.addMenu(None,TestTownCenter,Unit_TestTownCenter_Menu)
    
    None_TestTownCenter_Menu = ContextualMenu(None_TestTownCenter)
    menuMaster.addMenu(None,TestTownCenter,None_TestTownCenter_Menu)
    
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
    
