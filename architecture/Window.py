import pygame, threading

def TMP_eventParser(pygameEvents): # USING TMP_ TO INDICATE TEMPORARY IMPLEMENTATION FOR SAKE OF FUNCTIONALITY
    #The real parser will pass on the wrapped events to the low-level event manager
    #This way unused events can be ignored easily
    #Will use if-elseif-else block for this
    for rawEvent in pygameEvents:
        print rawEvent

class Window(object):
	"""
	A wrapper for a pygame screen, providing easily accessible
	functionality such as setting the window resolution and
	enabling full screen mode. It also intercepts pygame events
	for processing in a separate thread and sets up a drawing
	loop.
	
	#Attributes:
	#	fullscreenMode = bool
	#	resolution = (widthPx,heightPx)
	#	active = bool
	#	displaySurface = pygame.display
	"""
	
	def __init__(self,width=640,height=480,fullscreenMode=False):
		pygame.init()
		self.resolution = (width,height)
		self.fullscreenMode = fullscreenMode
		self.updateScreenMode()
		self.active = True
		self.loop()
		
	def updateScreenMode(self):
		if fullscreenMode:
			self.displaySurface = pygame.display.set_mode(self.resolution,pygame.FULLSCREEN)
		else:
			pygame.display.set_mode(self.resolution)

    def loop(self):
        TMP_ms_elapsed = 0
        TMP_gameClock = pygame.time.Clock()
        while self.active:
            #Pass all pygame events to a parser thread for wrapping in standardized events
            #NOT YET IMPLEMENTED PROPERLY - see function ref'd below
            threading.Thread(target=eventParser,args=(pygame.event.get(),)).start()
            
            #Send the draw event. I see no reason to thread this given the
            #pygame implementation. This will simply send an event that the
            #event manager will pass to the occurrence manager to send to the
            #renderer
            #QUESTION: will this cause additional overhead? Should we call the renderer fn
            #directly?
            #NOT YET IMPLEMENTED PROPERLY - drawing here for now
            print "Drawing now."
            screen.fill((randint(0,255),0,0))
            pygame.display.flip()
            TMP_ms_elapsed = TMP_gameClock.tick()
