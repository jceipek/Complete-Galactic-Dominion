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
import Event, networking
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
from gameClient import GameClient
from WorldManipulator import WorldManipulator
from client import init

if __name__ == '__main__':
    #FIXME: Very little implemented here.
    #Connect to server
    s = networking.BroadcastServer(port = 1567, host = 'localhost')
    s.listenAndConnect()
    eTypestoListeners = init()
    for key in eTypestoListeners:
        print 'Event type: %s'%str(key)
        print eTypestoListeners[key],'\n'

    
    
