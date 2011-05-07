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
import threading, traceback, time

#Import necessary user defined classes required for the client
import Event, networking
from Manager import Manager
from Window import Window
from Grid import InfiniteGrid
from Debugger import Debugger
from Event import EventTimer
from World import World
from UserInterface import UserInterface
from Universe import Universe
from Entity import Entity,TestEntity
from Structure import TestTownCenter
from Unit import Unit,TestUnit
from gameClient import GameClient
from WorldManipulator import WorldManipulator
#from NaturalObject import Gold

def init(host='localhost'):
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
    Entity.manager = eventManager

    #Create the occurence manager for high-level events (same across client and server)
    #FIXME: NOT YET IMPLEMENTED

    #THIS WILL BE CHANGED LATER TO ACCOUNT FOR LOADING, ETC.

    networked = True

    # World w is set to the activeWorld of the universe
    universe = Universe(eventManager)
    ui = UserInterface(eventManager,universe.activeWorld,None)

    gameWindow = Window(eventManager,width=1024,height=768)
    gameWindow.fullscreenMode = False
    gameWindow.updateScreenMode()

    w = World(universe)
    #universe.changeWorld(w)

    try:
        client = GameClient(eventManager,host=host,port=1567)
        while client.ID == None:
            import time
            time.sleep(.02)
        print 'Got an ID',client.ID
        clientID = client.ID
    #    client.sendRequest('GetWorld')

    except:
        networked = False

    if not networked:
        # Initialize 25 entities in World w
        # Initialize a TestTownCenter
        clientID = GameClient.ID = 0
        ui.setClientID(clientID)
        eventManager.post(Event.NewPlayerEvent(clientID))
        w._generateResources()
    else:
        clientID = client.ID
        ui.setClientID(clientID)

    wManipulator = WorldManipulator(eventManager,w,networked,gameClientID = clientID)

    #Notify the manager that the window should start to accept input:
    eventManager.post(Event.StartEvent())

    return eventManager.eventTypesToListeners

if __name__ == '__main__':
    #FIXME: Very little implemented here.
    #Connect to server

    eTypestoListeners = init('10.41.24.200')
