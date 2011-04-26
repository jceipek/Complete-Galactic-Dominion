from Event import Event

class NotificationEvent(Event):
    """
    Event which contains a string message.
    """
    def __init__(self,message):
        Event.__init__(self)
        self.message = message
        self.verboseInfo = "\tMessage: " + str(self.message) + "\n"

class ResourceChangeEvent(Event):
    
    def __init__(self,resource,amount):
        Event.__init__(self)
        self.resource = resource
        self.amount = amount

class EntityFocusEvent(Event):
    
    def __init__(self,entity):
        
        Event.__init__(self)
        self.entity = entity
