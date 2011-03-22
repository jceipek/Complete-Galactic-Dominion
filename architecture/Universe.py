import pygame
import Event
from Listener import Listener

class Universe(Listener):
    def __init__(self,manager):
        eventTypes = [Event.UpdateEvent]
        Listener.__init__(self,manager,eventTypes)
        self.worldList=[]
        
    def update():
        pass
    
    def notify(self,event):
        if isinstance(event,Event.RenderEvent):
            self.update()
