import pygame

class Overlay(object): #FIXME - should inherit from drawable object?
    def __init__(self):
        pygame.font.init()
        self.fontFilename = pygame.font.get_default_font()
        self.font = pygame.font.Font(self.fontFilename,16)
        pass
        
    def draw(self,displaySurface,size):
        pass
        
class DebugOverlay(Overlay):
    def __init__(self):
        Overlay.__init__(self)
        self.fps = 0
        
    def processUpdateEvent(self,event):
        timeElapsed = event.elapsedTimeSinceLastFrame
        if timeElapsed>0:
            self.fps = int(1//(event.elapsedTimeSinceLastFrame/1000.0))
            
    def draw(self,displaySurface,size):
        fontSurf = self.font.render("FPS: "+str(self.fps), False, (255,255,255))
        displaySurface.blit(fontSurf,(0,0))
        