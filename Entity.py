import MapObject
import pygame
from collections import deque
from Event import WorldManipulationEvent

class Entity(MapObject,pygame.sprite.Sprite):
    """A foreground MapObject with which one can interact."""
	manager = None
    def __new__(cls, imagePath, x, y, colorkey=None,
                 description = 'No information available.',serverCmd=False):
        if serverCmd:
            superCls = super(TestClass, cls)
            return superCls.__new__(cls)
        else:
            a=[self.__class__]
            a.append(imagePath, x, y, colorkey,
                 description,True)
            Entity.manager.post(WorldManipulationEvent(a))
    
    def __init__(self, imagePath, x, y, colorkey=None,
                 description = 'No information available.',serverCmd=False):    
        MapObject.__init__(self, imagePath, colorkey)

        # First class to inherit from Sprite
        pygame.sprite.Sprite.__init__(self)

        # First initialization of description
        self.description = description

        # First initialization of options---
        # Dictionary mapping strings for display in a menu shown
        # upon being clicked to a callback function to execute.
        # Menu options should be added to this dictionary.
        self.options = {'Description': showDescription}
	self.x=x #x position
	self.y=y #y position
	self.maxHealth=100
	self.curHealth=self.maxHealth
	self.size=100 #radius of collision
	self.status=Entity.Locals.IDLE
	self.time=pygame.time.get_ticks()
	self.timePrev=0
	self.timePassed=self.time-self.timePrev


    # First initialization of update method
    def update(self):
        """All Sprite objects should have an update function."""

        pass

    def dtime(self):
	"""returns time since last call, used in update, keeps track of time between frames"""
	self.timePrev=self.time
	self.time=pygame.time.get_ticks()
	self.timePassed= self.time-self.timePrev

    def showUponClicked(self):
        """Shows a list of options which can be invoked on an object.
        This should pull up some sort of clickable menu."""
        pass

    def showDescription(self):
        """Show the user the description of the entity.
        Needs to return more than just a string, eventually."""
        return self.description

    def die(self):
	"""removes entity from map"""
	del self #not sure if this is right

    def changeHealth(self, numHits):
	"""changes current health by numHits, removes object if current health drops to 0"""
	self.curHealth+=numHits
	if curHealth<=0:
	    self.die()


class Locals:
    #Statuses
    IDLE = 0
    MOVING = 1
    BUILDING = 2
    GATHERING = 3
    ATTACKING = 4
    #Efficiency
    MOVE=0
    BUILD=1
    GATHER=2
    ATTACK=3

