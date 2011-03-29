import Event
from Viewport import Viewport
from World import World

class Screen(object): #SHOULD PROBABLY INHERIT FROM DRAWABLE OBJECT
    """
    Contains all of the elements that might be shown on screen at once.
    This is an abstract class with child classes.
    
    #Attributes:
    #   active = bool #Useful for pausing the screen
    """
    
    def __init__(self):
        self.activate()

    def activate(self):
        self.active = True
        #Override for additional commands
        
    def deactivate(self):
        self.active = False
        #Override for additional commands
        
    def draw(self,displaySurface,screenSize):
        pass

    def processMouseClickEvent(self,event):
        pass

class MainScreen(Screen):
    """
    The screen where all of the action takes place.
    It consists of a viewport and a HUD
    
    #Attributes:
    @param viewport: A window into the active world.
    @type viewport: L{Viewport}
    
    @param hud: The HUD displays information to the player. It does not contain 
    a debug menu, but does contain resource counts, menus, etc...
    @type hud: L{HUD}
    """
    def __init__(self):
        Screen.__init__(self)
        self.viewport = None
        self.hud = None
        
    def TEST_createViewport(self,world):
        ###FIXME
        #world.TEST_createGrid()
        scrollLoc = (0,0)
        viewportPos = (0,0)
        #viewportSize = (640,480)
        viewportSize = (1024,768-100)
        testViewport = Viewport(world,scrollLoc,viewportPos,viewportSize)
        self.viewport = testViewport
        
    def draw(self,displaySurface,size):
        self.viewport.draw(displaySurface)
        #self.viewport.drawContainedEntities()
        
    def processMouseMovedEvent(self,event):
        self.viewport.setScrollSpeed(event.pos)

    def processMouseClickEvent(self,event):
        self.viewport.clickEvent(event)

    def processUpdateEvent(self,event):
        self.viewport.processUpdateEvent(event)
        
    def changeWorld(self,world):
        self.viewport.changeWorld(world)
