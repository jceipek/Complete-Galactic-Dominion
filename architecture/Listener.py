class Listener(object):
    """
    A Listener waits for events sent out by the
    manager to which it is registered.
    
    #Attributes:
    #   manager = event manager to which the listener is registered
    """

    def __init__(self, manager):
        self.manager = manager
        self.manager.registerListener(self)

    def notify(self, event):
        #Each type of listener will override this method
        pass


"""PRETTY SURE THAT THIS IS NO LONGER NEEDED
class PygameListener(Listener):
    \"""
    Convert Pygame events into processable events we define.
    This is useful because it allows us to ignore all unused
    pygame events and standardize events.
    \"""
    def notify(self, pygameEvent):
        import pygame
        #NOT YET FULLY IMPLEMENTED - more events needed
        realEvent = None
        if event.type == pygame.QUIT:
            realEvent = None #SET UP PROPER EVENT HERE
        
        if realEvent:
            self.manager.post(realEvent)
#"""

"""THIS WILL ONLY BE NEEDED ONCE COMPLEXITY INCREASES
class QuitListener(Listener):
    \"""
    Waits for a program close request and tells everyone else to comply.
    \"""
    def notify(self, event):
        #NOT YET FULLY IMPLEMENTED
        #This method will eventually need to tell everything else to close, too
        
        #close the window
        pass
#"""