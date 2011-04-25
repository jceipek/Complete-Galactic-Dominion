import Event
from Entity import Entity
from Listener import Listener
from Unit import Unit,TestUnit
from Overlay import HealthBar
import cPickle

class WorldManipulator(Listener):
    def __init__(self,manager,world,networked=True,gameClientID=None):
        eventTypes = [ Event.EventExecutionEvent,Event.WorldManipulationEvent]
        Listener.__init__(self,manager,eventTypes)
        
        self.networked=networked
        self.world=world
        self.gameClientID = gameClientID
    
    def notify(self,event):
        if (self.networked and isinstance(event,Event.EventExecutionEvent)) or\
         (not self.networked and isinstance(event, Event.WorldManipulationEvent)):
             
             data = event.data
             if 'GetWorld' in data:
                 return
            
             if self.networked:
                try:
                    cmd = cPickle.loads(data)
                except:
                    print 'LOAD FAILED, this is a fatal error PLEASE try to fix this\n'
                    if data == '':
                        return
                    cmd = cPickle.loads(data)
             else:
                cmd = data
                
             if isinstance(cmd,Entity):
                 entity = cmd
                 entity.world = self.world.universe.worldIDToWorld[entity.world]
                 self.world.universe.entityIDToEntity[entity.entityID] = entity
                 self.world.allEntities[entity.entityID] = entity
                 self.world.universe.creator.numberOfEntities+=1
                 
                 if (isinstance(entity,TestUnit) or isinstance(entity,Unit)) and entity.objectOfAction != None:
                     entity.objectOfAction = self.world.universe.entityIDToEntity.get(entity.objectOfAction,entity.objectOfAction)

             elif isinstance(cmd,list):
                if cmd[0] == 'act':
                    #this list should be in the form ['act',entityID_1,entityID_2]
                    entity = self.world.universe.entityIDToEntity[cmd[1]]
                    obj = self.world.universe.entityIDToEntity[cmd[2]]
                    print 'Entity owned by: %s\nActing on entity owned by: %s' % (str(entity.owner),str(obj.owner))
                    entity.execAction(obj)
                    
                elif cmd[0] == 'create':
                    #this list should be in the form ['create',class,*initArgs]
                    args = list(cmd[2])
                    args[2] = self.world.universe.worldIDToWorld[args[2]]
                    cmd[1](*args)
                    
                elif cmd[0] == 'setpath':
                    #list should be in the form ['setpath',entityID,coordinate_tuple]
                    entity=self.world.universe.entityIDToEntity[cmd[1]]
                    entity.addToPath(cmd[2],servercommand=True)
