#DEVELOPER'S NOTE: Anything beginning with "TMP_" must be removed before the release version.
#Variables and methods beginning with this specifier are present only for the purpose of scaffolding

import pygame, threading

import Event
from Listener import Listener

class Window(Listener):
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
    
    def __init__(self,manager,width=640,height=480,fullscreenMode=False):
        
        #Using this until someone can explain why super() is or is not the right way to do this
        #Waaaay too many disagreements/articles on this online
        Listener.__init__(self,manager)
        # A Window is a listener because it has to know when to change (close, for example)
        
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
        TMP_ms_elapsed = 0 #should be in the renderer
        TMP_gameClock = pygame.time.Clock() #should be in the renderer
        #while self.active: #This version should be used once events are implemented
        while self.active:
            #Pass all pygame events to a parser thread for wrapping in standardized events
            #I DON'T KNOW IF THIS WILL WORK PROPERLY FOR MULTIPLE EVENTS, YET - Julian
            threading.Thread(target=self.pygameEventPoster,args=(pygame.event.get(),)).start()
            
            #Send the update event. I see no reason to thread this given the
            #pygame implementation. This will simply send an event that the
            #event manager will pass to the occurrence manager to send to the
            #renderer (in the same thread + process) and the updater (in a separate thread)
            #QUESTION: will this cause additional overhead? Should we call the renderer fn
            #directly?
            #NOT YET IMPLEMENTED PROPERLY - drawing here for now
            #print "Updating now."
            self.displaySurface.fill((0,0,0))
            pygame.display.flip()
            TMP_ms_elapsed = TMP_gameClock.tick()
        
        pygame.quit()
        
    def pygameEventPoster(self,pygameEvents):
        #Convert pygame events to useful events and send them to the manager if needed
        #WARNING: THIS IS A THREADED FUNCTION. BE VERY CAREFUL WHEN CODING HERE.
        
        for rawEvent in pygameEvents:

            #NOT YET FULLY IMPLEMENTED - more events needed
            realEvent = None
            if rawEvent.type == pygame.QUIT:
                realEvent = Event.QuitEvent()
            elif rawEvent.type == pygame.MOUSEBUTTONDOWN:
                state = Event.MouseLocals.MOUSE_PRESSED
                buttonId = rawEvent.button
                realEvent = Event.MouseClickedEvent(rawEvent.pos,state,buttonId)
            elif rawEvent.type == pygame.MOUSEBUTTONUP:
                state = Event.MouseLocals.MOUSE_RELEASED
                buttonId = rawEvent.button
                realEvent = Event.MouseClickedEvent(rawEvent.pos,state,buttonId)
        
            if realEvent:
                self.manager.post(realEvent) #this scares me -Julian
            
    def notify(self, event):
        #Overriding Listener implementation
        if isinstance( event, Event.QuitEvent ):
            self.deactivate()

    def deactivate(self):
        #Called when the window needs to be closed.
        #This will prevent processing of any more user input events,
        #so the program should preferably be closed at this point
        self.active = False