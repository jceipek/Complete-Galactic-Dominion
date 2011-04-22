import Event
from Entity import Entity
from Listener import Listener
from Unit import Unit,TestUnit
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
            
             #print 'Got a command to unpickle the string ' + data + '\n'*5
             try:
                cmd = cPickle.loads(data)
             except:
                cmd = data
             #print 'Successfully unpickled the string' + data + '\n'*5
             if isinstance(cmd,Entity):
                 entity = cmd
                 entity.world = self.world.universe.worldIDToWorld[entity.world]
                 self.world.universe.entityIDToEntity[entity.entityID] = entity
                 self.world.allEntities[entity.entityID] = entity
                 #print entity.__class__, entity.objectOfAction
                 if (isinstance(entity,TestUnit) or isinstance(entity,Unit)) and entity.objectOfAction != None:
                     # DOES NOT TRY TO SET AGAIN IF IT FAILS CURRENTLY
                     entity.objectOfAction = self.world.universe.entityIDToEntity.get(entity.objectOfAction,entity.objectOfAction)
                     print entity.objectOfAction
             elif isinstance(cmd,list):
                if cmd[0] == 'act':
                    entity = self.world.universe.entityIDToEntity[cmd[1]]
                    object = self.world.universe.entityIDToEntity[cmd[2]]
                    entity.execAction(object)
