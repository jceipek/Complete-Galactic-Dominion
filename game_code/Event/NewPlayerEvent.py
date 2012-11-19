from Event import Event

class NewPlayerEvent(Event):
    """
    Fired when a new player joins the game
    """
    def __init__(self,ID):
        Event.__init__(self)
        self.ID = ID
