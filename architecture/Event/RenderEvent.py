from Event import Event

class RenderEvent(Event):
    """
    Request to draw to the display surface
    """
    def __init__(self,displaySurface,screenSize):
        Event.__init__(self)
        self.displaySurface = displaySurface
        self.screenSize = screenSize