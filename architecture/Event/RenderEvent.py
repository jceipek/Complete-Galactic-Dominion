from Event import Event

class RenderEvent(Event):
    """
    Request to draw to the display surface
    """
    def __init__(self,displaySurface):
        Event.__init__(self)
        self.displaySurface = displaySurface