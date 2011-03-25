from Event import Event 

class DisplaySurfaceCreatedEvent(Event):
    """
    Notifies the window about the resolution and the surface to be displayed. 

    @param resolution: resolution
    @type resolution: tuple(x,y)

    @param displaySurface: surface to be displayed in the window
    @type displaySurface: pygame.Surface
    """

    def __init__(self,resolution, displaySurface):
        Event.__init__(self)
	self.resolution = resolution
	self.displaySurface = displaySurface	
