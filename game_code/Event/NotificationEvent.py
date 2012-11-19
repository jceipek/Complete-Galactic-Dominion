from Event import Event

class NotificationEvent(Event):
    """
    Event which contains a string message.
    """
    def __init__(self,message,playerID):
        Event.__init__(self)
        self.message = message
        self.verboseInfo = "\tMessage: " + str(self.message) + "\n"
        self.playerID = playerID

class ResourceChangeEvent(Event):
    
    def __init__(self,resource,amount,playerID):
        Event.__init__(self)
        self.resource = resource
        self.amount = amount
        self.playerID = playerID

class EntityFocusEvent(Event):
    
    def __init__(self,entity):
        
        Event.__init__(self)
        self.entity = entity
        
class SelectedEntityEvent(Event):
    
    def __init__(self,entityList):
        
        Event.__init__(self)
        self.entityList = entityList

class GameOverEvent(Event):
    
    def __init__(self):
        
        Event.__init__(self)
