import pygame
from Sign import Sign
from HUDElements import DescriptionBox, SelectedUnitBar, Notification, NotificationList,ResourceBar
from GameData import Locals

from Listener import Listener

import Event

class HUD(Listener):
    
    def __init__(self,manager):
        
        eventTypes = [Event.NotificationEvent, Event.ResourceChangeEvent,
            Event.EntityFocusEvent]
        
        #Using this until someone can explain why super() is or is not the right way to do this
        #Waaaay too many disagreements/articles on this online
        Listener.__init__(self,manager,eventTypes)
        
        self.descBox = DescriptionBox()
        self.resourceBar = ResourceBar((811,0))
        self.selectedUnitBar = SelectedUnitBar()
        self.viewport=None
        self.note=NotificationList()
        
    def draw(self, displaySurface):
        self.drawSelected()
        self.selectedUnitBar.draw(displaySurface)
        self.descBox.draw(displaySurface)
        self.note.draw(displaySurface)
        self.resourceBar.draw(displaySurface)

    def addNotification(self, event):
        '''
        Called when a notification is sent to the player
        Usage:
        ========================
           self.note.add(Notification('Imma notify you'))
           self.note.add(Notification('This is a slightly shorter lasting notification', time=2))
           self.note.add(Notification('This is a longer lasting notification', time=8))
        '''
        note=Notification(event.message)
        self.note.add(note)

    def drawSelected(self):
		# FIXME - This line makes it so that the unit bars are updated
		# only when a change occurs, but this doesn't preserve
		# changes in unit orientation
		#if self.viewport.selectedEntitiesChanged():
		self.selectedUnitBar.updateWithUnits(self.viewport.selectedEntities)

    def processUpdateEvent(self, event):
        timeElapsed = event.elapsedTimeSinceLastFrame
        self.note.update(timeElapsed)
        
    def notify(self, event):
        
        if isinstance(event, Event.NotificationEvent):
            self.addNotification(event)
        elif isinstance(event, Event.ResourceChangeEvent):
            # ONLY HANDLES GOLD CURRENTLY
            self.resourceBar.setResourceCount(event.amount)
        elif isinstance(event, Event.EntityFocusEvent):
            # has an entity attribute containing a reference to an entity
            pass

