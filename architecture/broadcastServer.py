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
from Structure import Structure
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
            for entity in self.world.allEntities.values():
                if isinstance(entity,Unit) or isinstance(entity,Structure) or isinstance(entity,NaturalObject):
                    sockThrd.write(cPickle.dumps(entity))
            sockThrd.write('finishedLoading')
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
    try:                                            
        client = GameClient(eventManager,host='127.0.0.1',port=1567)
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
    #universe.changeWorld(w)
    
    #===========================================
    
    w._generateResources()

    #Notify the manager that the window should start to accept input:
    eventManager.post(Event.StartEvent())
    
    return eventManager.eventTypesToListeners

if __name__ == '__main__':
    #FIXME: Very little implemented here.
    #Connect to server
    s = BroadcastServer(port = 1567, host = 'localhost')
    s.listenAndConnect()
    
    init(server=s)

    
    
