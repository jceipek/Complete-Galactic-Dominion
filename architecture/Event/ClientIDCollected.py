from Event import Event

class ClientIDCollected(Event):
    """
    Fired when the gameClient is assigned an ID
    """
    def __init__(self,cID):
        self.clientID = cID
