"""
B{DEVELOPER'S NOTE:} Window.py is the first file that uses fully correct commenting practices to
enable parsing with epydoc.

Remember:
=========
    - Anything beginning with ``TMP_'' must be removed before the release version.
      (Variables and methods beginning with this specifier are present only for the purpose of
      scaffolding)
    - Use FIXME as a specifier for code that is implemented as a bad hack or does not work as
      envisioned in the final version.
"""

import pygame, threading, time

import Event
from InputDeviceMastermind import *
from Listener import Listener
from specialMath import *

class Window(Listener):
    """
    A wrapper for a pygame screen, providing easily accessible
    functionality such as setting the window resolution and
    enabling full screen mode. It also intercepts pygame events
    for processing in a separate thread and sets up a drawing
    loop.
    
    A Window is a listener because it has to know when to change (close, for example)
    
    @param fullscreenMode: Contains current status (pygame only has a setter, not a getter)
    @type fullscreenMode: bool
    
    @param resolution: (widthPx, heightPx) for the screen
    @type resolution: tuple(int, int)
    
    @param active: Used for the run loop. Disable to close the window and quit pygame.
    @type active: bool
    
    @param displaySurface: surface that is periodically displayed on the screen.
    @type displaySurface: pygame.Surface
    
    @param gameClock: Clock object that is used to determine time to render a frame
    @type gameClock: pygame.time.Clock
    
    @param gameFrametime: ms elapsed since last frame
    @type gameFrametime: int
    
    @param gameFrametime: ms elapsed since start
    @type gameFrametime: int
    
    @param pygameEvents: Keeps track of the pygame events that are fired during the run loop
    @type pygameEvents: list(*pygame.Event)
    
    @param controlMapping: Used to keep track of what pygame events map to what actual events.
    B{FIXME:} This is not yet implemented completely in terms of functionality in pygameEventPoster
    @type controlMapping: dict
    """
    
    def __init__(self,manager,width=640,height=480,fullscreenMode=False):
        """
        @param manager: The event manager to which the window is registered
        @type manager: pointer to L{Manager} object
        """
        
        eventTypes = [Event.StartEvent, Event.QuitEvent, Event.RefreshEvent, \
            Event.RefreshCompleteEvent]#, Event.DisplaySurfaceToggle]
        
        #Using this until someone can explain why super() is or is not the right way to do this
        #Waaaay too many disagreements/articles on this online
        Listener.__init__(self,manager,eventTypes)
        
        pygame.init()
        pygame.display.set_caption('Complete Galactic Dominion')
        
        self.maxFPS = 60
        
        self.gameClock = pygame.time.Clock()
        self.gameFrametime = 0
        self.gameTime = 0
        self.resolution = (width,height)
        self.fullscreenMode = fullscreenMode
        self.updateScreenMode()
        self.active = True
        self.pygameEvents = []
        self.controlMapping = []
        #self.setUpControlMapping() #FIXME
        
    def updateScreenMode(self):
        """
        Used to initialize the display surface for the first time or to update it at a later time.
        Right now, it only allows fullscreen mode to be toggled.
        """
        if self.fullscreenMode:
            self.displaySurface = pygame.display.set_mode(self.resolution,pygame.FULLSCREEN|pygame.HWSURFACE)
        else:
            self.displaySurface = pygame.display.set_mode(self.resolution)
        self.manager.post(Event.DisplaySurfaceCreatedEvent(self.resolution,self.displaySurface))

    def run(self):
        """
        Main loop for the window. Processes pygame events in a separate thread while 
        sending out messages to update unit positions and the user interface.
        
        B{FIXME:} It also sends out render events to display information on the screen. This is bad
        and should be fixed.
        """
    
        self.updateClock()
        
        self.eventLock = threading.Lock()
        self.eventQueue = []
        
        self.pygameEventThread = threading.Thread(target=self.pygameEventPoster)
        self.pygameEventThread.setDaemon(True)
        self.pygameEventThread.start()
        
        while self.active:
            #Pass all pygame events to a parser thread for wrapping in standardized events

            #Tell the objects on screen to update.
            self.pygameEvents += pygame.event.get()
            self.manager.post(Event.UpdateEvent(self.gameFrametime,self.gameTime))
            with self.eventLock:
                for event in self.eventQueue:
                    self.manager.post(event)
                self.eventQueue = []
            
            #Note: the renderer does not update or display anything.
            #It simply draws to the displaySurface i.e. self.displaySurface.fill((0,0,0))

        pygame.quit()
        
    def pygameEventPoster(self):
        """
        Daemon that converts pygame events to useful events and send them to the manager if needed.
        
        B{FIXME:} This function has to be changed to support reading from a user-defined config/pref
        file for converting events. For example, left and right mouse click mapping should be able
        to be reversed.
        
        B{WARNING: THIS IS A THREADED FUNCTION. BE VERY CAREFUL WHEN CODING HERE.}
        """

        #inputState=InputDeviceMastermind()
        '''
        def pEventToStr(event):
            e=str(event)
            s=''
            if 'Motion' in e:
                #print 'Motion collected'
                s += 'Motion Event '
                if hasattr(event,'pos'):
                    s+=str(event.pos)
                #print 'No problem here'
            elif 'Up' in e:
                s += 'Release Event'
            elif 'Down' in e:
                s += 'Press Event'
            return s

        pEventToStr=pEventToStr
        '''
        
        #FIXME: THIS IS A TEMPORARY MEASURE FOR MULTIPLE SELECTION
        
        keyHeldDict = {'shift':False, 'ctrl':False, 'alt':False}
        
        TMP_dragStartPos = (0,0)
        TMP_mousePos = (0,0)
        TMP_mouseState = 0
        TMP_clickrange = 5
        
        while self.active:
            #inputState.updateState(pEventToStr(rawEvent))
            if self.pygameEvents:
                
                try:
                    rawEvent=self.pygameEvents.pop(0)
                    
                    #FIXME - more events needed
                    realEvent = []
                    if rawEvent.type == pygame.QUIT:
                        realEvent.append(Event.QuitEvent())
    
                    elif rawEvent.type == pygame.MOUSEBUTTONDOWN:
                        
                        buttonId = rawEvent.button
                        if buttonId == Event.MouseLocals.LEFT_CLICK:
                            TMP_mouseState = 1
                            TMP_dragStartPos = rawEvent.pos
                            realEvent.append(Event.DragBeganEvent(rawEvent.pos))
                        elif buttonId == Event.MouseLocals.RIGHT_CLICK:
                            TMP_mouseState = 2
                            realEvent.append(Event.InitiateActionEvent(rawEvent.pos))
                    
                    elif rawEvent.type == pygame.MOUSEBUTTONUP:
                        
                        TMP_mouseState = 0
                        buttonId = rawEvent.button
                        if buttonId == Event.MouseLocals.LEFT_CLICK:
                            if distance(rawEvent.pos,TMP_dragStartPos) > TMP_clickrange:
                                if not keyHeldDict['shift']:
                                    realEvent.append(Event.DragCompletedEvent(TMP_dragStartPos,rawEvent.pos))
                                else:
                                    realEvent.append(Event.AddDragCompletedEvent(TMP_dragStartPos,rawEvent.pos))
                            else:
                                if not keyHeldDict['shift']:
                                    realEvent.append(Event.SelectionEvent(rawEvent.pos))
                                else:
                                    realEvent.append(Event.SingleAddSelectionEvent(rawEvent.pos))
                        elif buttonId == Event.MouseLocals.RIGHT_CLICK:
                            realEvent.append(Event.CompleteActionEvent(rawEvent.pos))
    
                    elif rawEvent.type == pygame.MOUSEMOTION:
                        TMP_mousePos = rawEvent.pos
                        realEvent.append(Event.MouseMovedEvent(rawEvent.pos))
                        
                        if TMP_mouseState == 1:
                            realEvent.append(Event.DragEvent(TMP_dragStartPos,rawEvent.pos))
                        
                    elif rawEvent.type == pygame.KEYDOWN:
                        if rawEvent.key == pygame.K_RSHIFT or \
                            rawEvent.key == pygame.K_LSHIFT:
                            keyHeldDict['shift'] = True
                        if rawEvent.key == pygame.K_RCTRL or \
                            rawEvent.key == pygame.K_LCTRL:
                            keyHeldDict['ctrl'] = True
                        if rawEvent.key == pygame.K_RALT or \
                            rawEvent.key == pygame.K_LALT:
                            keyHeldDict['alt'] = True
    
                    elif rawEvent.type == pygame.KEYUP:
                        if rawEvent.key == pygame.K_RSHIFT or \
                            rawEvent.key == pygame.K_LSHIFT:
                            keyHeldDict['shift'] = False
                        if rawEvent.key == pygame.K_RCTRL or \
                            rawEvent.key == pygame.K_LCTRL:
                            keyHeldDict['ctrl'] = False
                        if rawEvent.key == pygame.K_RALT or \
                            rawEvent.key == pygame.K_LALT:
                            keyHeldDict['alt'] = False
                        if pygame.K_0 <= rawEvent.key <= pygame.K_9:
                            realEvent.append( \
                                Event.NumberKeyPressEvent(rawEvent.key,Event.KeyLocals.UP,keyHeldDict) \
                            )
                        #The following was an attempt to toggle fullscreen mode. 
                        #It broke things and must thus be handled separately
                        #via a carefully constructed menu
                        #if rawEvent.key == pygame.K_F11:
                        #    realEvent.append( \
                        #        Event.DisplaySurfaceToggle(not self.fullscreenMode) \
                        #    )
                        if rawEvent.key == pygame.K_ESCAPE:
                            realEvent.append(Event.QuitEvent())
                    with self.eventLock:
                        for event in realEvent:
                            self.eventQueue.append(event)
#                    for i in realEvent:
#                        self.manager.post(i) #Warning: make sure that threading doesn't cause \
                                                    #problems here!
                except:
                    import sys,traceback
                    print 'An unexpected error occurred in the event thread.'
                    exc_type,exc_value,exc_traceback = sys.exc_info()
                    traceback.print_exc()
                    self.manager.post(Event.QuitEvent())
            
            else: time.sleep(.01)

    def setUpControlMapping(self):
        """
        Tells the ControlMapper to read a control scheme from a pref/config file.
        This mapping will then be used by the L{pygameEventPoster}
        
        B{FIXME:} This method should be called in __init__ and perhaps whenever a new control
        mapping gets assigned (would have to implement a new event to obtain this functionality).
        """
        from ControlMapper import ControlMapper
        controlMapper = ControlMapper()
        self.controlMapping = controlMapper.mapping

    def notify(self, event):
        """
        I{Overriding abstract Listener implementation}
        
        Allows the window to respond to events.
        
        Intercepted Events
        ==================
            - L{Event.StartEvent}
            - L{Event.QuitEvent}
            - L{Event.RefreshEvent}
            - L{Event.RefreshCompleteEvent}
        """

        if isinstance( event, Event.StartEvent ):
            self.manager.post(Event.StartedEvent())
            self.run()
        elif isinstance( event, Event.QuitEvent ):
            self.deactivate()
        elif isinstance( event, Event.RefreshEvent ):
            self.refresh()
        elif isinstance( event, Event.RefreshCompleteEvent ):
            self.updateClock()
        #elif isinstance( event, Event.DisplaySurfaceToggle ):
        #    self.fullscreenMode = event.isFullScreen
        #    self.updateScreenMode()
        
    def updateClock(self):
        """
        Update L{gameFrametime} to reflect the frames elapsed since the last call.
        """
        
        self.gameFrametime = self.gameClock.tick(self.maxFPS)
        self.gameTime += self.gameFrametime
        self.manager.post(Event.GenericDebugEvent(str(self.gameFrametime)))
        
    def refresh(self):
        """
        Tells the surface to display its prepared content to the user, on the screen.
        """
        pygame.display.flip()
        self.manager.post(Event.RefreshCompleteEvent())
    
    def deactivate(self):
        """
        Called when the window needs to be closed.
        This will prevent processing of any more user input events,
        so the program should preferably be closed at this point
        """

        self.active = False
