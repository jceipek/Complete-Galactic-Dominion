import cPickle
from Event import Event

class EventExecutionEvent(Event):
    """
    Fired as a command to change the world
    """
    def __init__(self,aStr):
        Event.__init__(self)
        print aStr
        self.data = cPickle.loads(aStr)
        self.verboseInfo = "Data: " + str(self.data) + "\n"
        
    
