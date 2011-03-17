import socket, sys, traceback, threading
from threading import *

class NetworkEntity(object):
    
    STOP_MESSAGE='the_end_is_near'
    CLOSE_MESSAGE='shut_it_down'
    
    def __init__(self,host,port):
        self.host=host
        try:
            self.port=int(port)
        except ValueError:
            try:
                self.port = socket.getservbyname(port,'tcp')
            except socket.error,e:
                print 'Couldn\'t find your port: %s' % e
                sys.exit(1)

    def processInput(sockThrd,data):
        pass#this should be overwritten in all non-abstract subclasses of NetworkEntity

    def removeSocketThread(sockThrd):
        pass#clean up any references to the appropriate socket thread

class Server(NetworkEntity):
    def __init__(self,host='',port=51423):
        NetworkEntity.__init__(self,host,port)
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.connecting=False
        self.socketThreads=dict()
        self.connectionThread=None

        self.socket.bind((self.host,self.port))

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
                s=SocketThread(self,clientSocket)
                self.socketThreads[s]=s.file

        self.socket.listen(numPendingConnections)
        self.connecting=True
        self.connectionThread=threading.Thread(target=connectToAllClients)
        self.connectionThread.start()

    def removeSocketThread(self,sockThrd):
        del self.socketThreads[sockThrd]
        
    def __del__(self):
        self.connecting=False
        for sock in self.socketThreads:
            try:
                del sock
            except KeyboardInterrupt:
                raise
            except:
                traceback.print_exc()
        self.socket.close()

class PrintServer(Server):
    def processInput(sockThrd,data):
        print data

class EchoServer(Server):
    def processInput(sockThrd,data):
        sockThrd.write(data)

class BroadcastServer(Server):
    def processInput(sockThrd,data):
        for sock in self.socketThreads.keys():
            sock.write(data)

class Client(NetworkEntity):
    def __init__(self,host='localhost',port=51423):
        NetworkEntity.__init__(self,host,port)
        try:
                self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        except socket.error, e:
                print 'Error creating socket %s' % e
                sys.exit(1)
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
        self.socketThread.write(request)

    def removeSocketThread(sockThrd):
        self.socketThread=None
    
    def __del__(self):
        try:
            del sock
        except KeyboardInterrupt:
            raise
        except:
            traceback.print_exc()

class MessengerClient(Client):
    def __init__(self,message,host='localhost',port=51423):
        Client.__init__(self,host,port)
        self.sendRequest(message)
        del self
            
class SocketThread(object):
    def __init__(self,parent,sock):
        self.parent=parent
        self.thread=threading.Thread(target=self.processInput,args=())
        self.socket=sock
        self.file=self.socket.makefile('rw',0)
        self.alive=True
        self.thread.start()
        
    def write(self,messageList):
        #this may need to change
        for line in messageList.split('\n'):
            self.file.write(line+'\n')
        self.file.flush()
        
    def processInput(self):
        line = ''
        while self.alive:
            while True:
                nline = self.file.readline()
                if nline == self.parent.STOP_MESSAGE:
                    break
                line+=nline 
            if line.strip() == self.parent.CLOSE_MESSAGE:
                del self
                return
            self.parent.processInput(self,line)
            #handles input and output from the socket
        
    def __del__(self):
        self.alive=False
        self.parent.removeSocketThread(self)
        self.socket.close()
