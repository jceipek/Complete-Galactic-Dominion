#this server will be able to handle multiple clients
#it is an echo server...it will simply echo any data that the client provides
#
#test this server by typing this command into the terminal while the program
#is running:
##telnet localhost 51423

import socket, traceback,os,sys
from threading import *

host=''#connect to all interfaces
port=51423#this port was chosen arbitrarily, it could be any free port above 1024

socketFiles=dict()

def handleChild(clientSocket):
    '''Here is where all of the client connections are dealt with
    '''
    print 'New child',currentThread().getName()
    print 'Got connection from',clientSocket.getpeername()
    fd=clientSocket.makefile('rw',0)
    socketFiles[fd]=1
    while True:
        data=fd.readline()#recieve 4096 bytes at a time
        print 'Message from client:',data.strip()
        if data.strip()=='quit':#if there is no more data left
            fd.write(data+'\n')#send the data back to the client
            fd.flush()
            break
        for aFile in socketFiles:
            aFile.write(data)#send the data to all of the clients
            aFile.flush()

    #close the connection
    del socketFiles[fd]
    clientSocket.close()

#set up the server's socket
#an internet server using TCP
serverSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

serverSocket.bind((host,port))#bind to the port
serverSocket.listen(1)

#the parent thread will listen for new connections
while True:
    #this try-except statement is VITAL, exceptions thrown here SHOULD NOT be
    #able to crash the server
    try:
        clientSocket,clientAddress=serverSocket.accept()
    except KeyboardInterrupt:
        #allow KeyboardInterrupt to stop the server
        raise
    except:
        #do not allow anything else to stop the server
        traceback.print_exc()
        continue

    t=Thread(target=handleChild,args=(clientSocket,))
    t.start()

