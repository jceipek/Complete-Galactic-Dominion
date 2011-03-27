from MapObject import MapObject
import pygame
from collections import deque
from GameData import Locals # includes statuses

class Entity(MapObject):
    """A foreground L{MapObject} with which one can interact."""
    
    # Class variable which keeps track of id of all entities
    # updated with each initialization of Entity and child classes
    IDcounter = 0
    
    def __init__(self, imagePath, x, y, world, colorkey=None,
                 description = 'No information available.'):
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
        
        MapObject.__init__(self, imagePath, x, y, colorkey)
        
        self.__class__.IDcounter += 1 # Increment class counter
        
        # sets entityID.  Unique for all Entities
        self.entityID = self.__class__.IDcounter
        
        self.world = world
        
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
        
        self.maxHealth = 100
        self.curHealth = self.maxHealth
        self.size = 100 #radius of collision
        self.status = Locals.IDLE
        self.time = pygame.time.get_ticks()
        self.timePrev = 0
        self.timePassed = self.time-self.timePrev
        self.selected = False
        self.blockable = False

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
        
        drawOffset = -worldOffset[0],-worldOffset[1]
        drawRect = self.rect.move(drawOffset)
        #drawRect.top = drawRect.top%gridHeight
        #drawRect.left = drawRect.left%gridWidth
        
        if self.selected:
            self.drawSelectionRing(screen,drawRect)
        
        screen.blit(self.image,drawRect)

    def drawSelectionRing(self, screen, drawRect):
        pygame.draw.circle(screen, (255,255,255), drawRect.center, 20, 1)

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
        del self

    def changeHealth(self, numHits):
        """changes current health by numHits, removes object if current health drops to 0"""
        self.curHealth+=numHits
        if curHealth<=0:
            self.die()
            
    def moveWrap(self):
        gridWidth,gridHeight = self.world.gridDim
        self.rect.top = self.rect.top%gridHeight
        self.rect.left = self.rect.left%gridWidth
        
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
        
        self.vel = (0,0)
    
    def update(self):
        """Implements random movement to test with."""
        from random import randint
        #self.rect.move_ip(randint(-4,4), randint(-4,4))
        #self.moveWrap()

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
    for i in range(50):
        w.addEntity(TestEntity('ball.png',i*50,i*50, w, (255,255,255)))
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
        print 'Currently %d entities on the screen'%len(curScreenEntities)
        
        for ent in w.getScreenEntities(screenZone):
            
            ent.draw(screen)
            
        pygame.display.flip()
        
        ms_elapsed = gameClock.tick(MAX_FPS)
        print 'Current frames per second: %d'%int(1000.0/ms_elapsed)
