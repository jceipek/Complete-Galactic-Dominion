import pygame
from Sign import Sign
from DescriptionBox import DescriptionBox
from GameData import Locals

class HUD(object):
    def __init__(self, loc, size):
        self.loc=loc
        self.size=size
        self.surface=pygame.Surface(size)
        self.descBox = DescriptionBox()
        self.rect = pygame.Rect(self.loc,self.size)
        self.width=200
        self.viewport=None
        self.infoRect=pygame.Rect((0,20), (self.size[0], self.size[1]-20))
        self.drawNotification()
        
    def draw(self, displaySurface):
        self.drawSelected()
        displaySurface.blit(self.surface, (self.loc,self.size))
        self.descBox.draw(displaySurface)

    def drawNotification(self, event=None):
        if event is None:
            text = ''
        else:
            text = event.message
        sign=Sign(self.size[0], (0,0))
        sign.addtext(text)
        sign.render()
        sign.draw(self.surface)

    def showInfo(self, entity, pos=(0,0)):
        
        text = '%s \nDescription: \n%s \n%s' % (entity.healthStr(), entity.description, Locals.status[entity.status])
        box=Sign(200, pos, entity.image)
        if entity.inventory:
            text+='\n'+ str(entity.inventory)
        box.addtext(text)
        box.render()
        box.draw(self.surface)

    def drawSelected(self):
        i=0
        pygame.draw.rect(self.surface, (0,0,0), self.infoRect)
        for e in self.viewport.selectedEntities:
            if not e.selected:
                continue
            self.showInfo(e, pos=(i,20))
            i+=self.width
            
