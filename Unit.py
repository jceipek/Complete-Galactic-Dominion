import Builder
import pygame

class Unit(pygame.sprite.Sprite):
    """A kind of Builder that can move around."""

    # Static class attribute--keeps track of all units initialized
    # by this computer (one particular player)
    allUnits = pygame.sprite.Group()
    
    def __init__(self, imagePath, colorkey=None):
        # Will set the image and rect properties required by Sprite
        Builder.__init__(self, imagePath, colorkey)
        Unit.allUnits.add(self)

    def update(self):
        """Called by game each frame to update object."""
        pass

    def kill(self):
        """Removes the current Sprite from all groups.  It will no longer
        be associated with this class."""
        pygame.sprite.Sprite.kill(self)
