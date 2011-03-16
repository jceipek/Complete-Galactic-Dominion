import sys, pygame, threading, socket, sys, time, cPickle

class Mouse:
	"""
	A class with one instance used to keep track of special mouse
	events like taps as opposed to button down + button up.
	I anticipate the removal/refactoring of this class when we 
	run iface event detection in a separate thread. -Julian
	
	This class only supports single tap events for the time being.
	"""
	eventChain = [] #a list of past events for processing
	
	def isTapActive(self):
		if len(self.eventChain) > 1:
			if self.eventChain[-2].type == pygame.MOUSEBUTTONDOWN and \
			self.eventChain[-1].type == pygame.MOUSEBUTTONUP:
				return True
		return False
	
	def addEvent_ip(self,event):
		self.eventChain.append(event)
	
	def clearEvents_ip(self):
		self.eventChain = []
		
	def pos(self):
		if len(self.eventChain) > 0:
			return self.eventChain[-2].pos

class Vector:
    """
    A way of representing a 2d location or dir.
    """
    #Attributes
    # x (scalar)
    # y (scalar)

    def __init__(self,x=0.0,y=0.0):    
        self.x = x
        self.y = y

    def mag(self):
        m = pow(self.x**2 + self.y**2,0.5)
        return m
        
    def scale_ip(self,s):
        self.x *=s
        self.y *= s
        
    def scale(self,s):
        return Vector(self.x*s,self.y*s)

    def unit_ip(self):
        mag = self.mag()
        self.x /= mag
        self.y /= mag
        
    def unit(self):
        mag = self.mag()
        return Vector(self.x/self.mag(), self.y/self.mag())
        
    def list(self):
        return [self.x,self.y]
        
    def tuple(self):
        return (self.x,self.y)
        
    def diff(self,vec):
        xdiff = vec.x-self.x
        ydiff = vec.y-self.y
        return Vector(xdiff,ydiff)

    def pointTo(self,locVec):
    	if locVec.x == self.x and locVec.y == self.y:
    		return Vector(0.0,0.0)
        diff = self.diff(locVec)
        diff.unit_ip()
        return diff

class Ball:
    """
    Object to represent properties of an object that has a location and the 
    ability to move.
    """
    #Attributes:
    #image #pygame.image object
    #rect #pygame.Rect
    
    # loc #float location of object (Vector object)
    # dir #dir the object wants to move (Vector object)
    # speed #max movement speed (scalar)
    
    # dest #overall destination for object

    
    def __init__(self,x,y,dx = 0.0,dy = 0.0,speed = 1.0,image = pygame.image.load("ball.png")):
        self.loc = Vector(x,y)
        self.dest = Vector(x,y)
        self.dir = Vector(dx,dy)
        self.speed = speed
        self.image = image.convert_alpha()
        self.rect = image.get_rect()
        #This works because Rect starts at 0.0,0.0
        self.rect.center = (int(x+0.5),int(y+0.5))
    
    def face_ip(self,locVec):
        self.dir = self.loc.pointTo(locVec)
        self.dest = locVec
                
    def move_ip(self,eTime):
        if eTime>0:
            disp = self.dir.unit()
            disp = disp.scale(eTime*self.speed)
            self.loc.x += disp.x
            self.loc.y += disp.y
            self.rect.center = (int(self.loc.x+0.5),int(self.loc.y+0.5))
        
    def update_ip(self,eTime):
    	if eTime*self.speed >= self.loc.diff(self.dest).mag():
    		#destination was reached
    		self.dir.x = 0.0
    		self.dir.y = 0.0
    		self.rect.move_ip(self.loc.diff(self.dest).list())
    		self.loc.x = self.dest.x
    		self.loc.y = self.dest.y
    	else:
    		self.move_ip(eTime)

def interpretMessage(message,ball):
    #Currently assumes tuple or list input for message
    ball.face_ip(Vector(float(message[0]),float(message[1])))

def manageNetworkConnection(host='localhost',port=51423):
        print 'Managing Network Connection'
        global requestQueue

        #create socket
        try:
                clientSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        except socket.error, e:
                print 'Error creating socket %s' % e
                sys.exit(1)

        #determine the port
        try:
                port=int(port)
        except ValueError:
                #look up the port
                port = socket.getservbyname(port,'tcp')
        except socket.error,e:
                print 'Couldn\'t find your port'
                sys.exit(1)

        try:
                clientSocket.connect((host,port))
        except socket.gaierror, e:
                print 'Address error: %s' % e
                sys.exit(1)
        except socket.error, e:
                print 'Connection error: %s' % e
                sys.exit(1)

        fd = clientSocket.makefile('rw',0)

        #Send and recieve data
        global RUNNING
        print 'running: '+str(RUNNING)
        while RUNNING:
                #print 'Im in a loop'
                #Write to the socket
                with requestQueueLock:
                        #print 'Network manager aquired requestQueueLock'
                        for request in requestQueue:
                                print 'Sending data:',request
                                try:
                                        fd.write(request)
                                except socket.error,e:
                                        print 'Error sending data: %s' % e
                                        sys.exit(1)
                        #Flush the write
                        if len(requestQueue):
                                try:
                                        fd.flush()
                                        print 'Data successfully sent'
                                except socket.error, e:
                                        print 'Error sending data (detected by flush): %s' % e
                                        sys.exit(1)
                                try:
                                        for line in fd:
                                                print 'There is something to read'
                                                message=cPickle.loads(line.strip())
                                                global BALL
                                                print 'Message from socket: '+line
                                                interpretMessage(message,BALL)
                                                print 'give me something'
                                except:
                                        pass#Handle exceptions
                                
                        requestQueue=[]

                #Allow time for requests to be made
                time.sleep(.01)

        print 'Closing network connection'
        clientSocket.close()
        pass#connect to server
        #look for available requests
        #send messages to server
        #listen for responses
        #send response to interpretMessage

def sendRequest(mousePosition,ball):
        global requestQueue
        global BALL
        BALL=ball
        print 'Adding request to queue'
        #pickle requests and add them to the queue
        request=cPickle.dumps(mousePosition)
        with requestQueueLock:
                print 'Request manager aquired requestQueueLock'
                requestQueue.append(request)
        print 'Request manager released requestQueueLock'
        time.sleep(.01)
        print requestQueue

#Establish network connection
RUNNING = True
requestQueue=[]
requestQueueLock=threading.Lock()
networkThread = threading.Thread(target=manageNetworkConnection)
networkThread.start()

#Background color
bg = (51, 51, 255)

#Vars to correct for lag
last_time = 0
ms_elapsed = 1

#Screen Parameters
size = (width, height) = (640, 480)

pygame.init()

screen = pygame.display.set_mode(size)

#Set up ball
aBall = Ball(0.0,0.0,speed=0.5)
aBall.dir = Vector(1.0,1.0)
aBall.dest = Vector(0.0,0.0)
aBall.dir = aBall.loc.pointTo(aBall.dest)

mouse = Mouse()


font = pygame.font.Font(pygame.font.get_default_font(), 16)
txt = font.render("FPS: ***", True, (255,255,255))
txtbound = txt.get_rect()

while RUNNING:
    last_time = pygame.time.get_ticks()


	########EVENTS#################
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN or \
        event.type == pygame.MOUSEBUTTONUP:
            mouse.addEvent_ip(event)
        
        if event.type == pygame.QUIT:
            RUNNING = False
            
    if mouse.isTapActive():
    	#specify new destination
    	sendRequest(mouse.pos(),aBall)
    	mouse.clearEvents_ip()
    ###############################
    
    #Move the ballrect in place (modifier, not pure function)
    #aBall.move_ip(ms_elapsed)
    aBall.update_ip(ms_elapsed)
    
    #Clear the background with a bg color
    screen.fill(bg)
    
    #Paste the ball image on the screen in the rectangle ballrect
    screen.blit(aBall.image, aBall.rect)
    
    txt = font.render("FPS: 1000/"+str(ms_elapsed), True, (255,255,255))
    screen.blit(txt, txtbound)
    #Update the screen by switching buffers
    pygame.display.flip()
    
    #Determine the time it took 
    
    
    ms_elapsed = pygame.time.get_ticks() - last_time

pygame.quit() #quit properly, without an exception
