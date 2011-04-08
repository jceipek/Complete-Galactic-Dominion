import pygame
import specialMath

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

class DragBox(object):
    
    def __init__(self,start):
        self.start = self.current = start
        self.visible = False
        self.boundingBox = pygame.Rect(start,(0,0))
    
    def update(self,current):
        self.current = current
        if specialMath.distance(current,self.start) > 5:
            self.visible = True
            self.updateBoundingBox()
        else:
            self.visible = False
    
    def setCorner(self,current):
        self.current = current
    
    def draw(self,surface):
        if self.visible:
            dragBoxColor = (150,150,0)
            dragBoxThickness = 3
            pygame.draw.rect(surface,dragBoxColor,self.boundingBox,dragBoxThickness)
        
    def updateBoundingBox(self):
        self.boundingBox = MakeBoundingBox(self.start,self.current)
        #x1,y1 = self.start
        #x2,y2 = self.current
        
        #bboxRect = (pygame.Rect(self.start,(x2-x1,y2-y1)))
        #bboxRect.normalize() # Normalizes to remove negative sizes.
        #self.boundingBox = bboxRect

def MakeBoundingBox(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    
    bboxRect = (pygame.Rect(p1,(x2-x1,y2-y1)))
    bboxRect.normalize() # Normalizes to remove negative sizes.
    return bboxRect

class HealthBar():
    
    def __init__(self,owner,hBarHeight=10,padY=3,scaleX=1,capWidth=True):
        
        from pygame import Surface
        
        self.owner = owner
        self.maxHealth = owner.maxHealth
        self.curHealth = owner.curHealth
        
        self.padY = padY
        self.hBarHeight = hBarHeight
        if capWidth:
            self.hBarWidth = min(owner.rect.width*scaleX,50)
        else:
            self.hBarWidth = owner.rect.width
        self.scaleHealth = 1
        
        self.healthBar = pygame.Surface((self.hBarWidth,self.hBarHeight))
        
        # set self.healthRemaining set self.healthLost
        self.updateHealthBar()
        
    def updateHealthBar(self):
        """
        Updates the self.healthBar surface to reflect the current state
        of the owner.
        """
        
        self.updateHealthStatus()
        healthRemaining = (0,0,self.scaleHealth,self.hBarHeight)
        healthLost = (self.scaleHealth,0,self.hBarWidth-self.scaleHealth,self.hBarHeight)
        
        self.healthBar.fill((0,255,0), healthRemaining)
        self.healthBar.fill((255,0,0), healthLost)
    
    def updateHealthStatus(self):
        """
        Updates max health, current health, and scale health (percentage
        of current health to max health) from the owner.
        """
        
        self.maxHealth = self.owner.maxHealth
        self.curHealth = self.owner.curHealth
        
        self.scaleHealth = round((float(self.curHealth)/self.maxHealth)*self.hBarWidth)
    
    def draw(self,surface,midTop):
        """
        Draws health bar to the given surface, centered at the provided
        (x,y) coordinate tuple midTop.
        """
        
        centerX, top = midTop
        hBarTop = top - self.padY - self.hBarHeight
        surface.blit(self.healthBar,(centerX-self.hBarWidth//2,hBarTop))
