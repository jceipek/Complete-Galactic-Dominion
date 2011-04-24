import pygame
from Sign import Sign
from HUDElements import DescriptionBox, SelectedUnitBar, Notification
from GameData import Locals

class HUD(object):
    def __init__(self, loc, size):
        self.loc=loc
        self.size=size
        self.surface=pygame.Surface(size)
        self.descBox = DescriptionBox()
        self.selectedUnitBar = SelectedUnitBar()
        self.rect = pygame.Rect(self.loc,self.size)
        self.width=200
        self.viewport=None
        self.infoRect=pygame.Rect((0,20), (self.size[0], self.size[1]-20))
        self.note=Notification()
        
    def draw(self, displaySurface):
        self.drawSelected()
        displaySurface.blit(self.surface, (self.loc,self.size))
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
    def drawNotification(self, event=None):
        note=Notification()
        note.draw(self.surface)

    def drawSelected(self):
		
		self.selectedUnitBar.updateWithUnits(self.viewport.selectedEntities)
