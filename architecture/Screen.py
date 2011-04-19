import Event
from Viewport import Viewport
from HUD import HUD
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
        
    def TEST_createViewport(self,world,manager):
        ###FIXME
        #world.TEST_createGrid()
        scrollLoc = (0,0)
        viewportPos = (0,0)
        #viewportSize = (640,480)
        viewportSize = (1024,768-100)
        testViewport = Viewport(world,manager,scrollLoc,viewportPos,viewportSize)
        self.viewport = testViewport
        
        hudPos=(0, viewportSize[1]-20)
        hudSize=(viewportSize[0], 120)
        self.hud=HUD(hudPos, hudSize)
        self.viewport.hud=self.hud
        self.hud.viewport=self.viewport
        
    def draw(self,displaySurface,size):
        self.viewport.draw(displaySurface)
        self.hud.draw(displaySurface)
        
    def processMouseMovedEvent(self,event):
        self.viewport.mouseMoved(event)

    def processMouseClickEvent(self,event):
        self.viewport.clickEvent(event)
    
    def processDragBeganEvent(self,event):
        self.viewport.startDrag(event)
        
    def processDragEvent(self,event):
        self.viewport.continueDrag(event)
    
    def processDragCompletedEvent(self,event):
        self.viewport.completeDrag(event)

    def processAddDragCompletedEvent(self,event):
        self.viewport.completeDrag(event)

    def processNumberKeyPressEvent(self,event):
        if event.state == Event.KeyLocals.UP:
            if event.comboKeys['ctrl']:
                self.viewport.setQuickSelect(event)
            else:
                self.viewport.getQuickSelect(event)
    
    def processCompleteActionEvent(self,event):
        self.viewport.completeActionEvent(event)
        
    def processInitiateActionEvent(self,event):
        self.viewport.initiateActionEvent(event)
        
    def processUpdateEvent(self,event):
        self.viewport.processUpdateEvent(event)
        
    def changeWorld(self,world):
        self.viewport.changeWorld(world)
