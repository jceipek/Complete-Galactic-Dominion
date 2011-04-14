from MapObject import MapObject
import pygame
from collections import deque
from GameData import Locals # includes statuses
import specialMath
from Overlay import HealthBar

class Entity(MapObject):
    """A foreground L{MapObject} with which one can interact."""
    
    # Class variable which keeps track of id of all entities
    # updated with each initialization of Entity and child classes
    IDcounter = 0
    
    def __init__(self, imagePath, x, y, world, colorkey=None,
                 description = 'No information available.',
                 movable = False):
        """
        Set up an Entity with an image loaded from the filepath
        specified by imagePath, an absolute x and y position in a given
        world, and a default description.  The image is loaded with
        an optional alpha colorkey.
        
        @param IDcounter: class counter which increments for every
        entity which is created, giving each entity a unique id
        
        @param entityID: unique id given to each Entity when
        instantiated
        
        @param world: L{World} object in which the Entity exists
        @type world: L{World}
        
        @param description: string description of the entity
        
        @param options: dictionary mapping string keys to callbacks.
        Intended to be used for displaying a popup menu.  When an
        item is selected, its callback will execute.
        @type options: dict
        
        @param maxHealth: maximum health of the Entity
        @param curHealth: current health of the Entity
        
        @param size: radius of collision (not currently implemented)
        @param status: current status of the Entity.  Found in Locals.
        
        """
        self.world = world
        
        # Prevents entities from being initialized off of the grid
        self.worldSize = self.world.grid.getCartGridDimensions()
        x = x%self.worldSize[0]
        y = y%self.worldSize[1]
        
        MapObject.__init__(self, imagePath, x, y, colorkey)
        
        self.__class__.IDcounter += 1 # Increment class counter
        
        # sets entityID.  Unique for all Entities
        self.entityID = self.__class__.IDcounter
        
        # adds the entity to the provided world
        world.addEntity(self)

        # First initialization of description
        self.description = description

        # First initialization of options---
        # Dictionary mapping strings for display in a menu shown
        # upon being clicked to a callback function to execute.
        # Menu options should be added to this dictionary.
        self.options = {'Description': self.showDescription}
        #self.pos = (x,y) # defined by superclass
        
        self.movable = movable
        
        self.maxHealth = 100
        self.curHealth = self.maxHealth
        self.size = 100 #radius of collision
        self.status = Locals.IDLE
        self.time = pygame.time.get_ticks()
        self.timePrev = 0
        self.timePassed = self.time-self.timePrev
        self.selected = False
        self.blocking = False
        self.drawOffset=(0,0)

        self.healthBar = HealthBar(self)

    # First initialization of update method
    def update(self):
        """All Sprite objects should have an update function."""
    # Override this
        pass

    def draw(self,screen,worldOffset=(0,0)):
        """
        Draws the entity to the given surface.  The screen should be
        the same which the world grid is drawn on.  The worldOffset is
        the current location of the corner of the viewport in the 
        activeworld.
        """
        
        #gridWidth,gridHeight = self.world.gridDim
        '''
        drawOffset = \
        specialMath.isoToCart((-worldOffset[0],-worldOffset[1]))
        drawRect = self.rect.move(drawOffset)
        '''
        drawRect = self.rect.move(self.drawOffset)
        #left,top=self.world.grid.cartToIso(drawRect.topleft)
        #right,bottom=self.world.grid.cartToIso(drawRect.bottomright)
        #drawRect = pygame.Rect(left,top,right-left,bottom-top)
        
        drawRect.center = self.world.grid.cartToIso(drawRect.center)
        
        #drawRect.top = drawRect.top%gridHeight
        #drawRect.left = drawRect.left%gridWidth
        
        if self.selected:
            self.drawSelectionRing(screen,drawRect)
            self.drawHealthBar(screen,drawRect)
        
        screen.blit(self.image,drawRect)

    def drawSelectionRing(self, screen, drawRect):
        pygame.draw.circle(screen, (255,255,255), drawRect.center, 20, 1)

    def drawHealthBar(self, screen, drawRect):
        self.healthBar.draw(screen,drawRect.midtop)

    def dtime(self):
        """returns time since last call, used in update, keeps track of time between frames"""
        self.timePrev=self.time
        self.time=pygame.time.get_ticks()
        self.timePassed= self.time-self.timePrev

    def showUponClicked(self):
        """Shows a list of options which can be invoked on an object.
        This should pull up some sort of clickable menu."""
        pass #FIXME

    def showDescription(self):
        """Show the user the description of the entity.
        Needs to return more than just a string, eventually."""
        return self.description

    def die(self):
        """
        Removes the current Sprite from all groups.  It will no longer
        be associated with this class.
        """
        self.kill()
        self.world.removeEntity(self)

    def changeHealth(self, numHits):
        """changes current health by numHits, removes object if current health drops to 0"""
        self.curHealth+=numHits
        self.healthBar.updateHealthBar()
        if self.curHealth<=0:
            self.die()
        elif self.curHealth > self.maxHealth:
            self.curHealth = self.maxHealth
            
    def moveWrap(self):
        """
        FIXME !!!
        """
        self.rect.top = self.rect.top%self.worldSize[1]
        self.rect.left = self.rect.left%self.worldSize[0]
        
    def getTimeElapsed(self):
        """
        Returns the amount of time since the last frame.
        Stored in world which the entity belongs to.
        Updated by viewport.
        """
        return self.world.__class__.elapsedTimeSinceLastFrame
    
    def addToPath(self,newLoc):
        pass
        
class TestEntity(Entity):
    """
    This should be deleted once subclasses are implemented.  This
    is meant to clean up Entity.
    """
    
    def __init__(self, imagePath, x, y, world, colorkey=None,
                 description = 'No information available.'):
        """
        @param vel: tuple of velocities (vx,vy)
        """
        
        Entity.__init__(self, imagePath, x, y, world, colorkey, description)
        
        #self.vel = (-1,1)
        from random import randint
        self.vel = (10,-5)
        #self.vel = (randint(-2,2),randint(-2,2))
        #self.vel = (2,1)
    
    def update(self):
        """Implements random movement to test with."""
        self.rect.move_ip(self.vel)
        self.moveWrap()
        #if self.selected==True:
        #    print self.rect
        
class TestEntity2(Entity):
    """
    This should be deleted once subclasses are implemented.  This
    is meant to clean up Entity.
    """
    
    def __init__(self, imagePath, x, y, world, colorkey=None,
                 description = 'No information available.'):
        """
        @param vel: tuple of velocities (vx,vy)
        """
        
        Entity.__init__(self, imagePath, x, y, world, colorkey, description)
        
        #self.vel = (-1,1)
        from random import randint
        #self.vel = (randint(-2,2),randint(-2,2))
        self.vel = (10,10)
    
        self.grid = world.grid
        #worldSize = size of grid in pixels
    
    def update(self):
        """Implements random movement to test with."""
        self.rect.move_ip(self.vel)
        self.moveWrap()
        #if self.selected==True:
        #    print self.rect

if __name__ == "__main__":
    
    # TESTS TO SHOW ENTITIES WORK
    
    screenSize = (width, height) = (1024, 768)
    screenLoc = [0.0, 0.0]
    
    from World import World

    RUNNING = True
    pygame.init()
    screen = pygame.display.set_mode(screenSize)
    screenZone = screen.get_rect()

    w = World()
    print 'World initialized'
    
    # Creates entities to test with in world w
    for i in range(10):
        w.addEntity(Entity('ball.png',i*50,i*50, w, (255,255,255)))
        #print Entity.IDcounter
    
    MAX_FPS = 60
    gameClock = pygame.time.Clock()
    pygame.init()
    
    while RUNNING:
        
        # calls update function of all Entities in world
        w.update()
        
        screen.fill((0,0,0))
        
        # Grabs all entities that are currently on the screen from the 
        # world
        curScreenEntities = w.getScreenEntities(screenZone)
        #print 'Currently %d entities on the screen'%len(curScreenEntities)
        
        for ent in w.allEntities.values():
            
            ent.draw(screen)
            
        pygame.display.flip()
        
        ms_elapsed = gameClock.tick(MAX_FPS)
        print 'Current frames per second: %d'%int(1000.0/ms_elapsed)
