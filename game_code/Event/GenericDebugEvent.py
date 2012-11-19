from Event import Event
        
class GenericDebugEvent(Event):
    """
    Fire this event instead of using a print statement for debugging purposes.
    """

    def __init__(self,info):
        Event.__init__(self)
        self.verboseInfo = info