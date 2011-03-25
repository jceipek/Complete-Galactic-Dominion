import pygame
import Event
from Listener import Listener
from World import World

class Universe(Listener):
    def __init__(self,manager,world=None):
        eventTypes = [Event.UpdateEvent]
        Listener.__init__(self,manager,eventTypes)
        self.worldList=[]
        if world == None:
            self.activeWorld=World()
            self.worldList.append(self.activeWorld)
        else:
            self.activeWorld=world
            self.worldList.append(world)

    def addWorld(self,world):
        pass#FIXME

    def changeWorld(self):
        pass#FIXME
    
    def update(self):
        self.activeWorld.update()
        #let the event manager know that the current world is updated
        for world in self.worldList:
            if not world is self.activeWorld:
                world.update()
    
    def notify(self,event):
        if isinstance(event,Event.UpdateEvent):
            self.update()#this may become a thread
