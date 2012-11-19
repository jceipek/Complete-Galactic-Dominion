import pygame
from Sign import Sign
from HUDElements import DescriptionBox, SelectedUnitBar, Notification, NotificationList,ResourceBar
from GameData import Locals

from Listener import Listener

import Event

class HUD(Listener):
    """
    Heads-Up Display contains elements to inform the player of
    the resources owned, health of selected entities, and
    description an entity being hovered over.
    Displays other pertinent information through notifications.

    @param descBox: Shows information about a hovered entity
    @type descBox: DescriptionBox

    @param resourceBar: Shows the number of resources owned by the player
    @type descBox: ResourceBar

    @param selectedUnitBar: Bar displaying the units selected
    @type selectedUnitBar: SelectedUnitBar

    @param clientID: id number of the player
    @type clientID: int

    @param viewport: reference to the player's viewport, not currently used
    @type viewport: Viewport

    @param note: Shows information regarding relevent events
    @type note: NotificationList
    
    """
    
    def __init__(self,manager,clientID):
        
        eventTypes = [Event.NotificationEvent, Event.ResourceChangeEvent,
            Event.EntityFocusEvent, Event.SelectedEntityEvent]
        
        Listener.__init__(self,manager,eventTypes)
        
        self.descBox = DescriptionBox()
        self.resourceBar = ResourceBar((811,0))
        self.selectedUnitBar = SelectedUnitBar()

        self.clientID = clientID

        #self.infoRect=pygame.Rect((0,20), (self.size[0], self.size[1]-20))
        self.note=NotificationList()
        
    def draw(self, displaySurface):
        #Draws elements of HUD to surface
        self.selectedUnitBar.draw(displaySurface)
        self.descBox.draw(displaySurface)
        self.note.draw(displaySurface)
        self.resourceBar.draw(displaySurface)

    def setClientID(self,clientID):
        self.clientID = clientID

    def addNotification(self, event):
        '''
        Called when a notification is sent to the player
        Usage:
        ========================
           self.note.add(Notification('Imma notify you'))
           self.note.add(Notification('This is a longer lasting notification', time=8))
        '''
        note=Notification(event.message)
        self.note.add(note)

    def drawSelected(self,event):
		# FIXME - This line makes it so that the unit bars are updated
		# only when a change occurs, but this doesn't preserve
		# changes in unit orientation
		#if self.viewport.selectedEntitiesChanged():
		self.selectedUnitBar.updateWithUnits(event.entityList)

    def processUpdateEvent(self, event):
        timeElapsed = event.elapsedTimeSinceLastFrame
        self.note.update(timeElapsed)
        
    def notify(self, event):
        
        if isinstance(event, Event.NotificationEvent):
            if event.playerID == self.clientID:
                self.addNotification(event)
        elif isinstance(event, Event.ResourceChangeEvent):
            # event has a .resource and .amount attribute
            # ONLY HANDLES GOLD CURRENTLY
            if event.playerID == self.clientID:
                self.resourceBar.setResourceCount(event.amount)
        elif isinstance(event, Event.EntityFocusEvent):
            # has an entity attribute containing a reference to an entity
            self.descBox.updateDisplayedEntity(event.entity)

        elif isinstance(event, Event.SelectedEntityEvent):
            self.drawSelected(event)
