import pygame
import Event
from Listener import Listener

#This will not be needed in the actual renderer
from random import randint

class Renderer(Listener):
    """
    A renderer simply draws object to the screen.
    It does not refresh the screen, but it tells the 
    screen to refresh.
    """
    
    def notify(self,event):
        #Overriding Listener Implementation
        if isinstance( event, Event.RenderEvent ):
            #In the actual implementation, messages will be sent out to do things like this
            #event.displaySurface.fill((randint(0,255),\
            #randint(0,255),\
            #randint(0,255)))
            
            #Done rendering? Draw to the screen
            self.manager.post(Event.RefreshEvent())