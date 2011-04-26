import Event
from Entity import Entity
from Listener import Listener
from Unit import Unit,TestUnit
from Structure import TestTownCenter
from Overlay import HealthBar
import cPickle

class WorldManipulator(Listener):
    def __init__(self,manager,world,networked=True,gameClientID=None):
        eventTypes = [ Event.EventExecutionEvent,Event.WorldManipulationEvent,Event.StartedEvent,Event.GameLoadedEvent]
        Listener.__init__(self,manager,eventTypes)
        
        self.networked=networked
        self.world=world
        self.gameClientID = gameClientID
        print 'WorldManipulator thinks the gameID is',gameClientID
    
    def notify(self,event):
        if isinstance(event, Event.StartedEvent):
            self.manager.post(Event.LoadGameEvent())
        if isinstance(event, Event.GameLoadedEvent):
            if self.gameClientID != 0:
                for i in xrange(4):
                    print 'creating a unit with playerID',self.gameClientID
                    self.manager.post(Event.WorldManipulationEvent(['create',TestUnit,(i*50,i*50,self.world.worldID,self.gameClientID)]))
                from random import randint,choice
                xpos = randint(0,self.world.gridDim[0])
                ypos = randint(0,self.world.gridDim[1])
                self.manager.post(Event.WorldManipulationEvent(['create',TestTownCenter,(xpos,ypos,self.world.worldID,self.gameClientID)]))
        elif (self.networked and isinstance(event,Event.EventExecutionEvent)) or\
         (not self.networked and isinstance(event, Event.WorldManipulationEvent)):
             
             data = event.data
             if 'GetWorld' in data:
                 return
            
             if self.networked:
                try:
                    cmd = cPickle.loads(data)
                except:
                    print 'LOAD FAILED, this is a fatal error PLEASE try to fix this\n'
                    #if data == '':
                    #    return
                    cmd = cPickle.loads(data)
             else:
                cmd = data
                
             if isinstance(cmd,Entity):
                 entity = cmd
                 entity.world = self.world.universe.worldIDToWorld[entity.world]
                 entity.world.universe.entityIDToEntity[entity.entityID] = entity
                 entity.world.allEntities[entity.entityID] = entity
                 entity.world.playerCount.setdefault(entity.owner,[]).append(entity.entityID)
                 print 'loadedEntity ID',entity.entityID
                 
                 if isinstance(entity,Unit) and entity.objectOfAction != None:
                     entity.objectOfAction = self.world.universe.entityIDToEntity.get(entity.objectOfAction,entity.objectOfAction)

             elif isinstance(cmd,list):
                if cmd[0] == 'act':
                    #this list should be in the form ['act',entityID_1,entityID_2]
                    entity = self.world.universe.entityIDToEntity[cmd[1]]
                    obj = self.world.universe.entityIDToEntity[cmd[2]]
                    print 'Object of action id:',cmd[2]
                    
                    #not sure if this will work, fix this later
                    if obj is not None:
                        print 'Entity owned by: %s\nActing on entity owned by: %s' % (str(entity.owner),str(obj.owner))
                        entity.execAction(obj)
                    
                elif cmd[0] == 'create':
                    #this list should be in the form ['create',class,*initArgs]
                    args = list(cmd[2])
                    print args[2]
                    args[2] = self.world.universe.worldIDToWorld[args[2]]
                    cmd[1](*args)
                    
                elif cmd[0] == 'setpath':
                    #list should be in the form ['setpath',entityID,coordinate_tuple]
                    entity=self.world.universe.entityIDToEntity[cmd[1]]
                    entity.addToPath(cmd[2],servercommand=True)
