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

class MainScreen(Screen):
    """
    The screen where all of the action takes place.
    It consists of a viewport and a HUD
    
    #Attributes:
    #   viewport
    #   hud
    """
    def __init__(self):
        Screen.__init__(self)
        self.viewport = None
        self.hud = None
        
    def TEST_createViewport(self,world):
        ###FIXME
        #world.TEST_createGrid()
        scrollLoc = (0,0)
        viewportPos = (50,20)
        #viewportSize = (640,480)
        viewportSize = (500,300)
        testViewport = Viewport(world,scrollLoc,viewportPos,viewportSize)
        self.viewport = testViewport
        
    def draw(self,displaySurface,size):
        self.viewport.draw(displaySurface)
        #self.viewport.drawContainedEntities()
        
    def processMouseMovedEvent(self,event):
        #self.viewport.scrollBasedOnMousePos(event.pos)
        self.viewport.setScrollSpeed(event.pos)

    def processUpdateEvent(self,event):
        self.viewport.world.update()
        self.viewport.scrollBasedOnElapsedTime(event.elapsedTimeSinceLastFrame)
