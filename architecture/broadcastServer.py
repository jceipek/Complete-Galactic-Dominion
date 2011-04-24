######################\n
#       Server       #\n
######################\n

#import code necessary to run the server
#built-in modules
import threading, cPickle
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
    numberOfEntities = 0
    
    def processInput(self,sockThrd,data):
        print 'Got input:' + data
        if 'GetWorld' in data and hasattr(self,'world'):
            for entity in self.world.allEntities.values():
                if isinstance(entity,Unit) or isinstance(entity,Structure) or isinstance(entity,NaturalObject):
                    sockThrd.write(cPickle.dumps(entity))
            sockThrd.write('finishedLoading')
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
                ID=BroadcastServer.numberOfEntities
                s.write('ID:'+str(ID))
                BroadcastServer.numberOfEntities += 1
                self.processInput(s,'GetWorld')
                self.processInput(s,'newPlayer:%d'%ID)

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
    
    networked = True
    try:                                            
        client = GameClient(eventManager,host=host,port=1567)
    #    client.sendRequest('GetWorld')
    except:
        networked = False
                                               
    #Create the occurence manager for high-level events (same across client and server)
    #FIXME: NOT YET IMPLEMENTED
    
    #THIS WILL BE CHANGED LATER TO ACCOUNT FOR LOADING, ETC.

    # World w is set to the activeWorld of the universe
    universe = Universe(eventManager)
    ui = UserInterface(eventManager,universe.activeWorld)
    
    gameWindow = Window(eventManager,width=1024,height=768)
    gameWindow.fullscreenMode = False
    gameWindow.updateScreenMode()
    
    w = World(universe)
    server.world=w
    wManipulator = WorldManipulator(eventManager,w,networked)
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
    #eTypestoListeners = init()
    #for key in eTypestoListeners:
    #    print 'Event type: %s'%str(key)
    #    print eTypestoListeners[key],'\n'

    
    
