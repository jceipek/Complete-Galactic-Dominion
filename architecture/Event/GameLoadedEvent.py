from Event import Event

class GameLoadedEvent(Event):
    """
    Fired when a new player joins the game
    """
    def __init__(self,numberOfEntities,releasedEntityIDs):
        self.numberOfEntities = numberOfEntities
        self.releasedEntityIDs = releasedEntityIDs
        self.verboseInfo = ''
