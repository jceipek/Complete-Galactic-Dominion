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

def init():
    """
    Game initialization function.
    """

    debugger = Debugger()
    
    #Create the event manager for low-level events

    eventManager = Manager(debugger) #more specific manager class will be needed later
    
    #Create the occurence manager for high-level events (same across client and server)
    #NOT YET IMPLEMENTED
    
    #Create and register the standard listeners
    #NOT YET FULLY IMPLEMENTED

    #grid = InfiniteGrid(eventManager,(100,100),64)
    grid = FiniteGrid(eventManager,(3,2),64)
    
    renderer = Renderer(eventManager)
    
    gameWindow = Window(eventManager)
    
    #Notify the manager that the window should start to accept input:
    eventManager.post(Event.StartEvent())

if __name__ == '__main__':
    #Connect to server
   init()
