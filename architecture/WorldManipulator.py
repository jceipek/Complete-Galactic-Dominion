import Event
from Entity import Entity
from Listener import Listener
from Unit import Unit,TestUnit
from Structure import TestTownCenter
from Overlay import HealthBar
import cPickle

class WorldManipulator(Listener):
    """
    Class which acts as the point of contact between the server and the
    game state stored in the World for which this is the manipulator.
    
    When a relevant event is received, it will execute the event 
    according to its contents, changing the state of the world.  The 
    world will only be changed if the server triggers an action (sent
    to all clients) if the game is networked, or if a message is received
    locally from the event manager in a non-networked game.
    """
    def __init__(self,manager,world,networked=True,gameClientID=None):
        
        # registers the WorldManipulator as a Listener for the given
        # events with the event manager.
        eventTypes = [ Event.EventExecutionEvent,Event.WorldManipulationEvent,Event.StartedEvent,Event.GameLoadedEvent]
        Listener.__init__(self,manager,eventTypes)
        
        self.networked=networked
        self.world=world
        self.gameClientID = gameClientID
        print 'WorldManipulator thinks the gameID is',gameClientID
    
    def notify(self,event):
        """
        Called by the event manager when an event of interest is 
        received.
        """
        if isinstance(event, Event.StartedEvent):
            self.manager.post(Event.LoadGameEvent())
        if isinstance(event, Event.GameLoadedEvent):
            if self.gameClientID != 0: # gameClientID is 0 for the server
            
                # initialize a new player with 4 units on all clients
                for i in xrange(4):
                    print 'creating a unit with playerID',self.gameClientID
                    self.manager.post(Event.WorldManipulationEvent(
                        ['create',TestUnit,(i*50,i*50,self.world.worldID,self.gameClientID)]
                        ))
                
                # initialize a new player with one TestTownCenter
                # randomly on the world
                from random import randint,choice
                xpos = randint(0,self.world.gridDim[0])
                ypos = randint(0,self.world.gridDim[1])
                self.manager.post(Event.WorldManipulationEvent(
                    ['create',TestTownCenter,(xpos,ypos,self.world.worldID,self.gameClientID)]
                    ))
                    
        elif (self.networked and isinstance(event,Event.EventExecutionEvent)) or\
         (not self.networked and isinstance(event, Event.WorldManipulationEvent)):
             
            data = event.data
            if 'GetWorld' in data:
                return
            
            # if networked, unpickle the data contained by the event
            # this will be an Event.WorldManipulationEvent
            # if not networked, the data does not need to be unpickled.
            # this will be an Event.EventExecutionEvent
            if self.networked:
                try:
                    cmd = cPickle.loads(data)
                except:
                    print 'LOAD FAILED, this is a fatal error PLEASE try to fix this\n'
                    # refires the error
                    cmd = cPickle.loads(data)
            else:
                cmd = data
            
            if isinstance(cmd,Entity):
                entity = cmd
                 
                # convert the world of the unpickled entity from
                # an integer to a world reference
                entity.world = self.world.universe.worldIDToWorld[entity.world]
                 
                # store a reference in the universe mapping the entityID
                # to the local entity, to allow for network interaction
                # between entities by their entityIDs
                entity.world.universe.entityIDToEntity[entity.entityID] = entity
                 
                # add the entity to the world controlled by this 
                # world manipulator
                entity.world.allEntities[entity.entityID] = entity
                 
                print 'loadedEntity ID',entity.entityID
                 
                # if it is a unit with an objectOfAction, unmap the
                # objectOfAction id (entityID) back to a reference
                # to an entity
                if isinstance(entity,Unit) and entity.objectOfAction != None:
                    entity.objectOfAction = self.world.universe.entityIDToEntity.get(entity.objectOfAction,entity.objectOfAction)

            elif isinstance(cmd,list):
                # if cmd is a list of information...
                
                if cmd[0] == 'act':
                    #allows for one entity to act on another entity
                    #this list should be in the form ['act',entityID_1,entityID_2]
                    entity = self.world.universe.entityIDToEntity[cmd[1]]
                    obj = self.world.universe.entityIDToEntity[cmd[2]]
                    print 'Object of action id:',cmd[2]
                    
                    # execute the action on the objectOfAction
                    if obj is not None:
                        print 'Entity owned by: %s\nActing on entity owned by: %s' % (str(entity.owner),str(obj.owner))
                        entity.execAction(obj)
                    
                elif cmd[0] == 'create':
                    #creates a new entity
                    #this list should be in the form ['create',class,*initArgs]
                    args = list(cmd[2])
                    print args[2]
                    args[2] = self.world.universe.worldIDToWorld[args[2]]
                    cmd[1](*args)
                    
                elif cmd[0] == 'setpath':
                    #sets the path of an entity
                    #list should be in the form ['setpath',entityID,coordinate_tuple]
                    entity=self.world.universe.entityIDToEntity[cmd[1]]
                    entity.addToPath(cmd[2],servercommand=True)
