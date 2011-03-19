import pygame

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
	
	def getCurrentRelMousePos(self):
		"""
		Returns current mouse position, relative to upper-left
		corner of the viewport.
		"""
		return pygame.mouse.get_pos()
