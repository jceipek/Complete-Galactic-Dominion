######################
#       Client       #
######################

#Import python modules required for the client
import threading

#Import necessary user defined classes required for the client
import Listener
from Manager import Manager
from Window import Window

def init():
    """
    Game initialization function.
    """
    
    #Create the event manager for low-level events
    eventManager = Manager() #more specific manager class will be needed later
    
    #Create the occurence manager for high-level events (same across client and server)
    #NOT YET IMPLEMENTED
    
    #Create and register the standard listeners
    #NOT YET FULLY IMPLEMENTED
    gameWindow = Window(eventManager)
    
    #Start the game loop
    gameWindow.run()

if __name__ == '__main__':
    #Connect to server
   init()
