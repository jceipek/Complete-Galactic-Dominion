import sys, pygame

class Mouse:
    """
    A class which keeps track of mouse events and processes them to
    determine when a mouse is being clicked or dragged, and the 
    associated buttons and positions.
    """
    
    # Class attributes mapping mouse button to an int
    LEFT = 1
    CENTER = 2
    RIGHT = 3
    
    # Class attributes mapping a mouse action to an int
    TAPPED = 10
    DRAGGED = 11

    def __init__(self):
		
		# Position of the last MOUSEBUTTONUP event
        self.upClickPos = (0,0)
        
        # Position of the last MOUSEBUTTONDOWN event
        self.downClickPos = (0,0)
        
        # A list of past events for processing
        self.eventChain = []
        
        # Boolean indicating whether the mouse is currently being dragged
        self.isDragging = False
        
        # Last position of the cursor while dragging
        self.dragPos = (0,0)
        
        # Which mouse button is currently down (int from above)
        self.mouseDownButton = None
        
        # Stores length of eventChain at previous MOUSEBUTTONDOWN event
        # Used to determine amount of events between a MOUSEBUTTONDOWN
        # and a MOUSEBUTTONUP event
        self.mouseDownIndex = 0
		
    def mouseClickState(self):
		"""
		Determines state of mouse and returns tuple indicating
		[0] - mouse state --> DRAGGED, TAPPED, NONE
		[1] - associated mouse button --> RIGHT, CENTER, LEFT, NONE
		"""
		if len(self.eventChain) > 0:
			
			curEvent = self.eventChain[-1]
			
			if curEvent.type == pygame.MOUSEBUTTONDOWN:
				
				self.mouseDownChainLen = len(self.eventChain)
				self.mouseDownButton = curEvent.button
				self.downClickPos = self.dragPos = curEvent.pos
				self.isDragging = True
				
			elif curEvent.type == pygame.MOUSEBUTTONUP:
				
				idxChange = len(self.eventChain)-self.mouseDownChainLen
				self.upClickPos = self.eventChain[-1].pos
				
				self.clearEvents_ip()
				self.isDragging = False
				
				if idxChange > 1:
					return (self.DRAGGED, self.mouseDownButton)
				else: # idxChange == 1 indicates a tap
					return (self.TAPPED, self.mouseDownButton)
			
			elif self.isDragging:
				self.dragPos = curEvent.pos
			
		return (None,None)
    
    def addEvent_ip(self,event):
		"""Adds event to eventChain queue."""
		self.eventChain.append(event)
    
    def clearEvents_ip(self):
		"""Clears events in eventChain queue."""
		self.eventChain = []
            
    def getFinishedPos(self):
		"""Returns position of click after mouse goes down then up."""
		return (self.downClickPos, self.upClickPos)
        
    def getDragPos(self):
		"""Returns position of click after mouse goes down then drags."""
		return (self.downClickPos, self.dragPos)

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

def BBoxToRect(p1,p2):
	"""
	Takes two screen positions and returns the bounding box as a 
	pygame.Rect object.
	"""
	x1,y1 = p1
	x2,y2 = p2
	bboxRect = (pygame.Rect(p1,(x2-x1,y2-y1)))
	bboxRect.normalize() # Normalizes to remove negative sizes.
	return bboxRect

class Ball(pygame.sprite.Sprite):
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
    # isSelected #bool
    
    # dest #overall destination for object

    
    def __init__(self,x,y,dx = 0.0,dy = 0.0,speed = 1.0,image = pygame.image.load("ball.png")):
        pygame.sprite.Sprite.__init__(self)
        self.loc = Vector(x,y)
        self.dest = Vector(x,y)
        self.dir = Vector(dx,dy)
        self.speed = speed
        self.image = image.convert_alpha()
        self.rect = image.get_rect()
        #This works because Rect starts at 0.0,0.0
        self.rect.center = (int(x+0.5),int(y+0.5))
        self.isSelected = False
        allSprites.add(self)
        self.health = self.maxHealth = 15.0
    
    def deSelected(self):
		"""Removes object from selectedSprites list."""
		self.isSelected = False
		selectedSprites.remove(self)
    
    def reSelected(self):
		"""Adds object to selectedSprites list."""
		self.isSelected = True
		self.health -= 1
		selectedSprites.add(self)
        
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
    
    def draw(self):
        if self.health > 0:
            screen.blit(self.image, self.rect)
            self.drawHealthBar()
        else:
            self.kill()
    
    def drawHealthBar(self):
		
		centerX, top = self.rect.midtop
		width, height = self.rect.size
		
		hBarPadY = 3
		hBarHeight = 10
		hBarScaleX = 1
		
		hBarWidth = (hBarScaleX*width)
		
		hBarTop = top - hBarPadY - hBarHeight
		scaleHealth = round((self.health/self.maxHealth)*hBarWidth)
		
		hRemain = (centerX-hBarWidth//2,hBarTop,scaleHealth,hBarHeight)
		hLost = (hRemain[0]+scaleHealth,hBarTop,hBarWidth-scaleHealth,hBarHeight)
		
		screen.fill((0,255,0), hRemain)
		screen.fill((255,0,0), hLost)
    
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

selectedSprites = pygame.sprite.Group()
allSprites = pygame.sprite.Group()

screen = pygame.display.set_mode(size)

#Set up ball
aBall = Ball(25.0,25.0,speed=0.5)
aBall.dest = Vector(25.0,25.0)
aBall.dir = aBall.loc.pointTo(aBall.dest)

#Set up another ball
bBall = Ball(250.0,250.0,speed=0.5)
bBall.dest = Vector(250.0,250.0)
bBall.dir = aBall.loc.pointTo(bBall.dest)

mouse = Mouse()
MAX_FPS = 60

font = pygame.font.Font(pygame.font.get_default_font(), 16)
txt = font.render("FPS: ***", True, (255,255,255))
txtbound = txt.get_rect()

# Initialize a game clock
gameClock = pygame.time.Clock()

# Initialize boolean to indicate whether a new mouse event has fired
# since the previous cycle through the loop
newEvent = False

while RUNNING:
        
    ########EVENTS#################
    for event in pygame.event.get():
        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, \
         pygame.MOUSEMOTION]:
            mouse.addEvent_ip(event)
            newEvent = True
        
        if event.type == pygame.QUIT:
            RUNNING = False
	
	if newEvent == True:
		newEvent = False
		
		clickType, clickButton = mouse.mouseClickState()
		downClickPos, upClickPos = mouse.getFinishedPos()
		
		if clickType is not None:
			
			if clickButton == Mouse.RIGHT:
			
				for sprite in selectedSprites:
					
					interpretMessage(upClickPos,sprite)
			
			elif clickButton == Mouse.LEFT:
				
				if clickType == Mouse.DRAGGED:
					
					dragRect = BBoxToRect(downClickPos,upClickPos)
					
					# Determine if any sprites overlap with the dragged
					# box and select/deselect them as necessary
					for sprite in allSprites:
						if sprite.rect.colliderect(dragRect):
							sprite.reSelected()
						else:
							sprite.deSelected()
					
				elif clickType == Mouse.TAPPED:
					
					# Determine if any sprites contain the tapped point
					# and select/deselect them as necessary
					for sprite in allSprites:
						if sprite.rect.collidepoint(*upClickPos):
							sprite.reSelected()
						else:
							sprite.deSelected()
    
    #Move the ballrects in place (modifier, not pure function)
    for sprite in allSprites:
		sprite.update_ip(ms_elapsed)
    
    #Clear the background with a bg color
    screen.fill(bg)
    
    #Paste the ball image on the screen in the rectangle ballrect
    #allSprites.draw(screen)
    for sprite in allSprites:
		#screen.blit(sprite.image, sprite.rect)
		sprite.draw()
    
    # Drag the left-click + drag bounding box
    if mouse.isDragging and mouse.mouseDownButton == Mouse.LEFT:
		bbox = BBoxToRect(*mouse.getDragPos())
		pygame.draw.rect(screen, (150,150,0),bbox,3)

    txt = font.render("FPS: "+str(int(gameClock.get_fps())), True, (255,255,255))
    screen.blit(txt, txtbound)
    
    #Update the screen by switching buffers
    pygame.display.flip()
    
    #Determine the amount of time that has passed since the previous tick
    #Limits framerate
    ms_elapsed = gameClock.tick(MAX_FPS)

pygame.quit() #quit properly, without an exception
