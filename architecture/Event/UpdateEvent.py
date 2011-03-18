from Event import Event

class UpdateEvent(Event):
    """
    Request to update objects.
    
    #Attributes:
    #   elapsedTime = time that has passed since the last frame. Used to sync 
                      movement speed across different hardware
    """

    def __init__(self,elapsedTime):
        Event.__init__(self)
        self.elapsedTime = elapsedTime