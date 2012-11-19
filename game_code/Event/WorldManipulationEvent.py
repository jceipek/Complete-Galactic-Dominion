import cPickle
from Event import Event

class WorldManipulationEvent(Event):
    """
    Fired as a request to change the world
    """
    def __init__(self,data=None):
        Event.__init__(self)
        self.data = data
        
    def toPacket(self):
        return cPickle.dumps(self.data)
