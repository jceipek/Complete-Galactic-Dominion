from Listener import Listener
import Event

class UserInterface(Listener):  #SHOULD PROBABLY INHERIT FROM DRAWABLE OBJECT
    """
    Contains all of the functionality required to present information screens to 
    the user and interprets user input.
    
    #Attributes:
    #   activeScreen = visible screen (i.e. loading, main menu, intro, credits,
                                                                          etc.)
    #   activeOverlay = current screen to display over game content (i.e. pause 
                                                                           menu)
    """
    
    def __init__(self,manager):
        eventTypes = [ Event.RenderEvent, Event.MouseMovedEvent, Event.UpdateEvent ]
        Listener.__init__(self,manager,eventTypes)
        self.activeOverlay = None
        self.activeWorld = None
        self.activeScreen = None
        #DO MORE SETUP STUFF

    def TEST_interfaceWithWorld(self,world):
		# STUB ###############
        self.loadWorld(world)
        
    def TEST_interface(self):
        from Screen import MainScreen
        testScreen = MainScreen()
        testScreen.TEST_createViewport()
        self.activeScreen = testScreen
        
    def notify(self,event):
        if isinstance( event, Event.RenderEvent ):
            self.activeScreen.draw(event.displaySurface,event.screenSize)
        elif isinstance( event, Event.MouseMovedEvent ):
            self.activeScreen.processMouseMovedEvent(event)
        elif isinstance( event, Event.UpdateEvent ):
            self.activeScreen.processUpdateEvent(event)
