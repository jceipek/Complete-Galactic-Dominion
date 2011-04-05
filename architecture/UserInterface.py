from Listener import Listener
import Event

class UserInterface(Listener):  #SHOULD PROBABLY INHERIT FROM DRAWABLE OBJECT
    """
    Contains all of the functionality required to present information screens to 
    the user and interprets user input.
    
    @param activeOverlay: activeOverlay = current screen to display over game 
    content (i.e. pause menu)
    
    @param activeWorld: The world that is currently enabled. It matches the 
    active world in the L{Universe}
    @type activeWorld: L{World}
    
    @param activeScreen: visible screen (i.e. loading, main menu, intro, 
    credits, etc.)
    @type activeScreen: L{Screen} or subclass thereof
    
    @param debugOverlay: An additional overlay disabled by default during real games. It displays the framerate and may eventually be used for 
    cheatcodes/displaying debug events. Only fps is currently enabled.
    """
    
    def __init__(self,manager,world):
        eventTypes = [ Event.RenderEvent, Event.MouseMovedEvent, Event.SelectionEvent, Event.SingleAddSelectionEvent, Event.UpdateEvent, Event.WorldChangeEvent, Event.DisplaySurfaceCreatedEvent, Event.SetDestinationEvent]
        Listener.__init__(self,manager,eventTypes)
        self.activeOverlay = None
        self.activeWorld = world
        self.activeScreen = None
        self.debugOverlay = None
        self.TEST_interface()
        #DO MORE SETUP STUFF
        
    def TEST_interface(self):
        from Screen import MainScreen
        from Overlay import DebugOverlay
        testScreen = MainScreen()
        testScreen.TEST_createViewport(self.activeWorld)
        self.activeScreen = testScreen
        self.debugOverlay = DebugOverlay()

    def setDisplaySurface(self,display,res):
        self.displaySurface=display
        self.resolution=res
        
    def notify(self,event):
        if isinstance(event, Event.RenderEvent):
            if self.activeScreen:
                self.activeScreen.draw(self.displaySurface,self.resolution)
            if self.debugOverlay:
                self.debugOverlay.draw(self.displaySurface,self.resolution)
        elif isinstance(event, Event.SelectionEvent):
            if self.activeScreen:
                self.activeScreen.processMouseClickEvent(event)
        elif isinstance(event, Event.SingleAddSelectionEvent):
            if self.activeScreen:
                self.activeScreen.processMouseClickEvent(event)            
        elif isinstance(event, Event.MouseMovedEvent):
            if self.activeScreen: 
                self.activeScreen.processMouseMovedEvent(event)
        #elif isinstance(event, Event.DragSelectionEvent):
        #    self.activeScreen.processDragSelectionEvent(event)
        #elif isinstance(event, Event.DragReleaseEvent):
        #    self.activeScreen.processDragReleaseEvent(event)
        elif isinstance(event, Event.UpdateEvent):
            if self.activeScreen:
                self.activeScreen.processUpdateEvent(event)
            if self.debugOverlay:
                self.debugOverlay.processUpdateEvent(event)
            self.manager.post(Event.RefreshEvent())
        elif isinstance(event, Event.WorldChangeEvent):
            if self.activeWorld:
                self.activeWorld = event.world
            if self.activeScreen:
                self.activeScreen.changeWorld(event.world)
        elif isinstance(event,Event.DisplaySurfaceCreatedEvent):
            self.setDisplaySurface(event.displaySurface, event.resolution)
