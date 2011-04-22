from Event import Event

class NotificationEvent(Event):
    """
    Event which contains a string message.
    """
    def __init__(self,message):
        Event.__init__(self)
        self.message = message
        self.verboseInfo = "\tMessage: " + str(self.message) + "\n"
