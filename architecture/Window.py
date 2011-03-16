#DEVELOPER'S NOTE: Anything beginning with "TMP_" must be removed before the release version.
#Variables and methods beginning with this specifier are present only for the purpose of scaffolding

import pygame, threading

def TMP_eventParser(pygameEvents): # USING TMP_ TO INDICATE TEMPORARY IMPLEMENTATION FOR SAKE OF FUNCTIONALITY
    #The real parser will pass on the wrapped events to the low-level event manager
    #This way unused events can be ignored easily
    #Will use if-elseif-else block for this
    global TMP_ACTIVE
    for rawEvent in pygameEvents:
        if rawEvent.type == pygame.QUIT:
            TMP_ACTIVE = False
        print rawEvent

class Window(object):
    """
    A wrapper for a pygame screen, providing easily accessible
    functionality such as setting the window resolution and
    enabling full screen mode. It also intercepts pygame events
    for processing in a separate thread and sets up a drawing
    loop.
    
    #Attributes:
    #    fullscreenMode = bool
    #    resolution = (widthPx,heightPx)
    #    active = bool
    #    displaySurface = pygame.display
    """
    
    def __init__(self,width=640,height=480,fullscreenMode=False):
        pygame.init()
        global TMP_ACTIVE
        self.resolution = (width,height)
        self.fullscreenMode = fullscreenMode
        self.updateScreenMode()
        self.active = True
        TMP_ACTIVE = True
        
    def updateScreenMode(self):
        if self.fullscreenMode:
            self.displaySurface = pygame.display.set_mode(self.resolution,pygame.FULLSCREEN)
        else:
            self.displaySurface = pygame.display.set_mode(self.resolution)

    def run(self):
        TMP_ms_elapsed = 0
        TMP_gameClock = pygame.time.Clock()
        #while self.active: #This version should be used once events are implemented
        while TMP_ACTIVE:
            #Pass all pygame events to a parser thread for wrapping in standardized events
            #NOT YET IMPLEMENTED PROPERLY - see function ref'd below
            threading.Thread(target=TMP_eventParser,args=(pygame.event.get(),)).start()
            
            #Send the update event. I see no reason to thread this given the
            #pygame implementation. This will simply send an event that the
            #event manager will pass to the occurrence manager to send to the
            #renderer (in the same thread + process) and the updater (in a separate thread)
            #QUESTION: will this cause additional overhead? Should we call the renderer fn
            #directly?
            #NOT YET IMPLEMENTED PROPERLY - drawing here for now
            print "Updating now."
            self.displaySurface.fill((0,0,0))
            pygame.display.flip()
            TMP_ms_elapsed = TMP_gameClock.tick()
        
        print "Quitting now."
        pygame.quit()
            
    def deactivate(self):
        #Called when the window needs to be closed.
        #This will prevent processing of any more user input events,
        #so the program should preferably be closed at this point
        self.active = False