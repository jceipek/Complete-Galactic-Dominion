from Event import Event

class UpdateEvent(Event):
    """
    Request to update objects.
    
    @param elapsedTimeSinceLastFrame: Time elapsed since last frame in ms.
    @type elapsedTimeSinceLastFrame: int
    
    @param elapsedTotalTime: Time elapsed since L{Window} timer was started.
    @type elapsedTotalTime: int
    """

    def __init__(self,elapsedTimeSinceLastFrame,totalTime):
        Event.__init__(self)
        self.elapsedTimeSinceLastFrame = elapsedTimeSinceLastFrame
        self.elapsedTotalTime = totalTime