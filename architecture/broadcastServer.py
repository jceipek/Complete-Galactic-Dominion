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
from Grid import InfiniteGrid
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
    This server manages connections with the client.
    It takes requests from a client and does one of two things:
    -If the client sends the 'GetWorld' request it will send that client
        the current game state
    -If the client sends another request it will broadcast that request
        to all of the clients that have made a connection
        
    @param numberOfClients: tracks the number of clients that have connected to the server, used to assign client IDs
    @type numberOfClients: int
    
    @param socket: the socket that listens for connections from the clients
    @type socket: socket
    
    @param connecting: a flag to indicate if the server is currently accepting connections from the client
    @type connecting: bool
    
    @param connectionThread: the thread that manages the connections to clients
    @type connectionThread: Thread
    
    @param socketThreads: a dictionary of socketThread objects that map sockets to their file-like socket objects
    @type socketThreads: dict
    """
    numberOfClients = 0

    def processInput(self,sockThrd,data):
        """
        All requests to the server come through here.
        Manages sending the game state to new clients as well as 
        broadcasting requests from one client to all of the clients.
        Clients are responsible for being able to decrypt the messages
        that they send over the network.
        
        @param sockThrd: the socketThread object that the request originated from
        @type sockThrd: socketThread
        
        @param data: the string that was sent to the server from sockThrd
        @param data: string
        """
        
        #if the client is requesting the game state
        #   give it the game state
        if 'GetWorld' in data:
            print 'Loading the world to %s' % str(sockThrd.ID),
            numEntities = 0
            
            #iterate through all of the world's entities and send their
            #pickled state across the network
            for entity in self.world.allEntities.values():
                sockThrd.write(cPickle.dumps(entity))
                numEntities = max(numEntities,entity.entityID)
                
            #let the client know that the world is finished loading
            #this is important to prevent race conditions in client.py
            sockThrd.write('finishedLoading:%d:%s' % (self.world.universe.creator.numberOfEntities,str(self.world.universe.creator.releasedEntityIDs)))
            print 'Done loading to %s' % str(sockThrd.ID),
            
        #if the client is making another request
        #   broadcast the request to all of the clients
        else:
            for sock in self.socketThreads.keys():
                sock.write(data)

    def listenAndConnect(self,numPendingConnections=5):
        """
        This is the method that starts the connectionThread and should
        be called when the broadcast server is ready to wait for input
        from the network.
        NOTE: This will start a non-daemonic thread that will prevent
        the program from exiting. This is often a desirable behavior for
        servers.
        
        @param numPendingConnections: This specifies the number of clients that can be waiting for a connection at one time. The default is 5 on most operating systems.
        @type numPendingConnections: int
        """
        
        def connectToAllClients():
            """
            The server's connectionThread will run in this method.
            This is a non-daemonic thread and will prevent the program from exiting
            """
            while self.connecting:
                try:
                    clientSocket,clientAddress=self.socket.accept()
                except KeyboardInterrupt:
                    raise
                except:
                    traceback.print_exc()
                    continue
                print 'Connection Established'
                
                #create a new SocketThread object and add it to the socketThreads dictionary
                s=SocketThread(self,clientSocket)
                self.socketThreads[s]=s.file
                
                #assign the client an ID and notify it of this ID
                ID=BroadcastServer.numberOfClients
                BroadcastServer.numberOfClients += 1
                s.write('ID:'+str(ID))
                s.ID = str(ID)

        #make the server socket available for connection
        self.socket.listen(numPendingConnections)
        self.connecting=True
        self.connectionThread=threading.Thread(target=connectToAllClients)
        self.connectionThread.start()#this is a non daemonic thread and will prevent the server from 

def init(host='localhost',server=None):
    """
    Most of this code is copied from init() function in client.py
    
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
    
    #Creates a Debugger that posts events to the terminal for debugging purposes
    debugger = Debugger()
    eventTimer = EventTimer()
    
    #Create the event manager for low-level events
    eventManager = Manager(eventTimer,debugger) #FIXME: more specific manager\
    Entity.manager = eventManager    

    # World w is set to the activeWorld of the universe
    universe = Universe(eventManager)
    ui = UserInterface(eventManager,universe.activeWorld,'BROADCASTSERVER')

    gameWindow = Window(eventManager,width=1024,height=768)
    gameWindow.fullscreenMode = False
    gameWindow.updateScreenMode()

    w = World(universe)
    s.world=w

    networked = True
    client = GameClient(eventManager,host=s.host,port=1567)

	#wait until the client is assigned an ID before proceeding
    while client.ID == None:
        import time
        time.sleep(.02)
    print 'Got an ID',client.ID
    clientID = client.ID

    ui.setClientID(clientID)

    wManipulator = WorldManipulator(eventManager,w,networked,gameClientID = clientID)
    
    #generate the resources in the server, the existance of these
    #resources will propogate through to every client when they connect
    w._generateResources()
    
    #Notify the manager that the window should start to accept input:
    eventManager.post(Event.StartEvent())

    return eventManager.eventTypesToListeners

if __name__ == '__main__':
    #FIXME: Very little implemented here.
    #Connect to server
    s = BroadcastServer(port = 1567, host = '192.168.50.74')
    s.listenAndConnect()

    init(server=s)



