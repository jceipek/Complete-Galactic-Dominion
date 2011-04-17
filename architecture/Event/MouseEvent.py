from Event import Event

class MouseLocals:
    MOUSE_PRESSED = 1
    MOUSE_RELEASED = 0
    LEFT_CLICK = 1
    RIGHT_CLICK = 3
    SCROLL_UP = 4
    SCROLL_DOWN = 5
        
class MouseMovedEvent(Event):
    """
    Fired when the mouse moves; keeps track of position only.
    May have to change this later.
    
    #Attributes:
    #   pos = (x,y)
    """
    def __init__(self,posxy):
        Event.__init__(self)
        self.pos = posxy
        self.verboseInfo = "\tPosition: " + str(self.pos) + "\n"
        
class SelectionEvent(Event):
    def __init__(self,posxy):
        Event.__init__(self)
        self.pos = posxy
        self.verboseInfo = "\tPosition: " + str(self.pos) + "\n"
        
class SingleAddSelectionEvent(Event):
    def __init__(self,posxy):
        Event.__init__(self)
        self.pos = posxy
        self.verboseInfo = "\tPosition: " + str(self.pos) + "\n"

class SingleAddSelectionEvent(Event):
    def __init__(self,posxy):
        Event.__init__(self)
        self.pos = posxy
        self.verboseInfo = "\tPosition: " + str(self.pos) + "\n"
        
class DragBeganEvent(Event):
    def __init__(self,posxy):
        Event.__init__(self)
        self.pos = posxy
        self.verboseInfo = "\tPosition: " + str(self.pos) + "\n"        
        
class AddDragBeganEvent(Event):
    def __init__(self,posxy):
        Event.__init__(self)
        self.pos = posxy
        self.verboseInfo = "\tPosition: " + str(self.pos) + "\n"      
        
class DragEvent(Event):
    def __init__(self,startxy,currxy):
        Event.__init__(self)
        self.start = startxy;
        self.curr = currxy;
        self.verboseInfo = "\tStartPos: " + str(self.start) + "\n" + \
                           "\tCurrPos: " + str(self.curr) + "\n"

class DragCompletedEvent(Event):
    def __init__(self,startxy,endxy):
        Event.__init__(self)
        self.start = startxy
        self.curr = endxy
        self.verboseInfo = "\tStartPos: " + str(self.start) + "\n" + \
                           "\tEndPos: " + str(self.curr) + "\n"
 
class AddDragCompletedEvent(Event):
    def __init__(self,startxy,endxy):
        Event.__init__(self)
        self.start = startxy
        self.curr = endxy
        self.verboseInfo = "\tStartPos: " + str(self.start) + "\n"+\
                           "\tEndPos: " + str(self.curr) + "\n"

class SetDestinationEvent(Event):
    def __init__(self,posxy):
        Event.__init__(self)
        self.pos = posxy
        self.verboseInfo = "\tPosition: " + str(self.pos) + "\n"
        
class InitiateActionEvent(Event):
    def __init__(self,posxy):
        Event.__init__(self)
        self.pos = posxy
        self.verboseInfo = "\tPosition: " + str(self.pos) + "\n"
