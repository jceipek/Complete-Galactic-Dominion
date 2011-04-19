import pygame
from Sign import Sign

class HUD(object):
	def __init__(self, loc, size):
		self.loc=loc
		self.size=size
		self.surface=pygame.Surface(size)
		self.rect = pygame.Rect(self.loc,self.size)
		self.width=200
		self.viewport=None
		self.infoRect=pygame.Rect((0,20), (self.size[0], self.size[1]-20))
		self.drawNotification()
		
	def draw(self, displaySurface):
		self.drawSelected()
		displaySurface.blit(self.surface, (self.loc,self.size))

	def drawNotification(self, text='Something happened!'):
		sign=Sign(self.size[0], (0,0))
		sign.addtext(text)
		sign.render()
		sign.draw(self.surface)

	def showInfo(self, entity, pos=(0,0)):
		
		text = '%s \nDescription: \n%s' % (entity.healthStr(), entity.description)
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
			self.showInfo(e, pos=(i,20))
			i+=self.width
			
