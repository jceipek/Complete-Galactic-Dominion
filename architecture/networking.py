####################\n
#    networking    #\n
####################\n

"""
This is a simple networking module that employs sockets directly. It is
the Client and Server classes are designed to be overwritten very
easily, this file includes some examples of these
"""

#import the necessary modules
import socket, sys, traceback, threading
from threading import *

class NetworkEntity(object):
    """
    The base class for Servers and Clients.
        Defines basic properties of entities on the network.
           
    @param host: the ip address of the entity's main socket
    @type host: string
    
    @param port: the port that the main socket is listening on
    @type port: int
    """
    
    '''
    Define the delimiter that indicates when a single message
        terminates. This is similar to the telegraph STOP message
    Define the delimiter that indicates when a connection is to be
        broken.
    '''
    STOP_MESSAGE='the_end_is_near'
    CLOSE_MESSAGE='shut_it_down'
    
    def __init__(self,host,port):
        """
        Initialize the network entity
        
        @param host: the ip address of the host server
        @type host: string
        
        @param port: the port that the NetworkEntity will be listening on
        @type port: int, string
        """
        self.host=host
        
        #test if the port is convertable into an integer
        try:
            self.port=int(port)
            
        #look up the port by its name. This allows the port to be set by
        #   its name e.g. 'http'
        except ValueError:
            try:
                self.port = socket.getservbyname(port,'tcp')
                
            #handle ports that could not be found
            except socket.error,e:
                print 'Couldn\'t find your port: %s' % e
                sys.exit(1)

    def processInput(self,sockThrd,data):
        """
        This method should be overwritten in all non=abstract subclasses
        of NetworkEntity.
        This method is designed to handle all of the data that comes
        across the network.
        
        @param sockThrd: the socket thread object that handles raw data from a socket
        @type sockThrd: SocketThread
        
        @param data: the string of data that can be sent across the network
        @type data: string
        """
        pass

    def removeSocketThread(self,sockThrd):
        """
        This method should be overwritten in all non=abstract subclasses
        of NetworkEntity.
        This method is designed to clean up any references to a
        SocketThread
        
        @param sockThrd: the SocketThread object that should be removed
        @type sockThrd: SocketThread
        """
        pass

class Server(NetworkEntity):
    """
    Inherits from NetworkEntity
    
    The base class for all Servers. This server by itself can accept
    connections from the network and accepts data from clients, but does
    nothing with this data.
    
    To make a non-trivial subclass of the Server the processInput method
    should be overwritten

    @param host: the ip address of the host server
    @type host: string
    
    @param port: the port that the Server will be listening on
    @type port: int, string
    
    @param socket: the socket that listens for connections from the clients
    @type socket: socket
    
    @param connecting: a flag to indicate if the server is currently accepting connections from the client
    @type connecting: bool
    
    @param connectionThread: the thread that manages the connections to clients
    @type connectionThread: Thread
    
    @param socketThreads: a dictionary of socketThread objects that map sockets to their file-like socket objects
    @type socketThreads: dict
    """
    def __init__(self,host='',port=51423):
        NetworkEntity.__init__(self,host,port)
        
        #specify TCP connection and other socker options
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        
        #initialize various instance variables
        self.connecting=False
        self.socketThreads=dict()
        self.connectionThread=None

        #connect the socket to the appropriate port
        self.socket.bind((self.host,self.port))

    def listenAndConnect(self,numPendingConnections=5):
        """
        This is the method that starts the connectionThread and should
        be called when the broadcast server is ready to wait for input
        from the network.
        NOTE: This will start a non-daemonic thread that will prevent
        the program from exiting. This is often a desirable behavior for
        servers.
        
        Generally this method should not be overwritten in Server's
        subclasses, because client connections cannot easily be
        intercepted. This may need to change in the future.
        
        If it is necessary to intercept client connections, 
        this code should be copied into the subclass's
        connectToAllClients method
        
        @param numPendingConnections: This specifies the number of clients that can be waiting for a connection at one time. The default is 5 on most operating systems.
        @type numPendingConnections: int
        """
        
        def connectToAllClients():
            """
            The server's connectionThread will run in this method.
            This is a non-daemonic thread and will prevent the program from exiting
            """
            while self.connecting:
                '''
                Exception handling here is very important, because
                errors connecting to one client should not crash the
                entire server
                '''
                try:
                    #accept clients that attempt to connect
                    clientSocket,clientAddress=self.socket.accept()
                except KeyboardInterrupt:
                    raise
                except:
                    traceback.print_exc()
                    continue
                print 'Connection Established'
                
                #create a corresponding SocketThread object and add it to the socketThreads dictionary
                s=SocketThread(self,clientSocket)
                self.socketThreads[s]=s.file
        
        #begin listening for connections
        self.socket.listen(numPendingConnections)
        self.connecting=True
        
        #manage connections in a different thread
        self.connectionThread=threading.Thread(target=connectToAllClients)
        self.connectionThread.start()#this is a non daemonic thread and will prevent the server from exiting

    def removeSocketThread(self,sockThrd):
        """
        Deletes the reference to the SocketThread from the socketThreads
        dictionary
        
        @param sockThrd: the SocketThread object that should be removed
        @type sockThrd: SocketThread
        """
        try:
            del(self.socketThreads[sockThrd])
        except:
            pass
        
    def __del__(self):
        """
        Deletes the Server
        """
        
        self.connecting=False
        try:
            del(self.socketThreads)
        except KeyboardInterrupt:
            raise
        except:
            traceback.print_exc()
        self.socket.close()
        

class Client(NetworkEntity):
    """
    Inherits from NetworkEntity
    
    The base class for all Clients.
    
    Client, unlike Server, has nontrivial behavior. It connects to a
    server and has the ability to send data to that server. It does not,
    however, respond to any data sent by the server.
    
    To respond to input from the client, overwrite the processInput
    method similarly to the Server class.

    @param host: the ip address of the host server
    @type host: string
    
    @param port: the port that the Client will be listening on
    @type port: int, string
    
    @param socket: the socket that listens to the server
    @type socket: socket
    
    @param socketThread: the SocketThread object that will handle communication across the network
    @type socketThread: SocketThread
    
    @param connected: a flag indicating whether or not the Client has connected to a server
    @type connected: bool
    """
    def __init__(self,host='localhost',port=51423):
        NetworkEntity.__init__(self,host,port)
        
        #specify TCP connection and catch appropriate exceptions
        try:
                self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        except socket.error, e:
                print 'Error creating socket %s' % e
                sys.exit(1)
                
        #connect to the server and catch appropriate exceptions
        try:
                self.socket.connect((self.host,self.port))
        except socket.gaierror, e:
                print 'Address error: %s' % e
                sys.exit(1)
        except socket.error, e:
                print 'Connection error: %s' % e
                sys.exit(1)
        
        self.connected=True
        self.socketThread=SocketThread(self,self.socket)

    def sendRequest(self,request):
        """
        Sends requests to the server
        
        @param request: the data that should be sent over the network
        @type request: string
        """
        self.socketThread.write(request)

    def removeSocketThread(self,sockThrd):
        """
        Deletes the reference to the SocketThread from the socketThreads
        dictionary
        
        @param sockThrd: the SocketThread object that should be removed
        @type sockThrd: SocketThread
        """
        self.socketThread=None
    
    def __del__(self):
        """
        Deletes the client
        """
        
        print 'Deleting Client'
        try:
            self.socketThread.__del__()
        except KeyboardInterrupt:
            raise
        except:
            traceback.print_exc()

            
class SocketThread(object):
    """
    A wrapper class for sockets. These sockets are managed in daemonic
    threads, and will terminate silently if all non-daemonic threads
    terminate
    
    @param parent: a reference to the object that created it
    @type parent: NetworkEntity
    
    @param thread: the thread that manages the socket
    @type thread: Thread
    
    @param socket: the socket that communicates across the network
    @type socket: socket
    
    @param file: the socket's file-like object, data can be written to and read from this object as if it were a file
    @type file: socket.file ???
    
    @param alive: a flag indicating whether or not the SocketThread is actively connected to the network
    @type alive: bool
    """
    
    def __init__(self,parent,sock):
        self.parent=parent
        
        #create the network manager thread in the processInput method of
        #the SocketThread
        self.thread=threading.Thread(target=self.processInput,args=())
        self.socket=sock
        self.file=self.socket.makefile('rw',0)
        self.alive=True
        self.thread.setDaemon(True)
        self.thread.start()
        
    def write(self,message):
        """
        Wraps the socket's write method, allowing endline characters to
        be included in the message. This happens by using
        NetworkEntity.STOP_MESSAGE as the delimiter to indicate the end
        of a message instead of an endline character
        
        @param message: the message to be sent over the network
        @type message: string
        """
        
        #write everything to the socket
        self.file.write(message+'\n')
        #end the message with the STOP_MESSAGE delimiter
        self.file.write(self.parent.STOP_MESSAGE+'\n')
        #ensure that the message is sent across the network
        self.file.flush()
        
    def processInput(self):
        """
        The method that the thread runs in.
        This will listen continuously to the network for information and
        post this information to the parent's processInput method
        """
        
        #run while the SocketThread is alive
        while self.alive:
            #initialize the line string
            line = ''
            
            #this is a flag that is used to find the end of the message
            flag=False
            
            #iterate through the lines in the file-like object
            for nline in self.file:
                flag=True
                #check to see if the message has ended
                if nline.strip() == self.parent.STOP_MESSAGE:
                    break
                #append the n(ext)line to the cumulative line
                line+=nline 
                
            #check for the CLOSE_MESSAGE
            if line.strip() == self.parent.CLOSE_MESSAGE or flag == False:
                self.__del__()
                return
                
            flag=False
            
            #send the data to the parent's processInput method
            self.parent.processInput(self,line)
            line=''
        
    def __del__(self):
        """
        Deletes the SocketThread and lets the network know that the
        SocketThread has been deleted
        """
        self.alive=False
        self.parent.removeSocketThread(self)
        
        #tell the entity on the other side of the network to delete the socket
        try:
            self.write(self.parent.CLOSE_MESSAGE)
        except:
            pass
            
        #close the network connection
        try:
            self.socket.close()
        except:
            pass

#########################\n
#    Server Examples    #\n
#########################\n
"""
Here are several examples of simple servers that inherit from the Server
class. When inheriting from Server these template should be followed.
"""

class PrintServer(Server):
    """
    A server that accepts data from the network and simply prints it to the
    local terminal
    """
    def processInput(self,sockThrd,data):
        #print the data to the terminal
        print data

class EchoServer(Server):
    """
    A server that accepts data from the network and echos the data back to
    the client that sent it
    """
    def processInput(self,sockThrd,data):
        #write the data back to the SocketThread that accepted it
        sockThrd.write(data)

class BroadcastServer(Server):
    """
    A server that accepts data from the network and broadcasts the data back
    to all of its clients
    """
    def processInput(self,sockThrd,data):
        #iterate through all of the SocketThread objects and write the
        #data to each of them
        for sock in self.socketThreads.keys():
            sock.write(data)

#########################\n
#    Client Examples    #\n
#########################\n
"""
Here are several examples of simple clients that inherit from the Client
class. When inheriting from Client there is more 
"""

class MessengerClient(Client):
    """
    """
    def __init__(self,message,host='localhost',port=51423):
        Client.__init__(self,host,port)
        print 'Sending message: %s' % message
        self.sendRequest(message)
        self.__del__()
