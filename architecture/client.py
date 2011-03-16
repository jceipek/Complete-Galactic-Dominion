######################
#       Client       #
######################

#Import python modules required for the client
import threading

#Import necessary user defined classes required for the client
import Window

def init():
    """
    Game initialization function.
    """
    
    #Create the drawing window
    gameWindow = Window.Window()
    
    #Create the event manager for low-level events
    #NOT YET IMPLEMENTED
    
    #Create the occurence manager for high-level events
    #NOT YET IMPLEMENTED
    
    #Create and register the listeners
    #NOT YET IMPLEMENTED
    
    #Start the game loop
    gameWindow.run()

if __name__ == '__main__':
    #Connect to server
   init()
