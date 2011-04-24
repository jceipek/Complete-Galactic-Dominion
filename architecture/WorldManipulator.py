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
            
             #print 'Got a command to unpickle the string ' + data + '\n'*5
             if self.networked:
                cmd = cPickle.loads(data)
             else:
                cmd = data
             #print 'Successfully unpickled the string' + data + '\n'*5
             if isinstance(cmd,Entity):
                 entity = cmd
                 entity.world = self.world.universe.worldIDToWorld[entity.world]
                 self.world.universe.entityIDToEntity[entity.entityID] = entity
                 self.world.allEntities[entity.entityID] = entity
                 self.world.universe.creator.numberOfEntities+=1
                 #print entity.__class__, entity.objectOfAction
                 if (isinstance(entity,TestUnit) or isinstance(entity,Unit)) and entity.objectOfAction != None:
                     # DOES NOT TRY TO SET AGAIN IF IT FAILS CURRENTLY
                     entity.objectOfAction = self.world.universe.entityIDToEntity.get(entity.objectOfAction,entity.objectOfAction)
                     #print entity.objectOfAction
             elif isinstance(cmd,list):
                if cmd[0] == 'act':
                    #this list should be in the form ['act',entityID_1,entityID_2]
                    print cmd
                    entity = self.world.universe.entityIDToEntity[cmd[1]]
                    obj = self.world.universe.entityIDToEntity[cmd[2]]
                    entity.execAction(obj)
                elif cmd[0] == 'create':
                    #this list should be in the form ['create',class,*initArgs]
                    args = list(cmd[2])
                    args[2] = self.world.universe.worldIDToWorld[args[2]]
                    print 'Begin creating the entity'
                    a=cmd[1](*args)
                    print 'Done creating the entity'
                    print 'Entity ID:',a.entityID
                elif cmd[0] == 'setpath':
                    print 'Trying to set the path'
                    #list should be in the form ['setpath',entityID,coordinate_tuple]
                    entity=self.world.universe.entityIDToEntity[cmd[1]]
                    entity.addToPath(cmd[2],servercommand=True)
