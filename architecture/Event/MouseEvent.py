from Event import Event

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