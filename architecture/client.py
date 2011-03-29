"""
B{RUN ME FIRST!}

######################\n
#       Client       #\n
######################\n
This file is used to set up everything that clients can do and begins the 
program.

B{FIXME:}We might want to move some of this code into a function that sets up 
servers and clients as needed. For now, no servers have been created.
"""

#Import python modules required for the client
import threading

#Import necessary user defined classes required for the client
import Event
from Manager import Manager
from Window import Window
from Grid import InfiniteGrid,FiniteGrid
from Debugger import Debugger
from Event import EventTimer
from World import World
from UserInterface import UserInterface
from Universe import Universe
from Entity import Entity,TestEntity
from Unit import Unit

def init():
    """
    Game initialization function.
        1. Creates a L{Debugger} (debugger) and L{EventTimer} (eventTimer) and 
           stores references to them in an instance of L{EventManager}.
        2. Several listeners are started and registered with eventManager:
            - Instance of L{Universe} (universe)
            - Instance of L{UserInterface} (ui)
            - Instance of L{Window} (gameWindow)
        3. We send the eventManager a message to start the game
            - This message is interpreted by the gameWindow
    """

    debugger = Debugger()
    eventTimer = EventTimer()
    
    #Create the event manager for low-level events
    eventManager = Manager(eventTimer,debugger) #FIXME: more specific manager\
                                                #classes will be needed later?
                                                
    #Create the occurence manager for high-level events (same across client and server)
    #FIXME: NOT YET IMPLEMENTED
    #Note: Do we even need this anymore? - Julian
    #Response: I don't think so.  - Jared
    
    #===========================================
    #Create and register the standard listeners
    #With the event manager
    #===========================================
    #FIXME: Not yet fully implemented
    
    #THIS WILL BE CHANGED LATER TO ACCOUNT FOR LOADING, ETC.

    # World w is set to the activeWorld of the universe
    universe = Universe(eventManager)
    ui = UserInterface(eventManager,universe.activeWorld)
    
    gameWindow = Window(eventManager,width=1024,height=768)
    
    w = World()
    universe.changeWorld(w)
    
    #===========================================
    
    # Initialize 500 entities in World w
    for i in range(6):
        #w.addEntity(Entity('ball.png',i*50,i*50, w, (255,255,255)))
        #w.addEntity(TestEntity('testBuilding.png', i*50, i*50, w, 'alpha'))
        w.addEntity(TestEntity('testCraft.png',i*50,i*50,w,'alpha'))

    #Notify the manager that the window should start to accept input:
    eventManager.post(Event.StartEvent())
    
    return eventManager.eventTypesToListeners

if __name__ == '__main__':
    #FIXME: Very little implemented here.
    #Connect to server
    
    eTypestoListeners = init()
    for key in eTypestoListeners:
        print 'Event type: %s'%str(key)
        print eTypestoListeners[key],'\n'
