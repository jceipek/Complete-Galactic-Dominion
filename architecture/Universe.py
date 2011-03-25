import pygame
import Event
from Listener import Listener
from World import World

class Universe(Listener):
<<<<<<< HEAD
    
=======
>>>>>>> 7dfb9167b5a4533f596933c0239981e996184adb
    def __init__(self,manager,world=None):
        eventTypes = [Event.UpdateEvent]
        Listener.__init__(self,manager,eventTypes)
        self.worldList=[]
<<<<<<< HEAD
        
        if world is None:
            world = World()
        self.activeWorld = world
=======
        if world == None:
            self.activeWorld=World()
            self.worldList.append(self.activeWorld)
        else:
            self.activeWorld=world
            self.worldList.append(world)
>>>>>>> 7dfb9167b5a4533f596933c0239981e996184adb

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
        #let the event manager know that the current world is updated
        for world in self.worldList:
            if not world is self.activeWorld:
                world.update()
    
    def notify(self,event):
        if isinstance(event,Event.UpdateEvent):
            self.update()#this may become a thread
