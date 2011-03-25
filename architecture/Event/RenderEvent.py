from Event import Event

class RenderEvent(Event):
    """
    Request to draw to the display surface
    """
    def __init__(self):
        Event.__init__(self)
