from MapObject import MapObject
import pygame
from collections import deque
from GameData import Locals # includes statuses
import specialMath
from Overlay import HealthBar
from Sign import Sign

from Event import NotificationEvent

class Entity(MapObject):
    """A foreground L{MapObject} with which one can interact."""
    
    # Class variable which determines how long it takes to build
    # an entity
    timeToBuild = 1
    
    # List of tuples containing a subclass of Resource and a cost
    costToBuild = []
    
    name = 'Generic Entity'
    
    def __init__(self, imagePath, x, y, world, colorkey=None,
                 description = 'No information available.',
                 movable = False, owner='tmp'):
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
        
        # MAYBE FIXME - ADDED WED, APR 20 TO TRY TO FIX OBJ PLACEMENT
        self.rect.center = (x,y)
        
        print 'Owner set to',str(owner)
        self.owner = owner
        
        # adds the entity to the provided world
        self.entityID = None
        # sets entityID
        #self.world.addEntity(self)

        # First initialization of description
        self.description = description
        self.realCenter=self.rect.center
        
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
        self.drawOffset=(0,0)#?

        #Image variables related to orientation
        self.imageCount = 1
        self.imageNum = None

        self.focused = False

        self.healthBar = HealthBar(self)
        
        self.regenRate = 0
        self._regenHealth = 0
        self.inventory=None
        
        self.selectionRect = self.imageBank.getMinimalRect(
            imagePath,colorkey,padding=25,showShadows=False)
        #self.selectionRectOffset = self.selectionRect.topleft
        #print self.selectionRect

    def _setEntityID(self,ID):
        self.entityID = ID

    def select(self):
        self.selected = True
        
    def deselect(self):
        self.selected = False

    def regenerate(self):
        self._regenHealth+=(self.getTimeElapsed()/1000.0)*self.regenRate
        
        if self._regenHealth >= 1:
            addHealth = int(self._regenHealth)
            self.changeHealth(addHealth)
            self._regenHealth-=addHealth
            
    # First initialization of update method
    def update(self):
        """All Sprite objects should have an update function."""
        if not self.hasFullHealth():
            self.regenerate()

    def draw(self,screen,worldOffset=(0,0)):
        """
        Draws the entity to the given surface.  The screen should be
        the same which the world grid is drawn on.  The worldOffset is
        the current location of the corner of the viewport in the 
        activeworld.
        """

        if self.drawOffset is None:
            return
        
        drawRect = self.rect.move(self.drawOffset)
        drawRect.center = self.world.grid.cartToIso(drawRect.center)
        
        selectRect = self.getSelectionRect(drawRect)
        
        if self.selected:
            self.drawSelectionRing(screen,selectRect)
        if self.selected or self.focused:
            self.drawHealthBar(screen,selectRect)
            self.focused = False

        screen.blit(self.image,drawRect)

    def getSelectionRect(self,drawRect):
        
        from copy import copy
        selRect = copy(self.selectionRect)
        selRect.topleft = drawRect.topleft
        selRect.top+=self.selectionRect.top
        selRect.left+=self.selectionRect.left
        
        return selRect
        
    def getSelectionRectOffset(self):
        return self.selectionRect.topleft

    def drawSelectionRing(self, screen, drawRect):
        pygame.draw.circle(screen, (255,255,255), drawRect.center, 20, 1)

    def drawHealthBar(self, screen, drawRect):
        self.healthBar.draw(screen,drawRect.midtop)

    def getInfo(self):
        text = '%s \n Description: \n %s' % (self.healthStr(), self.description)
        textBox=Sign(150, (0,0))
        textBox.addtext(text)
        textBox.render()
        return textBox

    def drawInfo(self, screen): #FIXME I am shitty.
        """Displays health and description"""
        text = '%s \n Description: \n %s' % (self.healthStr(), self.description)
        textBox=Sign(150, (0, 600), image=self.image)
        textBox.addtext(text)
        textBox.render()
        textBox.draw(screen)

    def healthStr(self):
        return 'Health: \n' +str(self.curHealth) + ' / ' +str(self.maxHealth)

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
        self.addNotification(NotificationEvent(self.description))
        #return self.description

    def die(self):
        """
        Removes the current Sprite from all groups.  It will no longer
        be associated with this class.
        """
        self.deselect()
        self.kill()
        self.world.removeEntity(self)

    def changeHealth(self, numHits):
        """changes current health by numHits, removes object if current health drops to 0"""
        self.curHealth+=numHits
        if self.curHealth<=0:
            self.curHealth=0
            self.die()
        elif self.curHealth > self.maxHealth:
            self.curHealth = self.maxHealth
        self.healthBar.updateHealthBar()
        
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
        return self.world.elapsedTimeSinceLastFrame
    
    def addToPath(self,newLoc,servercommand=False):
        """
        Adds a coordinate to the path of an entity.  This should be
        overriden for entities which can move.
        """
        pass
        
    def hasFullHealth(self):
        """
        Returns whether or not an entity is at full health.
        """
        return self.maxHealth == self.curHealth
        
    def addNotification(self,event):
        """
        Adds a notification to the list of world notifications.
        """
        self.world.addNotification(event)
        
    def sendEventToManager(self,event):
        """
        Sends an event to an event manager.
        """
        self.world.sendEventToManager(event)
        
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
