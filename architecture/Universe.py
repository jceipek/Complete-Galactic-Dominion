import pygame
import Event
from Listener import Listener
from World import World

class Universe(Listener):

    def __init__(self,manager,world=None):
        eventTypes = [Event.UpdateEvent]
        Listener.__init__(self,manager,eventTypes)
        self.worldList = []
        
        if world is None:
            world = World()
        self.activeWorld = world

    def addWorld(self,world=None):
        if world is None:
            world = World()
        self.worldList.append(world)

    def changeWorld(self,newWorld):
        """
        Changes the active world to the given world.  If this world
        already exists, it deletes it in worldList.  The previous
        activeWorld is added to the worldList.
        """
        self.addWorld(self.activeWorld)
        if newWorld in self.worldList:
            del self.worldList[newWorld]
        self.activeWorld = newWorld
    
    def update(self):
        self.activeWorld.update()
        self.manager.post(Event.RenderEvent())
        #let the event manager know that the current world is updated
        for world in self.worldList:
            if not world is self.activeWorld:
                world.update()
    
    def notify(self,event):
        if isinstance(event,Event.UpdateEvent):
            self.update()#this may become a thread
