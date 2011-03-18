import MapObject
import pygame

class EnumStatuses:
    IDLE = 0
    GATHERING = 1
    ATTACKING = 2
    MOVING = 3
    BUILDING = 4


class Entity(MapObject,pygame.sprite.Sprite):
    """
    A foreground MapObject with which one can interact.
    
    These objects may contain worlds inside them.
    
    #Attributes:
    #   world = world inside this entity. None if this is an entity that cannot 
                                          be entered
    
    ###### Attributes in progress
    description: description of behavior, abilities
    x: position
    y: position
    maxHealth: maximum/ default health points
    curHealth: current health
    size: radius of collision
    status: status of entity
    ######
    
    """
    
    
    def __init__(self, imagePath, colorkey=None,
                 description = 'No information available.'):    
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

        
    Methods:
    die(self): entity is removed from map
    changeHealth(self, numHits): decreases the health of the entity based on number of hits
    update(self): updates entity- performs actions    

    # First initialization of update method
    def update(self):
        """All Sprite objects should have an update function."""
        pass

    def showUponClicked(self):
        """Shows a list of options which can be invoked on an object.
        This should pull up some sort of clickable menu."""
        pass

    def showDescription(self):
        """Show the user the description of the entity.
        Needs to return more than just a string, eventually."""
        return self.description


