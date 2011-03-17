"""
This is copied almost verbatim from the MVC tutorial.
It will change once we have two managers. Start small, right? :)
"""

class Manager:
    """
    this object is responsible for coordinating most communication
    between the Model, View, and Controller.
    """
    def __init__(self):
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()
        self.eventQueue= []

    def registerListener( self, listener ):
        self.listeners[ listener ] = 1

    def unregisterListener( self, listener ):
        if listener in self.listeners:
            del self.listeners[ listener ]

    def post( self, event ):
        print(type(event))
        if event.verboseInfo:
            print(event.verboseInfo)
        #if not isinstance(event, TickEvent):
        #    logMsg( "     Message: " + event.name + " " + event.type)
        ##IN THE ACTUAL CODE, THIS FUNCTION WILL MAKE SURE EVENTS ONLY GET SENT TO LISTENERS WHICH MIGHT CARE
        for listener in self.listeners:
            #NOTE: If the weakref has died, it will be 
            #automatically removed, so we don't have 
            #to worry about it.
            listener.notify(event)