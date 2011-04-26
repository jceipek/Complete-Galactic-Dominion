import pygame
from Sign import Sign
from HUDElements import DescriptionBox, SelectedUnitBar, Notification, NotificationList
from GameData import Locals

class HUD(object):
    def __init__(self):
        self.descBox = DescriptionBox()
        self.selectedUnitBar = SelectedUnitBar()

        self.viewport=None
        #self.infoRect=pygame.Rect((0,20), (self.size[0], self.size[1]-20))
        self.note=NotificationList()
        
    def draw(self, displaySurface):
        self.drawSelected()
        self.selectedUnitBar.draw(displaySurface)
        self.descBox.draw(displaySurface)
        self.note.draw(displaySurface)

    """
    def drawNotification(self, event=None):
        if event is None:
            text = ''
        else:
            text = event.message
        sign=Sign(self.size[0], (0,0))
        sign.addtext(text)
        sign.render()
        sign.draw(self.surface)

    """
    def addNotification(self, event=None):
        note=Notification(event.message)
        self.note.add(note)

    def drawSelected(self):
		
		self.selectedUnitBar.updateWithUnits(self.viewport.selectedEntities)

    def processUpdateEvent(self, event):
        timeElapsed = event.elapsedTimeSinceLastFrame
        self.note.update(timeElapsed)
