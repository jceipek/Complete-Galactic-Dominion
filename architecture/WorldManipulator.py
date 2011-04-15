import Event
from Entity import Entity
from Listener import Listener
from Unit import Unit

class WorldManipulator(Listener):
    def __init__(self,manager,world,networked=True):
        eventTypes = [ Event.EventExecutionEvent,Event.WorldManipulationEvent]
        Listener.__init__(self,manager,eventTypes)
        
        self.networked=networked
        self.world=world
    
    def notify(self,event):
        if (self.networked and isinstance(event,Event.EventExecutionEvent)) or\
         (not self.networked and isinstance(event, Event.WorldManipulationEvent)):
             data=event.data
             if data[0]=='Unit':
                 
                 #parse the list and replace the 'world' string with self.world
                 for i in xrange(len(data)):
                     if data[i] == 'world':
                         data[i]=self.world
                 #self.world.addEntity(Unit(*data[1:]))
                 Unit(*data[1:])
