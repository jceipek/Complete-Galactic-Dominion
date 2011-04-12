import Event
from Entity import Entity
from Listener import Listener

class WorldManipulator(Listener):
    def __init__(self,manager,world,networked=True):
        eventTypes = [ Event.EventExecutionEvent,Event.WorldManipulationEvent]
        Listener.__init__(self,manager,eventTypes)
        
        self.networked=networked
        self.world=world
    
    def notify(self,event):
        if (self.networked and isinstance(event,Event.EventExecutionEvent)) or\
         (not self.networked and isinstance(event, Event.WorldManipulationEvent)):
            if isinstance(event.data,Entity):
                self.world.addEntity(event.data)
            
