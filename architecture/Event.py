class Event(object):
    """
    This is a superclass for any events that can be read by the low level event manager
    
    verboseInfo = A string of debugging info
    """
    #ATTRIBUTES UNKNOWN FOR THE MOMENT
    def __init__(self):
        self.verboseInfo = "\tNo Additional Debug Info Available\n"

class MouseLocals:
    MOUSE_PRESSED = 1
    MOUSE_RELEASED = 0
    LEFT_CLICK = 1
    RIGHT_CLICK = 3
    SCROLL_UP = 4
    SCROLL_DOWN = 5

class MouseClickedEvent(Event):
    """
    Basic mouse event.
    
    #Attributes:
    #   pos = (x,y)
    #   state = pressed or released ENUM
    #   buttonID = button ENUM
    """

    def __init__(self,posxy,state,buttonId):
        Event.__init__(self)
        self.pos = posxy
        self.state = state
        self.buttonId = buttonId
        self.verboseInfo = "\tPosition: "+str(self.pos)+"\n"+\
        "\tButton State: "+str(self.state)+"\n"+\
        "\tButton Pressed: "+str(self.buttonId)+"\n"

class GenericDebugEvent(Event):
    """
    Fire this event instead of using a print statement for debugging purposes.
    """

    def __init__(self,info):
        Event.__init__(self)
        self.verboseInfo = info

class RenderEvent(Event):
    """
    Request to draw to the display surface
    """
    def __init__(self,displaySurface):
        Event.__init__(self)
        self.displaySurface = displaySurface

class RefreshEvent(Event):
    """
    Request to update the screen
    """
    pass

class RefreshCompleteEvent(Event):
    """
    Called when drawing to the screen is completed
    """
    pass

class StartEvent(Event):
    """
    Request to begin monitoring input in the window
    """
    #ATTRIBUTES UNKNOWN FOR THE MOMENT
    pass

class QuitEvent(Event):
    """
    Request to close the program
    """
    #ATTRIBUTES UNKNOWN FOR THE MOMENT
    pass