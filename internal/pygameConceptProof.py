import sys, pygame

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
        self.image = image
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

#Background color
bg = (51, 51, 255)

#Vars to correct for lag
last_time = 0
ms_elapsed = 1

#Screen Parameters
size = (width, height) = (640, 480)

RUNNING = True

pygame.init()

screen = pygame.display.set_mode(size)

#Set up ball
aBall = Ball(0.0,0.0,speed=0.5)
aBall.dir = Vector(1.0,1.0)
aBall.dest = Vector(0.0,0.0)
aBall.dir = aBall.loc.pointTo(aBall.dest)

mouse = Mouse()

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
    	interpretMessage(mouse.pos(),aBall)
    	mouse.clearEvents_ip()
    ###############################
    
    #Move the ballrect in place (modifier, not pure function)
    #aBall.move_ip(ms_elapsed)
    aBall.update_ip(ms_elapsed)
    
    #Clear the background with a bg color
    screen.fill(bg)
    
    #Paste the ball image on the screen in the rectangle ballrect
    screen.blit(aBall.image, aBall.rect)
    #Update the screen by switching buffers
    pygame.display.flip()
    
    #Determine the time it took 
    ms_elapsed = pygame.time.get_ticks() - last_time

pygame.quit() #quit properly, without an exception
