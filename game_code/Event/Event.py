class Event(object):
    """
    This is a superclass for any events that can be read by the low level event manager
    
    #Attributes:
    #   verboseInfo = A string of debugging info
    #   timeFired = The time that the event was posted to the manager
    """

    def __init__(self):
        self.verboseInfo = "\tNo Additional Debug Info Available\n"
        self.timeFired = 0

