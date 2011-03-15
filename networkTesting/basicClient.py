#example from Chapter 1 of "Foundations of Network Programming"
#adapted for use with file-like objects

import socket, sys

port = 70#Gopher uses port 70
#Check iana.org for a list of assigned ports

host = sys.argv[1]#the first command-line argument
filename = sys.argv[2]#the second command-line argument

#create a socket for the internet (arg1) and TCP (arg2)
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    #connect to the host server on the correct port
    s.connect((host,port))
except socket.error, e:
    print 'Error connecting to server: %s' % e
    exit()

#generate a file-like object to use
#takes a mode, 'rw' (reading and writing), and a buffering mode, 0, (no buffering).
fd = s.makefile('rw',0)

#request the data from the server
fd.write(filename+'\r\n')

#print everything in the file-like object
for line in fd:
    print line
