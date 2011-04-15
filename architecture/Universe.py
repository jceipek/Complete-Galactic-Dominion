import pygame
import Event
from Listener import Listener
from World import World

class Universe(Listener):

    def __init__(self,manager,world=None):
        eventTypes = [Event.UpdateEvent]
        Listener.__init__(self,manager,eventTypes)
        
        self.creator = Creator()
        
        #self.worldList = []
        self.worldIDToWorld = {}
        self.activeWorld = world

    def addWorld(self,world,setToActive=False):
        #if world is None:
        #    world = World()
        #self.worldList.append(world)
        
        worldID = self.creator.registerWorld(world)
        self.worldIDToWorld[worldID] = world
        
        if setToActive:
            self.changeWorld(world)
        
        return worldID

    def addEntity(self,entity):
        return self.creator.registerEntity(entity)

    def changeWorld(self,newWorld):
        """
        Changes the active world to the given world.  If new world added
        to worldIDToWorld dict.
        """
        print 'Changing the world'
        
        if self.worldIDToWorld.get(newWorld.worldID,None) == None:
            self.addWorld(newWorld)
        
        self.activeWorld = newWorld
        
        #if newWorld in self.worldList:
        #    del self.worldList[newWorld]
        #self.activeWorld = newWorld
        a=Event.WorldChangeEvent(newWorld)
        print a
        self.manager.post(a)
    
    def update(self):
        if not self.activeWorld == None:
            self.activeWorld.update()
        self.manager.post(Event.RenderEvent())
        #let the event manager know that the current world is updated
        #for world in self.worldList:
        for world in self.worldIDToWorld.values():
            if not world is self.activeWorld:
                world.update()

    def copy(self):
        print 'Universe copy method not yet implemented.'
        pass

    def notify(self,event):
        if isinstance(event,Event.UpdateEvent):
            self.update()#this may become a thread

class Creator(object):
    
    def __init__(self):
        
        self.numberOfEntities = 0
        self.releasedEntityIDs = []
        
        self.numberOfWorlds = 0
        self.worldIDToAllEntities = {}
        self.releasedWorldIDs = []
        
    def registerWorld(self,world):
        
        self.numberOfWorlds+=1
        self.worldIDToAllEntities[self.numberOfWorlds] = world.allEntities
        return self.numberOfWorlds
    
    def unregisterWorld(self,world):
        
        self.numberOfWorlds-=1
        self.releasedWorldIDs.append(world.worldID)
    
    def registerEntity(self,entity):
        
        if self.releasedEntityIDs == []:
            self.numberOfEntities+=1
            return self.numberOfEntities
        else:
            return self.releasedEntityIDs.pop(0)
    
    def unregisterEntity(self,entity):
        
        self.numberOfEntities-=1
        self.releasedEntityIDs.append(entity.entityID)
