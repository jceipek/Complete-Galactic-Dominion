import cPickle

class WorldManipulationEvent(Event):
    """
    Fired whenever the state of the world needs to change
    """
    def __init__(self):
        Event.__init__(self)
    def toPacket(self):
        return cPickle.dumps(self)
    def fromPacket(str):
        return cPickle.loads(str)
