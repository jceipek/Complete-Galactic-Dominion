######################\n
#       Server       #\n
######################\n

#import code necessary to run the server
#built-in modules
import threading, cPickle, traceback
#developer defined modules
import Event, networking
from networking import SocketThread
from Manager import Manager
from Window import Window
from Grid import InfiniteGrid,FiniteGrid
from Debugger import Debugger
from Event import EventTimer
from World import World
from UserInterface import UserInterface
from Universe import Universe
from Entity import Entity,TestEntity
from Unit import Unit,TestUnit
from Structure import Structure, TestTownCenter
from gameClient import GameClient
from WorldManipulator import WorldManipulator
from NaturalObject import NaturalObject,Gold
from client import init


class BroadcastServer(networking.Server):
    """
    Extends the Server class in the networking module.
    This server takes requests from a client and does one of two things
    -If the client is new
    """
    numberOfClients = 0
    
    def processInput(self,sockThrd,data):
        if 'GetWorld' in data: #and hasattr(self,'world'):
            print 'Loading the world to %s' % str(sockThrd.ID),
            numEntities = 0
            for entity in self.world.allEntities.values():
                sockThrd.write(cPickle.dumps(entity))
                numEntities = max(numEntities,entity.entityID)
            sockThrd.write('finishedLoading:%d:%s' % (self.world.universe.creator.numberOfEntities,str(self.world.universe.creator.releasedEntityIDs)))
            print 'Done loading to %s' % str(sockThrd.ID),
        else:
            for sock in self.socketThreads.keys():
                sock.write(data)
                
    def listenAndConnect(self,numPendingConnections=5):
        
        def connectToAllClients():
            while self.connecting:
                try:
                    clientSocket,clientAddress=self.socket.accept()
                except KeyboardInterrupt:
                    raise
                except:
                    traceback.print_exc()
                    continue
                print 'Connection Established'
                s=SocketThread(self,clientSocket)
                self.socketThreads[s]=s.file
                ID=BroadcastServer.numberOfClients
                BroadcastServer.numberOfClients += 1
                s.write('ID:'+str(ID))
                s.ID = str(ID)

        self.socket.listen(numPendingConnections)
        self.connecting=True
        self.connectionThread=threading.Thread(target=connectToAllClients)
        self.connectionThread.start()#this is a non daemonic thread and will prevent the server from exiting
            
def init(host='localhost',server=None):
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

    # World w is set to the activeWorld of the universe
    universe = Universe(eventManager)
    ui = UserInterface(eventManager,universe.activeWorld,'BROADCASTSERVER')
    
    gameWindow = Window(eventManager,width=1024,height=768)
    gameWindow.fullscreenMode = False
    gameWindow.updateScreenMode()
    
    w = World(universe)
    s.world=w
    
    networked = True
    print "GameClient"
    client = GameClient(eventManager,host=host,port=1567)
    while client.ID == None:
        import time
        time.sleep(.02)
    print 'Got an ID',client.ID
    clientID = client.ID

    ui.setClientID(clientID)
    
    wManipulator = WorldManipulator(eventManager,w,networked,gameClientID = clientID)
    #universe.changeWorld(w)
    
    #===========================================
    w._generateResources()
    """
    for i in xrange(25):
        TestUnit(i*50,i*50,w,clientID)
        
    from random import randint,choice
    xpos = randint(0,w.gridDim[0])
    ypos = randint(0,w.gridDim[1])
    TestTownCenter(xpos,ypos,w,clientID)
    """
    
    #Notify the manager that the window should start to accept input:
    eventManager.post(Event.StartEvent())
    
    return eventManager.eventTypesToListeners

if __name__ == '__main__':
    #FIXME: Very little implemented here.
    #Connect to server
    
    import sys

    theHost = 'localhost'
    if (len(sys.argv) == 2):
        theHost = sys.argv[1]
    elif len(sys.argv) > 2:
        print "Usage: python broadcastServer.py ipAddress"
        print "Reverting to localhost..."
        theHost = 'localhost'
    
    s = BroadcastServer(port = 1567, host = theHost)
    s.listenAndConnect()
    
    init(server=s)

    
    
