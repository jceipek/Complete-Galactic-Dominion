import Event
from Entity import Entity
from Listener import Listener
from Unit import Unit
from Overlay import HealthBar
import cPickle

class WorldManipulator(Listener):
    def __init__(self,manager,world,networked=True):
        eventTypes = [ Event.EventExecutionEvent,Event.WorldManipulationEvent]
        Listener.__init__(self,manager,eventTypes)
        
        self.networked=networked
        self.world=world
    
    def notify(self,event):
        if (self.networked and isinstance(event,Event.EventExecutionEvent)) or\
         (not self.networked and isinstance(event, Event.WorldManipulationEvent)):
             
             data = event.data
             if 'GetWorld' in data:
                 return
             print 'Got a command to unpickle the string ' + data + '\n'*5
             entity = cPickle.loads(data)
             print 'Successfully unpickled the string' + data + '\n'*5
             
             print entity.__dict__
             
             entity.loadImage(entity.imagePath,entity.colorkey)
             entity.healthBar = HealthBar(self)
             entity.rect.center = entity.realCenter
             
             entity.world = self.world.universe.worldIDToWorld[entity.world]
             self.world.universe.entityIDToEntity[entity.entityID] = entity             
             if isinstance(entity,Unit) and entity.objectOfAction != None:
                 entity.objectOfAction = self.world.universe.entityIDToEntity[entity.objectOfAction]
