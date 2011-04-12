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
        self.setCorner(current)
        if specialMath.distance(self.current,self.start) > 5:
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

    def scroll(self,scrollChange):
        #self.start = self.start
        self.start=self.start[0]-scrollChange[0],self.start[1]-scrollChange[1]
        self.updateBoundingBox()
        #if scrollOffset[0] == 0:
        #    print self.start
        
    def findContainedEntities(self):
        
        t,l = self.boundingBox.topleft
        if top < 0 or l < 0:
            pass

def MakeBoundingBox(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    
    bboxRect = (pygame.Rect(p1,(x2-x1,y2-y1)))
    bboxRect.normalize() # Normalizes to remove negative sizes.
    return bboxRect

class HealthBar():
    
    def __init__(self,owner,hBarHeight=5,padY=3,scaleX=1,capWidth=True):
        
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

class MiniMap(object):
    
    def __init__(self, world, width=400, height=200, \
        borderColor=(0,0,0), borderWidth=5):
        
        self.world = world
        
        self.width = width
        self.height = height

        self.gridDict = self.world.grid.grid
        self.gridSize = self.world.grid.gridSize
        self.tileSize = self.world.grid.tileWidth,self.world.grid.tileHeight
        self.scale = self.width//(2*self.gridSize[0])
        
        # Offsets for drawing minimap data
        self.xOffset = self.width//2 - self.gridSize[0]*self.scale
        self.yOffset = self.height//2
        
        self.borderColor=borderColor
        self.borderWidth=borderWidth
        
        self.alphaColor = (255,0,255)
        self.baseSurface = pygame.Surface((width,height)) 
        self.baseSurface.convert()
        self.baseSurface.set_colorkey(self.alphaColor) 
        self.rect = self.baseSurface.get_rect()
        self._updateBaseSurface()
        
        self.dynamicSurface = pygame.Surface((width,height))
        self._updateDynamicSurface()
        
    def update(self):
        self._updateDynamicSurface()
    
    def draw(self,surf):
        surf.blit(self.baseSurface,self.rect)
        surf.blit(self.dynamicSurface,self.rect)
    
    def _updateDynamicSurface(self):

        from copy import copy

        newSurface = copy(self.baseSurface)#pygame.Surface((self.width,self.height))
        #newSurface.blit(self.baseSurface,self.rect)
        
        for entity in self.world.allEntities.values():
            
            entityPos = entity.rect.center
            
            gridPos = entityPos[0]/self.tileSize[1],entityPos[1]/self.tileSize[1]
            rawPos = specialMath.cartToIso(gridPos)
            drawPos = int(self.scale*rawPos[0]+self.xOffset),int(self.scale*rawPos[1]+self.yOffset)
            
            color = entity.getAverageColor()
            pygame.draw.circle(newSurface, color, drawPos, 3)
            
        self.dynamicSurface = newSurface
    
    def _updateBaseSurface(self):
        """
        Initializes the self.baseSurface attribute.  This stores
        the image of the map.
        """

        #fill base surface with alphaColor -> transparent
        pygame.draw.rect(self.baseSurface,self.alphaColor,self.rect,0)

        for y in range(self.gridSize[1]):
            for x in range(self.gridSize[0]):
                
                # Grab average color value of the grid at loc x,y
                curColor = (self.gridDict[(x,y)]).getAverageColor()
                
                # Calculate corners of polygons
                topleft = specialMath.cartToIso((x*self.scale,y*self.scale))
                topright = specialMath.cartToIso(((x+1)*self.scale,y*self.scale))
                bottomright = specialMath.cartToIso(((x+1)*self.scale,(y+1)*self.scale))
                bottomleft = specialMath.cartToIso((x*self.scale,(y+1)*self.scale))
                
                # Apply offsets
                topleft = (topleft[0]+self.xOffset,topleft[1]+self.yOffset)
                topright = (topright[0]+self.xOffset,topright[1]+self.yOffset)
                bottomright = (bottomright[0]+self.xOffset,bottomright[1]+self.yOffset)
                bottomleft = (bottomleft[0]+self.xOffset,bottomleft[1]+self.yOffset)
                
                # Draws minimap to baseSurface
                pygame.draw.polygon(self.baseSurface, curColor, \
                    [topleft,topright,bottomright,bottomleft])
        
        tl = specialMath.cartToIso((0,0))
        tr = specialMath.cartToIso((self.gridSize[0]*self.scale,0))
        br = specialMath.cartToIso((self.gridSize[0]*self.scale,self.gridSize[1]*self.scale))
        bl = specialMath.cartToIso((0,self.gridSize[1]*self.scale))
        
        tl = (tl[0]+self.xOffset-self.borderWidth,tl[1]+self.yOffset)
        tr = (tr[0]+self.xOffset,tr[1]+self.yOffset-self.borderWidth)
        br = (br[0]+self.xOffset+self.borderWidth,br[1]+self.yOffset)
        bl = (bl[0]+self.xOffset,bl[1]+self.yOffset+self.borderWidth)
        
        pygame.draw.polygon(self.baseSurface,self.borderColor, \
            [tl,tr,br,bl],self.borderWidth)
        
        # For debugging purposes
        #pygame.draw.rect(self.baseSurface,(150,150,150),\
        #        self.baseSurface.get_rect(),5)
                
if __name__ == "__main__":
    screenSize = (width, height) = (1024, 768)
    screenLoc = [0.0, 0.0]

    RUNNING = True
    pygame.init()
    screen = pygame.display.set_mode(screenSize)
    screenZone = screen.get_rect()

    from World import World
    from Unit import Unit
    from Entity import TestEntity
    
    w = World()
    m = MiniMap(w)
    #a = DrawableObject('orbPurpleBlack.png',(255,255,255))
    #print a.getAverageColor()
    for i in range(10):
        w.addEntity(TestEntity('orb.png',i*50,i*50,w,'alpha'))
    
    MAX_FPS = 60
    gameClock = pygame.time.Clock()
    pygame.init()
    
    while RUNNING:
        
        pygame.init()
        m.update()
        m.draw(screen)
        pygame.display.flip()
        
        ms_elapsed = gameClock.tick(MAX_FPS)
        
        for entity in w.allEntities.values():
            entity.update()
        #print 'Current frames per second: %d'%int(1000.0/ms_elapsed)
