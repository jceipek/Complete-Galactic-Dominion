#A basic server from an example in Chapter 3 of "Foundations of Python Network Programming"
import socket

host = ''
port = 51423

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((host,port))
print "Waiting for connections..."
s.listen(1)

while True:#catch all exceptions
    
    try:#look for a connection
        clientsock,clientaddr = s.accept()
    except KeyboardInterrupt:
        raise
    except:
        traceback.print_exc()
        continue

    try:#process the connection
        print "Got connection from", clientsock.getpeername()
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.print_exc()

    try:#close the connection
        clientsock.close()
    except KeyboardInterrupt:
        raise
    except:
        traceback.print_exc()
