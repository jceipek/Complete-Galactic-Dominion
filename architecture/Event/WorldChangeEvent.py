from Event import Event

class WorldChangeEvent(Event):
    """
    Request to change world.

    #Attributes:
    #    world = the destination world
    """

    def __init__(self,world):
        Event.__init__(self)
        self.world = world
