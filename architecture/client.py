######################
#       Client       #
######################

#Import python modules required for the client
import threading

#Import necessary user defined classes required for the client
import Event
from Manager import Manager
from Window import Window
from Grid import InfiniteGrid,FiniteGrid
from Debugger import Debugger
from Renderer import Renderer
from Event import EventTimer
from World import World
from Mouse import Mouse
from UserInterface import UserInterface
from Universe import Universe

def init():
    """
    Game initialization function.
    """

    debugger = Debugger()
    eventTimer = EventTimer()
    
    #Create the event manager for low-level events
    eventManager = Manager(eventTimer,debugger) #more specific manager classes will be needed later
    
    #Create the occurence manager for high-level events (same across client and server)
    #NOT YET IMPLEMENTED
    
    #Create and register the standard listeners
    #NOT YET FULLY IMPLEMENTED
    
    #THIS WILL BE CHANGED LATER TO ACCOUNT FOR LOADING, ETC.

    universe = Universe(eventManager)
    ui = UserInterface(eventManager)
    ui.TEST_interface()
    
    #renderer = Renderer(eventManager)

    #clippingArea=area that should be drawn to
    gameWindow = Window(eventManager)
    
    #Notify the manager that the window should start to accept input:
    eventManager.post(Event.StartEvent())
    
    # returns reference to dictionary of the eventManager mapping
    # event types to a list of associated listeners
    return eventManager.eventTypesToListeners

if __name__ == '__main__':
    #Connect to server
    ldict = init()
    for key in ldict:
        listeners = ldict[key]
        print key, ' with %d listener(s):'%len(listeners)
        print '\t', listeners, '\n'
