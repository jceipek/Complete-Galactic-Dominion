"""
B{The central hub of event processing. Look here after client.py}
"""

from Debugger import Debugger
import Event

class Manager(object):
    """
    All communication between the L{Universe}, L{UserInterface}, and L{Window} 
    happens here. It is essential for preserving an X{MVC} paradigm.
    
    L{Listener}s register themselves with the Manager, and then they can send 
    events to the Manager. When the manager gets an event, it is interpreted
    and passed along to any L{Listener} that is X{listening} for that event.
    """
    
    def __init__(self,eventTimer,debugger):
        """
        Set up a manager with an empty L{Listener} L{WeakKeyDictionary}, an 
        empty eventQueue, and a timer used for timestamps.
        
        @param listeners:
        @param eventTypesToListeners:
        @param eventQueue: A list of all events that come in for processing.
        @param eventTimer: Used for timestamps.
        
        @param debugger: Listens for all events and records events if it is 
        activated.
        @type debugger: L{Debugger}
        """
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()
        self.eventTypesToListeners = WeakKeyDictionary()
        self.eventQueue = []
        self.eventTimer = eventTimer
        self.debugger = debugger

    def registerListener( self, listener ):
		for evType in listener.eventTypes:
			self.eventTypesToListeners.setdefault(evType,[]).append(listener)
		self.listeners[ listener ] = 1

    def unregisterListener( self, listener ):
        if listener in self.listeners:
            del self.listeners[ listener ]

    def post( self, event ):
        event.timeFired = self.eventTimer.getTime()
    
        if self.debugger.SYMBOLS_ENABLED:
            self.debugger.logMsg(event)
        ##IN THE ACTUAL CODE, THIS FUNCTION WILL MAKE SURE EVENTS ONLY GET SENT 
        ##TO LISTENERS WHICH MIGHT CARE. SOME LISTENERS SHOULD START THEIR OWN 
        ##THREADS
        
        #for listener in self.listeners: ### WAS WORKING
        for listener in self.eventTypesToListeners.get(type(event),[]):
			listener.notify(event)
            #NOTE: If the weakref has died, it will be 
            #automatically removed, so we don't have 
            #to worry about it.
