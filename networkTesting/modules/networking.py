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

    def processInput(self,sockThrd,data):
        pass#this should be overwritten in all non-abstract subclasses of NetworkEntity

    def removeSocketThread(self,sockThrd):
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
                print 'Connection Established'
                s=SocketThread(self,clientSocket)
                self.socketThreads[s]=s.file

        self.socket.listen(numPendingConnections)
        self.connecting=True
        self.connectionThread=threading.Thread(target=connectToAllClients)
        self.connectionThread.start()#this is a non daemonic thread and will prevent the server from exiting

    def removeSocketThread(self,sockThrd):
        try:
            del(self.socketThreads[sockThrd])
        except:
            pass
        
    def __del__(self):
        self.connecting=False
        try:
            del(self.socketThreads)
        except KeyboardInterrupt:
            raise
        except:
            traceback.print_exc()
        self.socket.close()

class PrintServer(Server):
    def processInput(self,sockThrd,data):
        print data

class EchoServer(Server):
    def processInput(self,sockThrd,data):
        sockThrd.write(data)

class BroadcastServer(Server):
    def processInput(self,sockThrd,data):
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

    def removeSocketThread(self,sockThrd):
        self.socketThread=None
    
    def __del__(self):
        print 'Deleting Client'
        try:
            self.socketThread.__del__()
        except KeyboardInterrupt:
            raise
        except:
            traceback.print_exc()

class MessengerClient(Client):
    def __init__(self,message,host='localhost',port=51423):
        Client.__init__(self,host,port)
        print 'Sending message: %s' % message
        self.sendRequest(message)
        self.__del__()
            
class SocketThread(object):
    def __init__(self,parent,sock):
        self.parent=parent
        self.thread=threading.Thread(target=self.processInput,args=())
        self.socket=sock
        self.file=self.socket.makefile('rw',0)
        self.alive=True
        self.thread.setDaemon(True)
        self.thread.start()
        
    def write(self,message):
        #this may need to change
        self.file.write(message+'\n')
        self.file.write(self.parent.STOP_MESSAGE+'\n')
        self.file.flush()
        
    def processInput(self):
        while self.alive:
            line = ''
            flag=False
            for nline in self.file:
                flag=True
                print 'Something to read: %s' % nline.strip()
                if nline.strip() == self.parent.STOP_MESSAGE:
                    break
                line+=nline 
            if line.strip() == self.parent.CLOSE_MESSAGE or flag == False:
                self.__del__()
                return
            flag=False
            self.parent.processInput(self,line)
            line=''
        
    def __del__(self):
        self.alive=False
        self.parent.removeSocketThread(self)
        try:
            self.write(self.parent.CLOSE_MESSAGE)
        except:
            pass
        try:
            self.socket.close()
        except:
            pass
